from guardia.enumeracoes.forca_do_padrao import ForcaDoPadrao # Importa o enum com as forças do padrão (forte ou fraco)
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.modelos.padrao_de_deteccao import PadraoDeDeteccao # Importa a classe que guarda as regras de um tipo de dado


# Quadro 2 do artigo: tipo → Expressão Regular, Força, Peso (W) e Termos de Contexto
PADROES_DE_DETECCAO = { # Cria o dicionário: cada tipo de dado pessoal e as regras para reconhecê-lo
    # Tipo de Dado                        Expressão Regular                                          Força                Peso  Termos de contexto
    TipoDeDadoPessoal.CPF:                PadraoDeDeteccao(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}',          ForcaDoPadrao.FORTE, 3,    'cpf'), # Regras do CPF
    TipoDeDadoPessoal.RG:                 PadraoDeDeteccao(r'\d{1,2}\.?\d{3}\.?\d{3}-?[\dXx]',       ForcaDoPadrao.FRACO, 3,    'rg'), # Regras do RG
    TipoDeDadoPessoal.EMAIL:              PadraoDeDeteccao(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+',          ForcaDoPadrao.FORTE, 3,    ('email', 'mail')), # Regras do e-mail
    TipoDeDadoPessoal.DATA_DE_NASCIMENTO: PadraoDeDeteccao(r'\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}',   ForcaDoPadrao.FRACO, 2,    ('nasc', 'aniversario')), # Regras da data de nascimento
    TipoDeDadoPessoal.TELEFONE:           PadraoDeDeteccao(r'\(?\d{2}\)?\s?9?\d{4}-?\d{4}',          ForcaDoPadrao.FRACO, 2,    ('tel', 'celular', 'fone', 'whatsapp')), # Regras do telefone
    TipoDeDadoPessoal.NOME:               PadraoDeDeteccao(None,                                     ForcaDoPadrao.FRACO, 1,    'nome'), # Regras do nome de pessoa (não tem expressão regular)
    TipoDeDadoPessoal.CEP:                PadraoDeDeteccao(r'\d{5}-?\d{3}',                          ForcaDoPadrao.FRACO, 1,    'cep'), # Regras do CEP

    # Dados pessoais SENSÍVEIS (Art. 5º, II): Tipo Sanguíneo = dado referente à saúde / genético
    TipoDeDadoPessoal.TIPO_SANGUINEO:     PadraoDeDeteccao(r'(?:AB|A|B|O)\s?[+-]',                   ForcaDoPadrao.FRACO, 3,    'sangu',  sensivel=True), # Regras do tipo sanguíneo
    TipoDeDadoPessoal.FILIACAO_SINDICAL:  PadraoDeDeteccao(r'(?:[Ss]ind|SIND)\w*.*',                 ForcaDoPadrao.FRACO, 3,    'sindic', sensivel=True), # Regras da filiação sindical
}

PESO_MAXIMO = max(padrao.peso for padrao in PADROES_DE_DETECCAO.values()) # Maior peso entre todos os tipos, usado no cálculo do score de risco

# Tipos sensíveis: poucos valores possíveis, então não podem ter troca 1-para-1 (seria
# reversível pela frequência); são censurados ou sorteados de novo em todas as linhas.
TIPOS_SENSIVEIS = {tipo for tipo, padrao in PADROES_DE_DETECCAO.items() if padrao.sensivel} # Conjunto com os tipos marcados como sensíveis na tabela acima
