import os

INVALID_CREDENTIALS = "Usuário ou senha inválidos!"
UNAUTHORIZED = "Não autorizado. Não há sessão para esse usuário!"
TOKEN_ERROR = 'Essa requisição precisa do token JWT'
UNKNOW_ERROR = "Erro desconhecido"
SECRET = os.environ.get('SECRET', "secret")
LOGOUT_ERROR = "Ocorreu um erro ao tentar deslogar!"
UNFOLLOW_ERROR = "Ocorreu um problema na hora de parar de seguir o usuário!"
FOLLOW_ERROR = "Ocorreu um problema na hora de seguir o usuário!"
SEND_CODE = "Use a mutation sendCode para inserir o código de segurança!"
