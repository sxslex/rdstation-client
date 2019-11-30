# encoding: utf-8
"""Conficure test"""
import requests_mock
import pytest


@pytest.yield_fixture()
def mock_api():
    with requests_mock.Mocker() as m:
        m.get(
            'https://httpstatuses.com/401',
            status_code=401,
            json={
                'errors': {
                        'error_message': 'a field with '
                        "'api_identifier' = "
                        "'cf_my_custom_field' already "
                        'exists',
                        'error_type': 'TAKEN'}
            }
        )
        m.post(
            'https://api.rd.services/auth/token',
            status_code=200,
            json={
                'access_token': 'access_token',
                'expires_in': 86400, 'refresh_token': 'refresh_token'
            }
        )
        m.get(
            'https://api.rd.services/marketing/account_info',
            status_code=200,
            json={"name": "SlexSoft"}
        )
        m.get(
            'https://api.rd.services/marketing/tracking_code',
            status_code=200,
            json={
                'path': 'https://d335luupugsy2.cloudfront.net/js/'
                        'loader-scripts/cdadfa1b-2987e-5487-a428-7'
                        'eb92febf18b-loader.js'
            }
        )
        m.get(
            'https://api.rd.services/platform/contacts/'
            'email:sx.slex@gmail.com',
            status_code=200,
            json={
                "name": "RD Station Developer",
                "email": "sx.slex@gmail.com",
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
        )
        m.get(
            'https://api.rd.services/platform/contacts/'
            'email:contact@example.com',
            status_code=200,
            json={
                "name": "RD Station Developer",
                "email": "contact@example.com",
                "uuid": "b20da947-fbfd-4f0f-b338-fd08147d3842",
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
        )
        m.get(
            'https://api.rd.services/platform/contacts/'
            'b20da947-fbfd-4f0f-b338-fd08147d3842',
            status_code=200,
            json={
                "name": "RD Station Developer",
                "email": "contact@example.com",
                "uuid": "b20da947-fbfd-4f0f-b338-fd08147d3842",
                "job_title": "Developer",
                "bio": "This documentation explains the RD Station API.",
                "website": "https://developers.rdstation.com/",
                "linkedin": "rd_station",
                "personal_phone": "+55 48 3037-3600",
                "city": "Florian\u00f3polis",
                "state": "SC", "country": "Brasil",
                "tags": ["developer", "rdstation", "api"]
            }
        )
        m.patch(
            'https://api.rd.services/platform/contacts/'
            'email:contact@example.com',
            status_code=201,
            json={
                "name": "RD Station Developer",
                "uuid": "b20da947-fbfd-4f0f-b338-fd08147d3842",
                "job_title": "Developer",
                "bio": "This documentation explains the RD Station API.",
                "website": "https://developers.rdstation.com/",
                "linkedin": "rd_station",
                "personal_phone": "+55 48 3037-3600",
                "city": "Florian\u00f3polis",
                "state": "SC", "country": "Brasil",
                "tags": ["developer", "rdstation", "api"]
            }
        )
        m.patch(
            'https://api.rd.services/platform/contacts/'
            'uuid:b20da947-fbfd-4f0f-b338-fd08147d3842',
            status_code=201,
            json={
                "name": "RD Station Developer",
                'email': 'contact@example.com',
                "job_title": "Developer",
                "bio": "This documentation explains the RD Station API.",
                "website": "https://developers.rdstation.com/",
                "linkedin": "rd_station",
                "personal_phone": "+55 48 3037-3600",
                "city": "Florian\u00f3polis",
                "state": "SC", "country": "Brasil",
                "tags": ["developer", "rdstation", "api"]
            }
        )
        m.get(
            'https://api.rd.services/platform/contacts/fields',
            status_code=200,
            json={
                "fields": [
                    {
                        "uuid": "fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828",
                        "api_identifier": "name",
                        "custom_field": False,
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
                        "custom_field":  True,
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
        )
        m.post(
            'https://api.rd.services/platform/contacts/fields',
            status_code=201,
            json={
              "uuid": "fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828"
            }
        )
        m.patch(
            'https://api.rd.services/platform/contacts/fields/'
            'ca000da0-abc0-482a-935a-5bffab076d72',
            status_code=200,
            json={
                "uuid": "fdeba6ec-f1cf-4b13-b2ea-e93d47c0d828"
            }
        )
        m.delete(
            'https://api.rd.services/platform/contacts/fields/'
            '4dda4645-6bc1-42aa-a1f6-60602369dd05',
            status_code=204,
        )
        m.post(
            'https://api.rd.services/platform/events',
            status_code=200,
            json={'event_uuid': 'a22676ca-9f9c-48f7-91f1-61c4fd8b24d5'}
        )
        yield m
