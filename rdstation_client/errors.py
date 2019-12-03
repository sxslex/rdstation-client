# -*- coding: utf-8 -*-
import json
import pprint
from .utils import encode_all_unicode


class ExceptionRDStationClient(Exception):
    pass


class ExceptionRDStationClientCreateCode(ExceptionRDStationClient):
    pass


class ExceptionRDStationClientResponse(ExceptionRDStationClient):
    def __init__(self, message, response_obj=None):
        self.response_obj = response_obj or {}
        self.message = message
        try:
            self.response_obj = encode_all_unicode(json.loads(message))
            errors = self.response_obj['errors']
            error_message = errors.get('error_message')
            if error_message:
                self.message = error_message
            api_identifier = errors.get('api_identifier')
            if api_identifier:
                if isinstance(api_identifier, list):
                    self.message = '\n'.join(
                        [i.get('error_message') for i in api_identifier]
                    )
        except Exception:
            pass
        # try:
        #     super().__init__(self.message)
        # except Exception:
        super(self.__class__, self).__init__(self.message)

    def __repr__(self):
        return 'ExceptionRDStationClientResponse(%s, %s)' % (
            (
                '"%s"' % ('\n'.join(self.message))
                if isinstance(self.message, list)
                else pprint.pformat(self.message)
            ),
            pprint.pformat(self.response_obj)
        )

    def __str__(self):
        return self.__repr__()
