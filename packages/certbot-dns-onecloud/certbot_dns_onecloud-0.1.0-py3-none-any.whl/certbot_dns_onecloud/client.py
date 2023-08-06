# -*- coding: utf8 -*-

import json
import logging

import requests

from certbot import errors
from certbot.plugins import dns_common

__version__ = "0.0.1"


logger = logging.getLogger(__name__)


class OneCloudClient:
    """
    Encapsulates all communication with the onecloud API.
    """

    session = requests.session()
    api_url = "https://api.1cloud.ru"

    def __init__(self, token=None):
        self.common_params = {}
        self.token = token

    def set_token(self, token):
        """Setup token for ONECLOUD API

        :param str token: The ONECLOUD API Token, you can find it in
            [https://1cloud.ru/api/auth/auth].
        """

        self.token = token

    def add_txt_record(self, record, value, ttl):
        """
        Add a TXT record using the supplied information.

        :param str record: The record name
            (typically beginning with "_acme-challenge.").
        :param str value: The record content
            (typically the challenge validation).
        :param int record_ttl: The record TTL
            (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs when
            communicating with the ONECLOUD API
        """

        domain_id, domain_name = self._find_domain_id(record)
        logger.debug("Domain found: %s with id: %s", domain_name, domain_id)

        data = self._prepare_record_data(domain_id, record, value, ttl)
        logger.debug("Insert TXT record with data: %s", data)
        self._api_request("POST", "dns/recordtxt", data)

    def remove_txt_record(self, record, value):
        """
        Delete a TXT record using the supplied information.
        Note that both the record"s name and value are used to ensure that
            similar records created concurrently
            (e.g., due to concurrent invocations of this plugin)
            are not deleted.
        Failures are logged, but not raised.

        :param str record: The record name
            (typically beginning with "_acme-challenge.").
        :param str value: The record content
            (typically the challenge validation).
        """

        record_id, domain_id = self._find_txt_record(record, value)
        if record_id is not None:
            self._api_request("DELETE", "dns/{0}/{1}".format(domain_id, record_id))

    @staticmethod
    def _prepare_record_data(domain_id, record, value, ttl):
        """
        Prepare JSON for record data.

        :param str domain_id: Domain id of the zone.
        :param str record: Record name to add.
        :param str value: Record content to add.
        :param int ttl: The record TTL.
        :returns: Dictionary of record JSON.
        :rtype: dict
        """
        data = {
            "DomainId": domain_id,
            "Name": record,
            "Text": value,
            "TTL": ttl,
        }
        return data

    def _find_txt_record(self, record, value):
        """
        Find the record_id for a TXT record with the given name and content.

        :param str record: The record name
            (typically beginning with "_acme-challenge.").
        :param str value: The record content
            (typically the challenge validation).
        :returns: The record_id and domain_id, if found.
        :rtype: (int, int)
        """

        domain_id, ___ = self._find_domain_id(record)
        data = self._api_request("GET", "dns/{}".format(domain_id))
        host_name = "{}.".format(record)
        text_value = "\"{}\" ".format(value)
        for linked_record in data["LinkedRecords"]:
            if linked_record["TypeRecord"] != u"TXT":
                continue
            if linked_record["HostName"] != host_name:
                continue
            if linked_record["Text"] != text_value:
                continue
            return linked_record["ID"], domain_id
        logger.error(u"TXT record of %s not found", record)
        return (None, None)

    def _find_domain_id(self, record):
        """
        Find the managed zone for a given domain.

        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :returns: The ID and Name of the managed zone, if found.
        :rtype: (int, str)
        :raises certbot.errors.PluginError: if the managed zone cannot be found.
        """

        base_domain = self._get_base_domain(record)
        domain_dns_name_guesses = dns_common.base_domain_name_guesses(
            base_domain
        )

        owned_domains = self._get_domain_ids()

        for domain_name in domain_dns_name_guesses:
            # Get the domain id
            if domain_name in owned_domains:
                return owned_domains[domain_name], domain_name
        raise errors.PluginError("Domain not found")

    @staticmethod
    def _get_base_domain(record):
        """
        Extrat the "base_domain" from given record

        :param str record: The record name
            (typically beginning with "_acme-challenge.").
        :returns: base_domain, if found.
        :rtype: str
        :raises certbot.errors.PluginError: if no base_domain is found.
        """

        prefix = "_acme-challenge."
        if record.startswith(prefix):
            base_domain = record[len(prefix):]
        else:
            raise errors.PluginError(
                u"Unable to determine base_domain for {0}.".format(record)
            )

        logger.debug(u"%s => %s", record, base_domain)
        return base_domain

    def _get_domain_ids(self):
        """
        Get record id for the ACME challenge TXT record.

        :returns: Dictionary of domain names as key and id as value
        :rtype: dict
        """

        resp = self._api_request("GET", "dns")
        id_dict = {domain["Name"]: domain["ID"] for domain in resp}
        return id_dict

    def _api_request(self, method, endpoint, data=None):
        """
        Make a request against 1cloud API.

        :param str method: HTTP method to use.
        :param str endpoint: API endpoint to call.
        :param dict data: Dictionary to send a JSON data.
        :returns: Dictionary of the JSON response.
        :rtype: dict
        """
        headers = {"Authorization": "Bearer {0}".format(self.token)}
        url = self._get_url(endpoint)
        return self._request(method, url, data, headers)

    def _get_url(self, endpoint):
        """
        Get API URL for given endpoint.

        :param str endpoint: API endpoint.
        :returns: Full API URL.
        :rtype: str
        """
        return "{0}/{1}".format(self.api_url, endpoint)

    def _request(self, method, url, data=None, headers=None):
        """
        Make HTTP request.

        :param str method: HTTP method to use.
        :param str url: URL to call.
        :param dict data: Dictionary with data to send as JSON.
        :param dict headers: Headers to send.
        :returns: Dictionary of the JSON response.
        :rtype: dict
        :raises certbot.errors.PluginError: In case of HTTP error.
        """
        resp = self.session.request(method, url, json=data, headers=headers)
        logger.debug("API Request to URL: %s", url)
        error = None
        if resp.ok:
            try:
                result = resp.json()
            except json.JSONDecodeError:
                error = u"API response with non JSON: {0}".format(resp.text)
        else:
            try:
                result = resp.json()
            except json.JSONDecodeError:
                error = u"HTTP Error Status: {0}".format(resp.status_code)
            else:
                if "Message" in result:
                    error = result["Message"]
                else:
                    error = u"API response without Message: {0}".format(resp.text)
        if error:
            logger.error(u"[ONECLOUD] %s error: %s", method, error)
            raise errors.PluginError(
                u"Error communicating with the ONECLOUD API: {0}".format(error)
            )
        return result
