from pyrti.login import Login
from pyrti.config import URL_BASE, SECRET_KEY

variavel = None

def main():
    
    url_rt = URL_BASE

    url_pesquisa = 'users?query=[{"field":"Name","operator":"=", "value":"root"}]'

    token_rt = {'token':SECRET_KEY}

    variavel = Login(url_rt, url_pesquisa, token_rt)

    resposta = variavel.conectar()

    print('O resultado da pesquisa é: \n {}'.format(resposta))
    

if __name__ == "__main__":
    main()
