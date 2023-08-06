"""DNS Authenticator for ONECLOUD."""

import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common

from .client import OneCloudClient


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for ONECLOUD

    This Authenticator uses the ONECLOUD API to fulfill a dns-01 challenge.
    """

    description = (
        "Obtain certificates using a DNS TXT record "
        "(if you are using onecloud for DNS)."
    )
    ttl = 300

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)

        self.client = OneCloudClient()

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds=10):
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="ONECLOUD credentials INI file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond "
            "to a dns-01 challenge using the ONECLOUD API."
        )

    def _setup_credentials(self):
        credentials = self._configure_credentials(
            "credentials",
            "ONECLOUD credentials INI file",
            {
                "api-token": "API Token for ONECLOUD account"
            }
        )
        self.client.set_token(
            credentials.conf("api-token")
        )

    def _perform(self, domain, validation_name, validation):
        self.client.add_txt_record(validation_name, validation, self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        self.client.remove_txt_record(validation_name, validation)
