import os

INVALID_CREDENTIALS_ERROR = "Usuário ou senha inválidos!"
UNAUTHORIZED_ERROR = "Não autorizado. Não há sessão para esse usuário!"
UNAUTHORIZED_CHALLENGE_ERROR = "Não autorizado. Não há autorização pendente para esse token!"
TOKEN_ERROR = 'Essa requisição precisa do token JWT'
UNKNOW_ERROR = "Erro desconhecido"
SECRET = os.environ.get('SECRET', "secret")
LOGOUT_ERROR = "Ocorreu um erro ao tentar deslogar!"
UNFOLLOW_ERROR = "Ocorreu um problema na hora de parar de seguir o usuário!"
FOLLOW_ERROR = "Ocorreu um problema na hora de seguir o usuário!"
SEND_CODE = "Use a mutation sendCode para inserir o código de segurança!"
LOGIN_SUCCESS = "Logado com sucesso!"
CHALLENGE_REQUIRED = "Autorização pendente! Use a mutation sendCodeChallenge para inserir o código de segurança!"
BASE_URL = 'https://www.instagram.com/'
INVALID_TOKEN = 'Token inválido!'
CODE_ERROR = 'Código errado. Verifique o código que enviamos para você e tente novamente.'
LOGOUT_SUCCESS = "Deslogado com sucesso!"
UNFOLLOW_SUCCESS = "Você parou de seguir!"
FOLLOW_SUCCESS = "Você começou a seguir!"
