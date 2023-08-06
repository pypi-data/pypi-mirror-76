ONECLOUD DNS Authenticator plugin for Certbot
---------------------------------------------

Use the certbot client to generate a certificate using onecloud.

Prepare an API Token
====================
Fetch an api token by instruction on https://1cloud.ru/api/auth/auth


Install certbot and plugin
==========================

.. code-block:: bash

    pip install certbot-dns-onecloud


Create a credentials file
=========================

.. code-block:: ini

    certbot_dns_onecloud:dns_onecloud_api_token = "ONECLOUD-API-TOKEN"


Generate a certificate
======================

.. code-block:: bash

    certbot certonly -a certbot-dns-onecloud:dns-onecloud \
        [--certbot-dns-onecloud:dns-onecloud-credentials PATH-TO-CREDENTIAL-FILE]
        -d REPLACE-WITH-YOUR-DOMAIN
