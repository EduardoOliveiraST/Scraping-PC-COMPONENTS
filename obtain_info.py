import pandas as pd
import re

def separate_placa_de_video(df):
    def separar_dados(produto):
        padrao = re.compile(r'Placa [Dd]e [Vv][ií]deo (.+?) (.+?) (.+?), (\d+GB)')
        match = padrao.search(produto)
        if match:
            marca = match.group(1)
            modelo = match.group(3)
            giga_placa = match.group(4)
            return pd.Series([marca, modelo, giga_placa])
        return pd.Series([None, None, None])

    df[['Marca', 'Modelo', 'Gigas']] = df['Produto'].apply(separar_dados)

def separate_processador(df):
    def separar_dados(produto):
        padrao_amd = re.compile( r'Processador (AMD|Intel) ([\w\s\d]+),? ([\d\.]+GHz) (\([\d\.]+GHz Turbo\)), (\d+-Cores \d+-Threads), (([cC]ooler \w+ \w+|[sS]em [cC]ooler|[cC]om [cC]ooler), (AM\d)|(AM\d), ([cC]ooler \w+ \w+|[sS]em [cC]ooler|[cC]om [cC]ooler))')
        
        match_amd = padrao_amd.search(produto)
        if match_amd:
            fabricante = match_amd.group(1)
            modelo = match_amd.group(2)
            frequencia_base = match_amd.group(3)
            cores_threads = match_amd.group(5)
            socket_tratado = match_amd.group(6).split(',')
            socket = socket_tratado[0] if 'AM4' in socket_tratado[0].strip() or 'AM5' in socket_tratado[0].strip() else socket_tratado[1].strip()
            return pd.Series([fabricante, modelo, frequencia_base, cores_threads, socket])
        return pd.Series([None, None, None, None, None])

    df[['Fabricante', 'Modelo', 'Frequencia_base', 'Cores_threads', 'Socket']] = df['Produto'].apply(separar_dados)
