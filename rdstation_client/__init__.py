# -*- coding: utf-8 -*-
# https://developers.rdstation.com/en/overview
"""Client for access API rdstation."""

__version__ = '0.0.10'

from .utils import encode_all_unicode
from .errors import (
    ExceptionRDStationClient,
    ExceptionRDStationClientCreateCode,
    ExceptionRDStationClientResponse
)
import requests
import pprint
import json


# try:
#     FileNotFoundError
# except NameError:
#     FileNotFoundError = IOError


MSG_FILE_CONF = (
    'Please import the file path "file_auth"'
)

MSG_ERROR = (
    'Please fill in the configuration file for API access '
    'with the required data.\n'
    'For more details on how to have these values visit the link: '
    'https://developers.rdstation.com/en/overview'
)
MSG_CREATE_TOKEN = (
    'Visit the link below with the RDStation account '
    'to get the CODE that will be in the URL. '
    'https://app.rdstation.com.br/api/'
    'platform/auth?client_id=%(client_id)s'
    '&redirect_url=%(redirect_url)s'
)

my_input = input


class RDStationClient:

    def __init__(
        self,
        file_auth=None,
        log=False,
        console_input=True
    ):
        if not file_auth:
            raise ExceptionRDStationClient(MSG_FILE_CONF + '\n' + MSG_ERROR)
        self.file_auth = file_auth
        self.log = log
        self.client_id = None
        self.client_secret = None
        self.code = None
        self.access_token = None
        self.refresh_token = None
        self.redirect_url = None
        self.console_input = console_input

    def _saving_params(self):
        f = open(self.file_auth, 'w')
        f.write(json.dumps(dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=self.code,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            redirect_url=self.redirect_url
        ), indent=True, sort_keys=True))
        f.close()

    def _loading_params(self):
        try:
            f = open(self.file_auth, 'r')
            params = json.loads(f.read().strip())
            self.client_id = params['client_id']
            self.client_secret = params['client_secret']
            self.code = params.get('code')
            self.access_token = params.get('access_token')
            self.refresh_token = params.get('refresh_token')
            self.redirect_url = params.get('redirect_url')
            f.close()
        except IOError:
            self.client_id = 'client_id'
            self.client_secret = 'client_secret'
            self.code = 'code'
            self.access_token = 'access_token'
            self.refresh_token = 'refresh_token'
            self.redirect_url = 'https://appname.org/auth/callback'
            self._saving_params()
            raise ExceptionRDStationClient(MSG_ERROR)

    def _create_token(self, deep=False):
        headers = {
            'Content-Type': 'application/json',
        }
        params = dict(
            client_secret=self.client_secret,
            client_id=self.client_id,
        )
        if self.refresh_token is None:
            params['code'] = self.code
        else:
            params['refresh_token'] = self.refresh_token
        data = json.dumps(params)
        _response = requests.post(
            'https://api.rd.services/auth/token',
            headers=headers, data=data
        )
        if self.log:
            print('POST /auth/token')
            pprint.pprint(params)
            pprint.pprint(_response.json())
        if _response.status_code != 200:
            if self.refresh_token:
                self.refresh_token = None
                return self._create_token()
            msg = MSG_CREATE_TOKEN % dict(
                client_id=self.client_id, redirect_url=self.redirect_url
            )
            if not self.console_input or deep:
                raise ExceptionRDStationClientCreateCode(msg)
            self.code = str(my_input(msg + '\n Enter CODE: '))
            return self._create_token(deep=True)
        data = encode_all_unicode(_response.json())
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self._saving_params()

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.access_token,
        }

    @staticmethod
    def _get_json_response_200s(response):
        if response.status_code == 204:
            return {}
        if int(response.status_code / 100) == 2:
            return encode_all_unicode(response.json())
        raise ExceptionRDStationClientResponse(
            response.content.decode()
        )

    def _request(self, method, url, **kwargs):
        if self.client_id is None:
            self._loading_params()
        if self.access_token is None:
            self._create_token()
        kwargs['headers'] = self._get_headers()
        response = requests.request(method, url, **kwargs)
        if self.log:
            print('{} {}'.format(method, url))
            try:
                pprint.pprint(kwargs)
                print(response.status_code)
                pprint.pprint(encode_all_unicode(response.json()))
            except Exception:
                pass
        if response.status_code in (401, 402, 403, 404):
            self._create_token()
            kwargs['headers'] = self._get_headers()
            if self.log:
                print('{} {}'.format(method, url))
            response = requests.request(method, url, **kwargs)
        return response

    def _get(self, uri):
        response = self._request(
            'get',
            'https://api.rd.services/%s' % uri
        )
        return self._get_json_response_200s(response)

    def _delete(self, uri):
        response = self._request(
            'delete',
            'https://api.rd.services/%s' % uri
        )
        return self._get_json_response_200s(response)

    def _patch(self, uri, data=None):
        response = self._request(
            'patch',
            'https://api.rd.services/%s' % uri,
            data=json.dumps(data) if data else None
        )
        return self._get_json_response_200s(response)

    def _post(self, uri, data=None):
        response = self._request(
            'post',
            'https://api.rd.services/%s' % uri,
            data=json.dumps(data) if data else None
        )
        return self._get_json_response_200s(response)

    def _put(self, uri, data=None):
        response = self._request(
            'put',
            'https://api.rd.services/%s' % uri,
            data=json.dumps(data) if data else None
        )
        return self._get_json_response_200s(response)

    # Available methods
    def account_info_get(self):
        """
        Available methods
        Returns the account name from your RD Station Marketing account.
        Vide: https://developers.rdstation.com/pt-BR/reference/account_infos
            # get_account_info
        :return: dict
            {"name": "Account Name"}
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.account_info_get().get('name'))
        """
        return self._get('marketing/account_info')

    def tracking_code_get(self):
        """
        Available methods
        Returns the RD Station Marketing tracking code so it can be embedded
            on websites or CMS.
        Vide: https://developers.rdstation.com/en/reference/account_infos
            # get_tracking_code
        :return: dict
            {
              "path": "https://d335luupugsy2.cloudfront.net/js/loader-s"
                      "cripts/8d2892c6-e22c-2c2d-b15a-36916776e5e7-loader.js"
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.tracking_code_get().get('path'))
        """
        return self._get('marketing/tracking_code')

    # Contacts

    def contacts_get_by_uuid(self, uuid):
        """
        Returns data about a specific Contact
        Vide: https://developers.rdstation.com/en/reference/contacts#get_uuid
        :return: dict
            {
              "name": "RD Station Developer",
              "email": "contact@example.com",
              "job_title": "Developer",
              "bio": "This documentation explains the RD Station API.",
              "website": "https://developers.rdstation.com/",
              "linkedin": "rd_station",
              "personal_phone": "+55 48 3037-3600",
              "city": "Florianópolis",
              "state": "SC",
              "country": "Brasil",
              "tags": ["developer", "rdstation", "api"],
              "extra_emails": ["contact2@example.com"],
              "cf_custom_field_2": "custom field value2"
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.contacts_get_by_uuid('123-456-456-456-465'))
        """
        return self._get('platform/contacts/%s' % uuid)

    def contacts_get_by_email(self, email):
        """
        Returns data about a specific Contact
        Vide: https://developers.rdstation.com/en/reference/contacts#get_email
        :return: dict
            {
              "name": "RD Station Developer",
              "email": "contact@example.com",
              "job_title": "Developer",
              "bio": "This documentation explains the RD Station API.",
              "website": "https://developers.rdstation.com/",
              "linkedin": "rd_station",
              "personal_phone": "+55 48 3037-3600",
              "city": "Florianópolis",
              "state": "SC",
              "country": "Brasil",
              "tags": ["developer", "rdstation", "api"],
              "extra_emails": ["contact2@example.com"],
              "cf_custom_field_2": "custom field value2"
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.contacts_get_by_email('sx.slex@gmail.com'))
        """
        return self._get('platform/contacts/email:%s' % email)

    def contacts_patch(self, contact):
        """
        Updates the properties of a Contact.
        Vide: https://developers.rdstation.com/en/reference/contacts#patch
        :return: dict
            {
              "name": "RD Station Developer",
              "email": "contact@example.com",
              "job_title": "Developer",
              "bio": "This documentation explains the RD Station API.",
              "website": "https://developers.rdstation.com/",
              "linkedin": "rd_station",
              "personal_phone": "+55 48 3037-3600",
              "city": "Florianópolis",
              "state": "SC",
              "country": "Brasil",
              "tags": ["developer", "rdstation", "api"],
              "extra_emails": ["contact2@example.com"],
              "cf_custom_field_2": "custom field value2"
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.contacts_patch(
                {
                    "name": "RD Station Developer",
                    "email": "contact@example.com",
                    "job_title": "Developer",
                    "bio": "This documentation explains the RD Station API.",
                    "website": "https://developers.rdstation.com/",
                    "linkedin": "rd_station",
                    "personal_phone": "+55 48 3037-3600",
                    "city": "Florianópolis",
                    "state": "SC",
                    "country": "Brasil",
                    "tags": ["developer", "rdstation", "api"]
                }
            ))
        """
        email = None
        uuid = None
        if 'uuid' in contact:
            uuid = contact.pop('uuid')
        else:
            email = contact.pop('email')
        return self._patch(
            'platform/contacts/' + (
                ('email:%s' % email) if email
                else ('uuid:%s' % uuid)
            ),
            contact
        )

    # Funnels

    def funnels_get(self, contact, funnel_name="default"):
        """
        Returns a list of Funnels associated to the given contact.
        Currently only a single funnel called default is supported.

        See: https://developers.rdstation.com/en/reference/contacts/funnels#methodGetByUuidDetails
        and https://developers.rdstation.com/en/reference/contacts/funnels#methodGetByEmailDetails
        :return: dict
            {
                "lifecycle_stage": "Lead",
                "opportunity": false,
                "contact_owner_email": "",
                "fit": 60,
                "interest": 10
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.funnels_get({'email': 'contact@email.com'}, 'default'))
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.funnels_get(
                {'uuid': 'b20da947-fbfd-4f0f-b338-fd08147d3842'}, 'default'))
        """
        email = None
        uuid = None

        if 'uuid' in contact:
            uuid = contact['uuid']
        else:
            email = contact['email']

        return self._get(
            'platform/contacts/' +
            (('email:%s' % email if email else ('uuid:%s' %
                                                uuid)) + ("/funnels/%s" % funnel_name))
        )

    def funnels_put(self,
                    contact={'lifecycle_stage': 'Lead',
                             'opportunity': False, 'contact_owner_email': ''},
                    funnel_name="default"):
        """
        Updates the funnel information about the current contact.
        See: https://developers.rdstation.com/en/reference/contacts/funnels#methodPatchDetails
        :return: dict
            {
                "lifecycle_stage": "Qualified Lead",
                "opportunity": true,
                "contact_owner_email": "",
                "fit": 60,
                "interest": 10,
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            rdsc.funnels_put({
                # either email or uuid can be used
                'email': 'contact@example.com',
                'lifecycle_stage': 'Qualified Lead',
                'opportunity': True,
                'contact_owner_email': ''
            })
        """

        email = None
        uuid = None

        if 'uuid' in contact:
            uuid = contact['uuid']
        else:
            email = contact['email']

        return self._put(
            'platform/contacts/' +
            (('email:%s' % email if email else ('uuid:%s' %
                                                uuid)) + ("/funnels/%s" % funnel_name)),
            contact
        )

    # Fields

    def fields_get(self):
        """
        Returns a list of Fields and their attributes from the current account.
        A field can be either default or custom, as follow:
            Default fields are standard fields that represent RD Station's
            Contact's basic information.
            Custom fields are fields that represent unique Contact's
            information accordingly to your organization and that were
            created by RD Station's users.
        Vide: https://developers.rdstation.com/en/reference/fields#field-get
        :return: dict
            {
              "fields": [
                {
                  "uuid": "fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828",
                  "api_identifier": "name",
                  "custom_field": false,
                  "data_type": "STRING",
                  "name": {
                    "default": "nome",
                    "pt-BR": "nome"
                  },
                  "label": {
                    "default": "Nome completo",
                    "pt-BR": "Nome completo"
                  },
                  "presentation_type": "TEXT_INPUT",
                  "validation_rules": {}
                },
                {
                  "uuid": "f0a3dd8a-f044-432c-a1ce-1bb559d6edf4",
                  "api_identifier": "cf_language",
                  "custom_field":  true,
                  "data_type": "STRING[]",
                  "name": {
                    "default": "Idioma",
                    "pt-BR": "Idioma"
                  },
                  "label": {
                    "default": "Selecione o idioma",
                    "pt-BR": "Selecione o idioma"
                  },
                  "presentation_type": "CHECK_BOX",
                  "validation_rules": {
                    "valid_options": [
                      {
                        "value": "Português",
                        "label": {
                          "default": "Português",
                          "pt-BR": "Português"
                        }
                      },
                      {
                        "value": "Inglês",
                        "label": {
                          "default": "Inglês",
                          "pt-BR": "Inglês"
                        }
                      },
                      {
                        "value": "Espanhol",
                        "label": {
                          "default": "Espanhol",
                          "pt-BR": "Espanhol"
                        }
                      }
                    ]
                  }
                }
              ]
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            fields = rdsc.fields_get()['fields']
            print(fields)
            print(print([0]['api_identifier'])
        """
        return self._get('platform/contacts/fields')

    def fields_post(self, field):
        """
        Creates a Field for the current account.
        :param field:
        Vide: https://developers.rdstation.com/en/reference/fields#field-post
        :return: dict
            {
              "uuid": "fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828"
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.fields_post(
                {
                  "name": {
                    "pt-BR": "Meu campo customizado"
                  },
                  "label": {
                    "pt-BR": "Selecione uma das opções"
                  },
                  "api_identifier": "cf_my_custom_field",
                  "data_type": "STRING",
                  "presentation_type": "COMBO_BOX",
                  "validation_rules": {
                    "valid_options": [
                      {
                        "value": "opcao_1",
                        "label": {
                          "pt-BR": "opcao_1"
                        }
                      },
                      {
                        "value": "opcao_2",
                        "label": {
                          "pt-BR": "opcao_2"
                        }
                      }
                    ]
                  }
                }
            ))
        """
        return self._post(
            'platform/contacts/fields',
            field
        )

    def fields_path(self, field):
        """
        Updates a Field for the current account. It supports partial updates.
        :param field:
        Vide: https://developers.rdstation.com/en/reference/fields#field-patch
        :return: dict
            {
              "uuid": "fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828"
            }
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.fields_path(
                {
                  "uuid": "fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828",
                  "name": {
                    "pt-BR": "Meu campo customizado"
                  },
                  "label": {
                    "pt-BR": "Selecione uma das opções"
                  },
                  "api_identifier": "cf_my_custom_field",
                  "data_type": "STRING",
                  "presentation_type": "COMBO_BOX",
                  "validation_rules": {
                    "valid_options": [
                      {
                        "value": "opcao_1",
                        "label": {
                          "pt-BR": "opcao_1"
                        }
                      },
                      {
                        "value": "opcao_2",
                        "label": {
                          "pt-BR": "opcao_2"
                        }
                      }
                    ]
                  }
                }
            ))
        """
        uuid = field.pop('uuid')
        return self._patch(
            'platform/contacts/fields/%s' % uuid,
            field
        )

    def fields_delete(self, uuid):
        """
        Deletes a Field from the current account.
        :param uuid:
        Vide: https://developers.rdstation.com/en/reference/fields#delete
        :return: {}
        :Example:
            rdsc = RDStationClient('/home/var/rdstation_client.json')
            print(rdsc.fields_delete("fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828"))
        """
        return self._delete(
            'platform/contacts/fields/%s' % uuid,
        )

    # TODO: Webhooks
    # def integrations_webhooks_get(self):
    #     return self._get_json_response_200s(response)

    # Events
    def events_post(self, event):
        return self._post(
            'platform/events',
            event
        )
