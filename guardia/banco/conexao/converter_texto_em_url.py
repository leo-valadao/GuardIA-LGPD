from sqlalchemy.engine import make_url # Importa a função do SQLAlchemy que lê uma URL escrita como texto
from sqlalchemy.exc import ArgumentError # Importa o erro que o SQLAlchemy lança quando não consegue ler a URL

from guardia.banco.conexao.constantes import DRIVER # Importa o driver do PostgreSQL usado pelo GuardIA
from guardia.excecoes.banco_nao_suportado import BancoNaoSuportado # Importa o erro lançado quando o banco não é PostgreSQL
from guardia.excecoes.url_invalida import UrlInvalida # Importa o erro lançado quando a URL está mal escrita


def converter_texto_em_url(texto): # Define a função, que recebe a URL escrita como texto
    """Aceita 'postgresql://usuario@host:5432/banco' (com ou sem senha)."""
    try: # Tenta ler a URL; se não der, cai no except
        url = make_url(texto) # Lê o texto e transforma numa URL do SQLAlchemy
    except (ArgumentError, ValueError): # Se o texto não pôde ser lido como URL
        raise UrlInvalida(f'não foi possível ler "{texto}"') from None # Lança o erro de URL inválida, sem mostrar o erro técnico
    # Qualquer forma de escrever PostgreSQL na URL passa a usar o driver do GuardIA
    if url.drivername in ('postgresql', 'postgres', 'postgresql+psycopg', 'postgresql+psycopg2'): # Confere se a URL é de PostgreSQL, escrita de um desses jeitos
        url = url.set(drivername=DRIVER) # Troca o driver pelo do GuardIA
    if not url.drivername.startswith('postgresql'): # Confere se a URL não é de PostgreSQL
        raise BancoNaoSuportado(url.drivername) # Lança o erro de banco não suportado
    if not url.database: # Confere se a URL não tem o nome do banco
        raise UrlInvalida('falta o nome do banco') # Lança o erro de URL inválida
    return url # Devolve a URL pronta para usar
