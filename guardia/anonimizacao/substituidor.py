import datetime # Importa o módulo datetime, que trabalha com datas e horas
import random # Importa o módulo random, que sorteia números
import re # Importa o módulo re, de expressões regulares (busca de padrões em texto)
from collections import defaultdict # Importa o defaultdict, um dicionário que cria sozinho o valor de uma chave nova

from faker import Faker # Importa o Faker, a biblioteca que gera dados falsos (nomes, sobrenomes etc.)

from guardia.anonimizacao.constantes import CARACTERE_DA_MASCARA # Importa o caractere usado na censura
from guardia.deteccao.calcular_digitos_verificadores_do_cpf import calcular_digitos_verificadores_do_cpf # Importa a função que calcula os 2 dígitos verificadores do CPF
from guardia.enumeracoes.tipo_de_dado_pessoal import TipoDeDadoPessoal # Importa o enum com os tipos de dado pessoal
from guardia.utilitarios.verificar_se_esta_vazio import verificar_se_esta_vazio # Importa a função que diz se um valor está vazio
from guardia.utilitarios.normalizar_texto import normalizar_texto # Importa a função que deixa o texto em minúsculas e sem acentos


DOMINIOS_DE_EMAIL = ( # Cria a tupla (lista que não muda) com os domínios sorteados para os e-mails falsos
    'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br', 'icloud.com', # Primeira metade dos domínios
    'uol.com.br', 'bol.com.br', 'terra.com.br', 'live.com', 'globo.com', # Segunda metade dos domínios
)

# Partes do nome que não entram no e-mail ("Ana da Silva" → ana.silva)
PARTICULAS_DE_NOME = {'da', 'de', 'do', 'das', 'dos', 'e'} # Conjunto com as partículas que ligam as partes de um nome

# Distribuição aproximada dos tipos sanguíneos na população brasileira (%)
DISTRIBUICAO_DO_TIPO_SANGUINEO = { # Cria o dicionário: cada tipo sanguíneo e a porcentagem da população que o tem
    'O+': 36.0, 'A+': 34.0, 'O-': 9.0, 'A-': 8.0, # Tipos O e A
    'B+': 8.0, 'B-': 2.0, 'AB+': 2.5, 'AB-': 0.5, # Tipos B e AB
}

# Tipos cujo valor é um número (com ou sem pontuação)
TIPOS_NUMERICOS = {TipoDeDadoPessoal.CPF, TipoDeDadoPessoal.TELEFONE, TipoDeDadoPessoal.CEP, TipoDeDadoPessoal.RG} # Conjunto com os tipos numéricos


def _extrair_digitos(valor): # Define a função privada que recebe um valor
    """Só os dígitos do valor: "529.982.247-25" → "52998224725"."""
    return re.sub(r'\D', '', str(valor)) # Apaga tudo que não é dígito e devolve o que sobrou


def _trocar_digitos(valor_original, digitos_novos): # Define a função privada que recebe o valor original e os dígitos novos
    """Coloca os novos dígitos no lugar dos antigos, mantendo pontos, traços e parênteses."""
    digitos_novos = iter(digitos_novos) # Prepara os dígitos novos para serem usados um de cada vez, em ordem
    return ''.join(next(digitos_novos, caractere) if caractere.isdigit() else caractere # Troca cada dígito pelo próximo dígito novo e mantém o que não é dígito
                   for caractere in str(valor_original)) # Passa por cada caractere do valor original


