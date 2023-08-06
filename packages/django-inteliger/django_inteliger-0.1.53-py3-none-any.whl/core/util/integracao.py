import unicodedata

import requests
import json
import core.log.models


class Integracao:
    def __init__(self, url=None, body=None, headers=None, servico=None, request=None):
        self.url = url
        self.body = body
        self.headers = headers
        self.response = None
        self.servico = servico
        self.status_code = None
        self.tipo = None
        self.request = request

    def salvar(self):
        nova_integracao = core.log.models.ClienteIntegracao(
            servico=self.servico,
            url=self.url,
            body=self.body,
            headers=self.headers,
            response=self.response,
            status_code=self.status_code,
            tipo=self.tipo
        )
        nova_integracao.save(request_=self.request)
        return True

    def tratar_campo(self, campo=None):
        if isinstance(campo, str) and campo is not None:
            campo = unicodedata.normalize('NFD', campo)
        return campo if campo is not None else ''

    def post(self):
        data = json.dumps(self.body, ensure_ascii=False)
        data = unicodedata.normalize('NFD', data).encode('ASCII', 'ignore')
        resposta = requests.post(self.url, data=data, headers=self.headers)
        self.response = resposta.content
        self.status_code = resposta.status_code
        self.salvar()

    def get(self):
        resposta = requests.get(self.url, headers=self.headers, data=self.body)
        self.response = resposta.content
        self.status_code = resposta.status_code
        self.salvar()

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    @url.deleter
    def url(self):
        del self.__url

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, value):
        self.__body = value if value is not None else {}

    @body.deleter
    def body(self):
        del self.__body

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        self.__headers = value if value is not None else {'Content-type': 'application/json'}

    @headers.deleter
    def headers(self):
        del self.__headers

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, value):
        self.__response = value

    @response.deleter
    def response(self):
        del self.__response

    @property
    def servico(self):
        return self.__servico

    @servico.setter
    def servico(self, value):
        self.__servico = value

    @servico.deleter
    def servico(self):
        del self.__servico

    @property
    def status_code(self):
        return self.__status_code

    @status_code.setter
    def status_code(self, value):
        self.__status_code = value

    @status_code.deleter
    def status_code(self):
        del self.__status_code

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, value):
        self.__tipo = value

    @tipo.deleter
    def tipo(self):
        del self.__tipo

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, value):
        self.__request = value

    @request.deleter
    def request(self):
        del self.__request