from sqlalchemy.engine import URL # Importa a classe do SQLAlchemy que representa uma URL de conexão

from guardia.banco.conexao.constantes import DRIVER, PORTA_PADRAO # Importa o driver do PostgreSQL e a porta padrão
from guardia.excecoes.dados_de_conexao_invalidos import DadosDeConexaoInvalidos # Importa o erro lançado quando os dados de conexão são inválidos


def montar_url(host, banco, usuario, porta=PORTA_PADRAO, senha=None):
    """Monta a URL de conexão do PostgreSQL; valida banco, usuário e porta."""
    if not banco or not usuario: # Confere se faltou o nome do banco ou o usuário
        raise DadosDeConexaoInvalidos('o banco e o usuário são obrigatórios.') # Lança o erro de dados de conexão inválidos
    try: # Tenta transformar a porta em número; se não der, cai no except
        porta = int(porta) # Transforma a porta em número inteiro
    except (TypeError, ValueError): # Se a porta não era um número
        raise DadosDeConexaoInvalidos(f'a porta precisa ser um número (foi informado "{porta}").') from None # Lança o erro de dados de conexão inválidos, sem mostrar o erro técnico
    return URL.create(DRIVER, username=usuario, password=senha, host=host, port=porta, database=banco) # Monta e devolve a URL de conexão
