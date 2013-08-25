#coding=utf-8
# Programado por:
#    Israel Fermín Montilla <iferminm@gmail.com>
from .metaclasses import Singleton
import simplejson
import requests


class Textveloper(object):
    api_url = 'http://api.textveloper.com/{0}/'


class API(Textveloper):
    """
    Implementación del API para sub-cuentas
    de Textveloper
    """
    def __init__(self, cuenta_token, sub_token):
        super(API, self).__init__()
        self.account_token = cuenta_token
        self.token = sub_token
        
    def enviar_mensaje(self, telefono, mensaje):
        """docstring for enviar_mensaje"""
        payload = {
            'cuenta_token': self.account_token,
            'subcuenta_token': self.token,
            'telefono': telefono,
            'mensaje': mensaje
        }
        request_url = self.api_url.format('enviar')
        response = requests.post(request_url, data=payload)
        return response

    def enviar_mensaje_masivo(self, telefonos, mensaje):
        """
        docstring
        """
        responses = {}.fromkeys(telefonos)
        for telefono in telefonos:
            responses[telefono] = self.enviar_mensaje(telefono, mensaje)

        return responses

    def consultar_puntos(self):
        """docstring for consultar_puntos"""
        payload = {
            'cuenta_token': self.account_token,
            'subcuenta_token': self.token
        }
        request_url = self.api_url.format('saldo-subcuenta')
        response = requests.post(request_url, data=payload)
        return eval(response.content)

    def historial_transferencias(self):
        """docstring for historial_transferencias"""
        payload = {'cuenta_token': self.token}
        request_url = self.api_url.format('historial-transferencias')
        response = requests.post(request_url, data=payload)

        return simplejson.loads(response.content)

    def historial_mensajes(self):
        """
        docstring
        """
        payload = {'cuenta_token': self.account_token}
        request_url = self.api_url.format('historial-envios')
        response = requests.post(request_url, data=payload)

        return simplejson.loads(response.content)


class AccountManager(Textveloper):
    """
    Clase que interactúa con el api para envío de 
    mensajes de texto
    """
    __metaclass__ = Singleton

    def __init__(self, cuenta_token, registro_subcuentas=False):
        super(Textveloper, self).__init__()
        self.token = cuenta_token
        self.memoizing = registro_subcuentas
        self.sub_accounts = {}

    def api_subcuenta(self, sub_token):
        if self.memoizing: 
            if sub_token not in self.sub_accounts.keys():
                self.sub_accounts[sub_token] = API(cuenta_token=self.token, sub_token=sub_token)

            return self.sub_accounts[sub_token]

        return API(cuenta_token=self.token, sub_token=sub_token)

    def consultar_puntos(self):
        """docstring for saldo_cuenta"""
        payload = {'cuenta_token': self.token}
        request_url = self.api_url.format('saldo-cuenta')
        response = requests.post(request_url, data=payload)
        return eval(response.content)

    def historial_compras(self):
        """docstring for historial_transferencias"""
        payload = {'cuenta_token': self.token}
        request_url = self.api_url.format('historial-compras')
        response = requests.post(request_url, data=payload)
        return simplejson.loads(response.content)
