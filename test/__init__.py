#############################################################################
##             _____            __ _      _            _                   ##
##            / ____|          / _(_)    (_)          | |                  ##
##           | |     ___   ___| |_ _  ___ _  ___ _ __ | |_ ___             ##
##           | |    / _ \ / _ \  _| |/ __| |/ _ \ '_ \| __/ _ \            ##
##           | |___| (_) |  __/ | | | (__| |  __/ | | | ||  __/            ##
##            \_____\___/ \___|_| |_|\___|_|\___|_| |_|\__\___|            ##
##                                                                         ##
##    Coeficiente Sistemas Ltda. - © 2021. Todos os direitos reservados.   ##
##                                                                         ##
#############################################################################
import os
import unittest
from abc import ABC
from datetime import date
from datetime import datetime
from typing import Union
from urllib.parse import urlencode

from requests import request
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv

#import settings

load_dotenv()

from os import environ as env


class APITest(ABC, unittest.TestCase):
    """ Classe responsável pela base de testes. """

    currentResult = None
    header_token:str = None

    request_history = {}
    meta_data = {
    }
    test_data = {
        'date': date.today()
    }

    amount = 0
    errors = []
    failures = []
    skipped = []
    multipart_files = []

    def __init__(self, test):
        super(APITest, self).__init__(test)

    @classmethod
    def setUpClass(cls):

        if not cls.header_token:
            #TODO: Buscar token header
            pass

    """
    @classmethod
    def request_file(cls, file_location):

        addr = settings.DIR_BASE / file_location
        name = os.path.basename(addr)
        file = open( addr , 'rb')

        cls.multipart_files.append(file)

        return (name, file)
    """

    @classmethod
    def multipart(cls, payload):
        return MultipartEncoder(payload)

    @classmethod
    def request(cls,
                url: str,
                method: str = 'GET',
                query: Union[dict, str] = '',
                payload: dict = {},
                as_multipart:bool=False,
                as_json: bool = True):
        """
        Dispara request para o servidor local.
        :param handler:
        :param method:
        :param query:
        :param payload:
        :param payload_type: tipo de payload a ser enviado
        :param as_json: retorna resposta dado como json.
        :return:
        """

        if query:
            """ Reescreve a query como string.
            """
            query = '?%s' % urlencode(query)

        uri = url
        url = f'{env["WSGI_PROTOCOL"]}://' \
              f'{env["WSGI_HOST"]}:' \
              f'{env["WSGI_PORT"]}/' \
              f'{uri}{query}'

        print('[TEST] -- URL ', url)

        req_data = dict(
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Token {cls.header_token}'
            }
        )

        payload_type = 'json'

        if as_multipart:
            payload_type = 'data'
            req_data['headers']['Content-Type'] = payload.content_type

        if method != 'GET':  # Incrementa body à requisição.
            req_data[payload_type] = payload

        response = request(
            method=method,
            url=url,
            **req_data,
        )

        print('[TEST] -- STATUS', response.status_code)

        if as_json:
            data = response.json()

            print('[TEST] -- data', data)
            cls.meta_data[uri] = data

            return (data, response.status_code)

        return response

    @classmethod
    def setResult(cls, amount, errors, failures, skipped):
        # https://stackoverflow.com/questions/28500267/python-unittest-count-tests?noredirect=1&lq=1
        cls.amount, cls.errors, cls.failures, cls.skipped = \
            amount, errors, failures, skipped

    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        print(
            f'\n{"-" * 77}\n',
            self._testMethodName, amount,
            len(errors), len(failures), len(skipped),
            f'\n{"=" * 77}\n',
        )
        self.setResult(amount, errors, failures, skipped)

    @classmethod
    def tearDownClass(cls):
        """

        :return:
        """

        for f in cls.multipart_files:
            f.close()

    def run(self, result=None):
        self.currentResult = result
        unittest.TestCase.run(self, result)

    def setUp(self):
        """

        :return:
        self.server = WSGIApplicationTester()
        with self.server.client() as c:
            response = c.post('/?method=getTokenAuthorization',
                              data=json.dumps(
                                  app_env.TEST_AUTHORIZATION_PAYLOAD),
                              content_type='application/json')
            data = json.loads(response.data)
            # para cada request um novo token
            self.token = data['token']
        """

    def __str__(self):
        return "method_handler: %s" % (
            '_'.join(self._testMethodName.split('test_')[-1].rsplit('_')[1:])
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)

# end-of-file