class Substituidor: # Define a classe que gera os valores sintéticos
    """Gera valores sintéticos coerentes, com dicionário bijetor por tipo."""

    def __init__(self, semente=None): # Define o que acontece ao criar o Substituidor, que pode receber uma semente
        self.gerador_de_dados_falsos = Faker('pt_BR') # Cria o gerador de dados falsos em português do Brasil
        self.gerador_aleatorio = random.Random(semente) # Cria o sorteador de números; com a mesma semente, os sorteios se repetem
        if semente is not None: # Confere se foi informada uma semente
            self.gerador_de_dados_falsos.seed_instance(semente) # Usa a mesma semente no Faker, para ele também repetir os dados
        self._dicionario_de_real_para_sintetico = {}            # (Tipo, valor real) → valor sintético
        self._valores_sinteticos_usados = defaultdict(set)      # Tipo → valores sintéticos já entregues

    def substituir(self, tipo, valor, nome=None): # Define o método que troca um valor real por um sintético
        """Valor sintético para 'valor'. 'nome' (sintético) é usado para montar o e-mail."""
        if verificar_se_esta_vazio(valor): # Confere se o valor está vazio
            return valor # Valor vazio continua vazio
        # CPF, telefone, CEP e RG usam só os dígitos como chave: '52998224725' na coluna e
        # '529.982.247-25' no texto viram o MESMO valor falso, cada um no seu formato.
        usa_digitos_como_chave = tipo in TIPOS_NUMERICOS and bool(_extrair_digitos(valor)) # Confere se o tipo é numérico e se o valor tem dígitos
        valor_original = _extrair_digitos(valor) if usa_digitos_como_chave else valor # Usa só os dígitos ou o valor inteiro como valor original
        chave = (tipo, valor_original) # Monta a chave do dicionário: o tipo junto com o valor original
        if chave not in self._dicionario_de_real_para_sintetico: # Confere se este valor ainda não foi trocado antes
            valor_sintetico = valor_original # Começa com o próprio valor original, só para a variável existir
            for _ in range(100): # Tenta até 100 vezes gerar um valor sintético novo
                valor_sintetico = self._gerar_valor_sintetico(tipo, valor_original, nome) # Gera um valor sintético para o tipo
                if valor_sintetico != valor_original and valor_sintetico not in self._valores_sinteticos_usados[tipo]: # Confere se é diferente do real e se ainda não foi usado
                    break # Achou um valor bom: para de tentar
            self._valores_sinteticos_usados[tipo].add(valor_sintetico) # Marca o valor sintético como usado
            self._dicionario_de_real_para_sintetico[chave] = valor_sintetico # Guarda a troca no dicionário, para o mesmo valor real virar sempre o mesmo sintético
        valor_sintetico = self._dicionario_de_real_para_sintetico[chave] # Pega no dicionário o valor sintético deste valor real
        if not usa_digitos_como_chave: # Se o tipo não é numérico
            return valor_sintetico # Devolve o valor sintético como está
        if isinstance(valor, int): # Se o valor original era um número inteiro
            return int(valor_sintetico) # Devolve o sintético também como número inteiro
        tem_o_mesmo_tamanho = len(_extrair_digitos(valor)) == len(valor_sintetico) # Confere se o original e o sintético têm a mesma quantidade de dígitos
        return _trocar_digitos(valor, valor_sintetico) if tem_o_mesmo_tamanho else valor_sintetico # Devolve o sintético no formato do original, com a mesma pontuação, quando dá

    def sortear_dado_sensivel(self, achado): # Define o método que sorteia um valor falso para dado sensível
        """
        Valor sintético para dado SENSÍVEL, sorteado de novo em cada linha (sem dicionário):
        - tipo sanguíneo: pela distribuição da população brasileira;
        - filiação sindical: filiado na mesma proporção da coluna original, em um dos
          sindicatos que aparecem nela; senão, vazio.
        """
        if achado.tipo == TipoDeDadoPessoal.TIPO_SANGUINEO: # Se o dado é tipo sanguíneo
            tipos, pesos = zip(*DISTRIBUICAO_DO_TIPO_SANGUINEO.items()) # Separa a tabela em duas listas: os tipos sanguíneos e as porcentagens
            return self.gerador_aleatorio.choices(tipos, weights=pesos)[0] # Sorteia um tipo sanguíneo; os mais comuns saem mais vezes
        if self.gerador_aleatorio.random() >= achado.taxa_de_preenchimento or not achado.valores_observados: # Sorteia se a pessoa é filiada, na mesma proporção da coluna original
            return None # Não é filiada: o valor fica vazio
        return self.gerador_aleatorio.choice(achado.valores_observados) # É filiada: sorteia um dos sindicatos que apareceram na coluna

    def descartar_dicionario(self): # Define o método que apaga o dicionário de trocas
        """Apaga o dicionário real → sintético: o processo passa a ser irreversível."""
        self._dicionario_de_real_para_sintetico.clear() # Esvazia o dicionário de valor real para valor sintético
        self._valores_sinteticos_usados.clear() # Esvazia a lista de valores sintéticos já usados

    # --- Geradores por tipo ------------------------------------------------

    def _gerar_valor_sintetico(self, tipo, valor, nome): # Define o método privado que escolhe o gerador certo para o tipo
        gerador = { # Cria o dicionário: cada tipo e o método que gera o valor falso dele
            TipoDeDadoPessoal.CPF: self._gerar_cpf, # Gerador de CPF
            TipoDeDadoPessoal.RG: self._gerar_rg, # Gerador de RG
            TipoDeDadoPessoal.EMAIL: lambda valor_ignorado: self._gerar_email(nome), # Gerador de e-mail: usa o nome sintético e ignora o e-mail original
            TipoDeDadoPessoal.DATA_DE_NASCIMENTO: self._gerar_data, # Gerador de data
            TipoDeDadoPessoal.TELEFONE: self._gerar_telefone, # Gerador de telefone
            TipoDeDadoPessoal.NOME: self._gerar_nome, # Gerador de nome
            TipoDeDadoPessoal.CEP: self._gerar_cep, # Gerador de CEP
        }.get(tipo, self._gerar_valor_generico) # Pega o gerador do tipo; se não houver, usa o gerador genérico
        return gerador(valor) # Gera e devolve o valor falso

    def _sortear_numeros(self, quantidade): # Define o método privado que sorteia uma sequência de dígitos
        return ''.join(str(self.gerador_aleatorio.randrange(10)) for _ in range(quantidade)) # Sorteia a quantidade pedida de dígitos de 0 a 9 e junta tudo num texto

    def _gerar_cpf(self, valor): # Define o método privado que gera um CPF falso
        """CPF válido: 9 dígitos sorteados (não todos iguais) + os 2 dígitos verificadores."""
        while True: # Repete até sortear 9 dígitos que não sejam todos iguais
            nove_digitos = self._sortear_numeros(9) # Sorteia 9 dígitos
            if len(set(nove_digitos)) > 1: # Confere se há pelo menos 2 dígitos diferentes
                break # Os dígitos servem: sai da repetição
        primeiro_digito_verificador, segundo_digito_verificador = calcular_digitos_verificadores_do_cpf(nove_digitos) # Calcula os 2 dígitos verificadores
        cpf_novo = f'{nove_digitos}{primeiro_digito_verificador}{segundo_digito_verificador}' # Junta os 9 dígitos com os 2 verificadores
        if isinstance(valor, int): # Se o CPF original era um número inteiro
            return int(cpf_novo) # Devolve o CPF novo também como número inteiro
        return _trocar_digitos(valor, cpf_novo) if len(_extrair_digitos(valor)) == 11 else cpf_novo # Devolve o CPF novo com a pontuação do original, quando ele tinha 11 dígitos

    def _gerar_rg(self, valor): # Define o método privado que gera um RG falso
        return _trocar_digitos(valor, self._sortear_numeros(len(_extrair_digitos(valor)))) # Sorteia a mesma quantidade de dígitos e mantém a pontuação do original

    def _gerar_telefone(self, valor): # Define o método privado que gera um telefone falso
        """Mantém o DDD (compatível com a cidade) e sorteia o resto; celular mantém o 9."""
        digitos = _extrair_digitos(valor) # Pega só os dígitos do telefone
        digitos_fixos = digitos[:3] if len(digitos) == 11 and digitos[2] == '9' else digitos[:2] # Celular mantém o DDD e o 9; fixo mantém só o DDD
        telefone_novo = digitos_fixos + self._sortear_numeros(len(digitos) - len(digitos_fixos)) # Junta os dígitos mantidos com dígitos sorteados no lugar do resto
        return int(telefone_novo) if isinstance(valor, int) else _trocar_digitos(valor, telefone_novo) # Devolve como número, se o original era número; senão, com a pontuação do original

    def _gerar_cep(self, valor): # Define o método privado que gera um CEP falso
        """Mantém os 5 primeiros dígitos (mesma região/cidade) e sorteia os 3 últimos."""
        digitos = _extrair_digitos(valor) # Pega só os dígitos do CEP
        cep_novo = digitos[:5] + self._sortear_numeros(len(digitos) - 5) # Mantém os 5 primeiros dígitos e sorteia o resto
        return int(cep_novo) if isinstance(valor, int) else _trocar_digitos(valor, cep_novo) # Devolve como número, se o original era número; senão, com a pontuação do original

    def _gerar_data(self, valor): # Define o método privado que gera uma data falsa
        """Outro dia do mesmo ano: preserva a idade aproximada."""
        if isinstance(valor, (datetime.date, datetime.datetime)): # Confere se o valor é uma data
            dias_depois_de_primeiro_de_janeiro = self.gerador_aleatorio.randrange(365) # Sorteia um número de dias entre 0 e 364
            dia_sorteado = datetime.date(valor.year, 1, 1) + datetime.timedelta(days=dias_depois_de_primeiro_de_janeiro) # Soma esses dias ao 1.º de janeiro do mesmo ano
            if isinstance(valor, datetime.datetime): # Se o valor também tinha hora
                return valor.replace(year=dia_sorteado.year, month=dia_sorteado.month, day=dia_sorteado.day) # Troca só o dia e o mês, mantendo a hora
            return dia_sorteado # Devolve o dia sorteado
        for formato in ('%d/%m/%Y', '%Y-%m-%d'): # Tenta ler o texto nos dois formatos de data aceitos
            try: # Tenta converter o texto em data; se não der, cai no except
                data = datetime.datetime.strptime(str(valor), formato).date() # Converte o texto numa data, no formato da vez
            except ValueError: # Se o texto não estava neste formato
                continue # Tenta o próximo formato
            return self._gerar_data(data).strftime(formato) # Gera uma data falsa e a devolve como texto, no mesmo formato
        return _trocar_digitos(valor, self._sortear_numeros(len(_extrair_digitos(valor)))) # Se não era uma data conhecida, só troca os dígitos por dígitos sorteados

    def _gerar_nome(self, valor): # Define o método privado que gera um nome falso
        """Mesma quantidade de palavras do original (mínimo 2); nome e nome do meio do mesmo gênero."""
        quantidade_de_partes = max(2, min(5, len(str(valor).split()))) # Conta as palavras do nome original, ficando entre 2 e 5
        if self.gerador_aleatorio.random() < 0.5: # Sorteia o gênero, com 50% de chance para cada um
            gerar_nome_do_genero_sorteado = self.gerador_de_dados_falsos.first_name_female # Vai gerar nomes femininos
        else: # Se não saiu feminino
            gerar_nome_do_genero_sorteado = self.gerador_de_dados_falsos.first_name_male # Vai gerar nomes masculinos

        def sortear_primeiro_nome(): # Define uma função interna que sorteia um nome de uma palavra só
            while ' ' in (nome := gerar_nome_do_genero_sorteado()):      # O Faker tem nomes compostos ("João Pedro")
                pass # Não faz nada: só repete o sorteio
            return nome # Devolve o nome sorteado

        nomes = [sortear_primeiro_nome()] # Começa a lista de nomes com o primeiro nome
        while quantidade_de_partes >= 3 and len(nomes) < 2: # Se o nome tem 3 partes ou mais, também precisa de um nome do meio
            nome_do_meio = sortear_primeiro_nome() # Sorteia o nome do meio, do mesmo gênero
            if nome_do_meio != nomes[0]: # Confere se o nome do meio é diferente do primeiro nome
                nomes.append(nome_do_meio) # Acrescenta o nome do meio à lista
        sobrenomes = [] # Lista que vai guardar os sobrenomes
        while len(nomes) + len(sobrenomes) < quantidade_de_partes: # Repete até completar a quantidade de partes do nome original
            sobrenome = self.gerador_de_dados_falsos.last_name() # Sorteia um sobrenome
            if ' ' not in sobrenome and sobrenome not in sobrenomes:      # Evita "da Cunha" contar como 2 palavras
                sobrenomes.append(sobrenome) # Acrescenta o sobrenome à lista
        return ' '.join(nomes + sobrenomes) # Junta os nomes e os sobrenomes, com um espaço entre eles

    def _gerar_email(self, nome): # Define o método privado que gera um e-mail falso
        """E-mail feito a partir do nome sintético da pessoa, em um formato sorteado."""
        nome_normalizado = normalizar_texto(nome or self._gerar_nome('x x x')) # Usa o nome sintético da pessoa (ou gera um), em minúsculas e sem acentos
        partes = [re.sub(r'[^a-z]', '', parte) for parte in nome_normalizado.split()] # Separa o nome em palavras e deixa só as letras de cada uma
        partes = [parte for parte in partes if parte and parte not in PARTICULAS_DE_NOME] or ['usuario'] # Tira as partículas e as palavras vazias; se não sobrar nada, usa "usuario"
        primeiro_nome, ultimo_sobrenome = partes[0], partes[-1] # Pega a primeira e a última palavra do nome
        nome_do_meio = partes[1] if len(partes) > 2 else '' # Pega o nome do meio, se o nome tiver mais de 2 palavras
        formatos = [ # Cria a lista com os formatos possíveis para o usuário do e-mail
            f'{primeiro_nome}.{ultimo_sobrenome}', # Nome, ponto e sobrenome
            f'{primeiro_nome}_{ultimo_sobrenome}', # Nome, traço baixo e sobrenome
            f'{primeiro_nome}{ultimo_sobrenome}', # Nome e sobrenome juntos
            f'{primeiro_nome[0]}{ultimo_sobrenome}', # Primeira letra do nome e sobrenome
            f'{ultimo_sobrenome}.{primeiro_nome}', # Sobrenome, ponto e nome
        ]
        if nome_do_meio: # Se o nome tem nome do meio
            formatos += [ # Acrescenta mais dois formatos à lista
                f'{primeiro_nome}.{nome_do_meio}.{ultimo_sobrenome}', # Nome, nome do meio e sobrenome, separados por ponto
                f'{primeiro_nome}{nome_do_meio[0]}{ultimo_sobrenome}', # Nome, primeira letra do nome do meio e sobrenome
            ]
        usuario = self.gerador_aleatorio.choice(formatos) # Sorteia um dos formatos para o usuário do e-mail
        if self.gerador_aleatorio.random() < 0.5: # Com 50% de chance
            usuario += str(self.gerador_aleatorio.randrange(100)) # Acrescenta um número de 0 a 99 no fim do usuário
        return f'{usuario}@{self.gerador_aleatorio.choice(DOMINIOS_DE_EMAIL)}' # Junta o usuário com um domínio sorteado e devolve o e-mail

    def _gerar_valor_generico(self, valor): # Define o método privado usado para tipos sem gerador próprio
        digitos = _extrair_digitos(valor) # Pega só os dígitos do valor
        return _trocar_digitos(valor, self._sortear_numeros(len(digitos))) if digitos else CARACTERE_DA_MASCARA * len(str(valor)) # Troca os dígitos por dígitos sorteados; se não houver dígitos, troca tudo por asteriscos
