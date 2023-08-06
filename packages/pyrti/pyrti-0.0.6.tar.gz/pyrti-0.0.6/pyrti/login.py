from pyrti.config import URL_BASE, SECRET_KEY
import requests

class Login:

    def __init__(self, url_rt, url_pesquisa, token_rt):
        url = url_rt + url_pesquisa
        self.resultado = requests.get(url, data=token_rt)

    def conectar(self):
        return self.resultado.text