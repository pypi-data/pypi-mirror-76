# -*- coding: utf-8 -*-
"""Tests for certbot_dns_onecloud.client"""

import responses
import pytest
import json

from certbot import errors
from certbot.plugins.dns_test_common import DOMAIN
from certbot_dns_onecloud.client import OneCloudClient

API_TOKEN = "APITOKEN"
SUB_DOMAIN = "_acme-challenge"
RECORD_ID = 1
DOMAIN_ID = 1
RECORD_NAME = ".".join([SUB_DOMAIN, DOMAIN])
RECORD_VALUE = "record-value"
TTL = 42
ERROR_MSG = "error-message"
ERROR = {
    "Message": ERROR_MSG,
    "ModelState": {
    }
}


@pytest.fixture
def onecloud():
    onecloud = OneCloudClient(API_TOKEN)
    return onecloud


@responses.activate
def test_wrong_auth(onecloud):
    onecloud.set_token("INVALIDTOKEN")
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        status=401,
        body="Invalid API key"
    )

    with pytest.raises(errors.PluginError):
        onecloud.add_txt_record(RECORD_NAME, RECORD_VALUE, TTL)


@responses.activate
def test_add_txt_record(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        json=[{
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": []
        }]
    )
    responses.add(
        responses.POST, "https://api.1cloud.ru/dns/recordtxt",
        json={
            "ID": RECORD_ID,
            "TypeRecord": "TXT",
            "Text": RECORD_VALUE,
            "HostName": RECORD_NAME,
            "State": "Active",
            "TTL": TTL,
        }
    )
    onecloud.add_txt_record(RECORD_NAME, RECORD_VALUE, TTL)
    expected = {
        "DomainId": DOMAIN_ID,
        "Text": RECORD_VALUE,
        "TTL": TTL,
        "Name": RECORD_NAME
    }
    assert len(responses.calls) == 2
    assert json.loads(responses.calls[1].request.body) == expected


@responses.activate
def test_add_txt_record_error(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        json=[{
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": []
        }]
    )
    responses.add(
        responses.POST, "https://api.1cloud.ru/dns/recordtxt",
        status=400,
        json=ERROR
    )

    with pytest.raises(errors.PluginError, match=ERROR_MSG):
        onecloud.add_txt_record(RECORD_NAME, RECORD_VALUE, TTL)


def test_add_txt_record_wrong(onecloud):
    with pytest.raises(
        errors.PluginError,
        match="Unable to determine base_domain for wrong-domain."
    ):
        onecloud.add_txt_record("wrong-domain", RECORD_VALUE, TTL)


@responses.activate
def test_add_txt_record_domain_not_found(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        json=[{
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": []
        }]
    )
    with pytest.raises(
        errors.PluginError,
        match="Domain not found"
    ):
        onecloud.add_txt_record("{}.wrong-domain.org".format(SUB_DOMAIN), RECORD_VALUE, TTL)


@responses.activate
def test_add_txt_record_response_without_json(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        body="OK"
    )
    with pytest.raises(errors.PluginError):
        onecloud.add_txt_record(RECORD_NAME, RECORD_VALUE, TTL)


@responses.activate
def test_remove_txt_record(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        json=[{
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": []
        }]
    )
    host_name = "{}.".format(RECORD_NAME)
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns/1",
        json={
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": [
                {"ID": "err-0", "TypeRecord": "A",
                 "Text": RECORD_VALUE, "HostName": host_name},
                {"ID": "err-1", "TypeRecord": "TXT",
                 "Text": "some-value", "HostName": "some-name"},
                {"ID": "err-2", "TypeRecord": "TXT",
                 "Text": RECORD_VALUE, "HostName": "some-name"},
                {"ID": "err-3", "TypeRecord": "TXT",
                 "Text": "some-value", "HostName": host_name},
                {"ID": RECORD_ID, "TypeRecord": "TXT",
                 "Text": "\"{}\" ".format(RECORD_VALUE), "HostName": host_name}
            ]
        }
    )
    responses.add(
        responses.DELETE, "https://api.1cloud.ru/dns/{}/{}".format(DOMAIN_ID, RECORD_ID),
        json={"status": {"code": "1"}}
    )
    onecloud.remove_txt_record(RECORD_NAME, RECORD_VALUE)
    assert len(responses.calls) == 3


@responses.activate
def test_remove_txt_record_error_during_record_id_lookup(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        json=[{
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": []
        }]
    )
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns/1",
        status=400,
        json=ERROR
    )
    with pytest.raises(errors.PluginError):
        onecloud.remove_txt_record(RECORD_NAME, RECORD_VALUE)


@responses.activate
def test_remove_txt_record_error_during_delete(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        json=[{
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": []
        }]
    )
    host_name = "{}.".format(RECORD_NAME)
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns/1",
        json={
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": [
                {"ID": "err-0", "TypeRecord": "A",
                 "Text": RECORD_VALUE, "HostName": host_name},
                {"ID": "err-1", "TypeRecord": "TXT",
                 "Text": "some-value", "HostName": "some-name"},
                {"ID": "err-2", "TypeRecord": "TXT",
                 "Text": RECORD_VALUE, "HostName": "some-name"},
                {"ID": RECORD_ID, "TypeRecord": "TXT",
                 "Text": "\"{}\" ".format(RECORD_VALUE), "HostName": host_name}
            ]
        }
    )
    responses.add(
        responses.DELETE, "https://api.1cloud.ru/dns/{}/{}".format(DOMAIN_ID, RECORD_ID),
        status=500,
        json=ERROR
    )

    with pytest.raises(errors.PluginError):
        onecloud.remove_txt_record(RECORD_NAME, RECORD_VALUE)

    assert len(responses.calls) == 3


@responses.activate
def test_remove_txt_record_no_record(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        json=[{
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": []
        }]
    )
    host_name = "{}.".format(RECORD_NAME)
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns/1",
        json={
            "ID": DOMAIN_ID,
            "Name": DOMAIN,
            "TechName": DOMAIN,
            "State": "Active",
            "IsDelegate": "true",
            "LinkedRecords": [
                {"ID": "err-0", "TypeRecord": "A", "Text": RECORD_VALUE, "HostName": host_name},
            ]
        }
    )
    onecloud.remove_txt_record(RECORD_NAME, RECORD_VALUE)

    assert len(responses.calls) == 2


@responses.activate
def test_remove_txt_record_http_error(onecloud):
    responses.add(
        responses.GET, "https://api.1cloud.ru/dns",
        status=500,
        json={}
    )

    with pytest.raises(errors.PluginError):
        onecloud.add_txt_record(RECORD_NAME, RECORD_VALUE, TTL)
