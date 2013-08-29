#coding=utf-8
import textveloper as tv
import unittest
import simplejson
from mock import patch

class AccountManagerTest(unittest.TestCase):
    def setUp(self):
        self.account_manager = tv.AccountManager('mytokentest')

    @patch('textveloper.requests')
    def test_consultar_puntos(self, mock_requests):
        mocked_response = {
                "transaccion":"exitosa",
                "puntos_enviados":"100",
                "total_puntos":"1000",
                "puntos_disponibles":"900" 
            }
        mock_requests.post.return_value.content = simplejson.dumps(mocked_response)

        response = self.account_manager.consultar_puntos()

        self.assertEquals(response, mocked_response)

    def test_api_subcuenta(self):
        response = self.account_manager.api_subcuenta('sub_token')
        self.assertEquals(str(type(response)), '<class \'textveloper.API\'>')


class APITest(unittest.TestCase):
    def setUp(self):
        am = tv.AccountManager('token')
        self.api = am.api_subcuenta('sub_token')

    @patch('textveloper.requests')
    def test_enviar_mensaje(self, mock_requests):
        mocked_response = {'mensaje_transaccion': 'MENSAJE_ENVIADO', 'transaccion': 'exitosa'}
        mock_requests.post.return_value.content = simplejson.dumps(mocked_response)

        response = self.api.enviar_mensaje("04125559988", "Foo bar baz")

        self.assertEquals(mocked_response, response)
    
    @patch('textveloper.requests')
    def test_consultar_puntos_app(self, mock_requests):
        mocked_response = {
                "transaccion":"exitosa",
                "puntos_enviados":"100",
                "total_puntos":"1000",
                "puntos_disponibles":"900" 
            }
        mock_requests.post.return_value.content = simplejson.dumps(mocked_response)

        response = self.api.consultar_puntos()

        self.assertEquals(mocked_response, response)

    @patch('textveloper.requests')
    def test_historial_transferencias(self, mock_requests):
        mocked_response = {
                'historico': [
                    {
                        'cantidad': '20',
                        'codigo_transaccion': '10',
                        'fecha': '2013-08-24 19:10:08'
                    },
                    {
                        'cantidad': '1',
                        'codigo_transaccion': '11',
                        'fecha': '2013-08-28 23:17:07'
                    }
                ],
                'transaccion': 'exitosa'
            }

        mock_requests.post.return_value.content = simplejson.dumps(mocked_response)

        response = self.api.historial_transferencias()

        self.assertEquals(mocked_response, response)

    @patch('textveloper.requests')
    def test_historial_mensajes(self, mock_requests):
        mocked_response = {
            'historico': [
                {
                    'codigo_log': '67',
                    'estatus': 'Enviado',
                    'fecha': '2013-08-24 19:16:51',
                    'mensaje': 'ola ke ase?',
                    'telefono': '04241017107'
                },
                {
                    'codigo_log': '68',
                    'estatus': 'Enviado',
                    'fecha': '2013-08-24 19:25:36',
                    'mensaje': 'Hola gente, es Israel',
                    'telefono': '04142454597'
                }
            ],
            'transaccion': 'exitosa'
        }

        mock_requests.post.return_value.content = simplejson.dumps(mocked_response)

        response = self.api.historial_mensajes()

        self.assertEquals(mocked_response, response)



if __name__ == '__main__':
    unittest.main()
