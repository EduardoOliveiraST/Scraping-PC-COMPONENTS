import pandas as pd 
import re
import locale
import obtain_info
import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def tratar_preco_atual(data):
    if data == '749':
        pass
    data = re.sub(r'[^\d.,]', '', data)
    data = ''.join(data.split(',')[0:-1][0].split('.')[0:])
    data = int(data)
    return f"{data:.2f}"

def tratar_preco_parcelado(parcelamento):
    parcelas, valor_parcela = parcelamento.split('x de ')
    parcelas = int(parcelas)
    valor_parcela = float(valor_parcela)
    return parcelas, valor_parcela

def tratar_parcelamento(data, categoria):
    val_parc = re.findall(r'\d+', data)
    val_parc = val_parc[:-1]
    data = f"{val_parc[0]}x de {''.join(val_parc[1:])}" 
    return(data)

def trata_dados(file_name):
    def categorize(text, tipo):
        
        if tipo == 'processadores':
            if isinstance(text, str):
                if re.search(r"^Processador", text):
                    return "Produto"
                elif re.search(r"De:\s+R\$", text):
                    return "Preco_Original"
                elif "à vista" in text:
                    return "Preco_Atual"
                elif re.search(r"\b\d+(\.\d+)?\b", text):
                    padrao_parcelamento = r"\b\d+(\.\d+)?\b"
                    unidades = ['mm', 'cm', 'kg', 'g', 'GHz', 'MHz', 'W']
                        # Procurar todos os números na string
                    numeros = re.findall(padrao_parcelamento, text)

                    # Verificar se os números estão próximos de unidades de medida comuns
                    for numero in numeros:
                        for unidade in unidades:
                            if re.search(rf"{numero}\s*{unidade}", text):
                                return False

                            # Se não há unidades de medida, considerar como parcelamento
                    if bool(numeros):
                        return "Parcelamento"
                    else:
                        return 'Outros'
            return "Outros"
        
        else:
            if isinstance(text, str):
                if re.search(r"^Placa\s+[dD]e\s+V[ií]deo", text):
                    return "Produto"
                elif re.search(r"De:\s+R\$", text):
                    return "Preco_Original"
                elif "à vista" in text:
                    return "Preco_Atual"
                elif re.search(r"\b\d+(\.\d+)?\b", text):
                    return "Parcelamento"
            return "Outros"

    for file in file_name:
        if 'processadores' in file :
            tipo = 'processadores'
        else:
            tipo = 'placavideo'

        df = pd.read_excel(f'raw_data/{file}')

        df = df.rename(columns={'Unnamed: 0': 'principal'})

        inicio_padrao = "(^Processador.*)" if tipo == 'processadores' else "(^Placa [dD]e [vV][ií]deo.*)"

        # Extrair as partes desejadas do texto
        parte_inicial = list(df['principal'].str.extract(inicio_padrao, expand=False).dropna().index)

        filtro = "(^Todos vendidos*)"
        exclude_inicial = list(df['principal'].str.extract(filtro, expand=False).dropna().index)
        exclude_inicial = [c - 1 for c in exclude_inicial]

        parte_inicial = [item for item in parte_inicial if item not in exclude_inicial]
        parte_final = [num + 7  for num in parte_inicial]

                # Verificar se as contagens são diferentes
        if len(parte_inicial) != len(parte_final):
            print("Os índices iniciais e finais têm contagens diferentes.")
            # Ajustar os índices para garantir que tenham o mesmo comprimento
            min_len = min(len(parte_inicial), len(parte_final))
            parte_inicial = parte_inicial[:min_len]
            parte_final = parte_final[:min_len]

        indices = {'Indice_Inicial': parte_inicial,
                   'Indice_Final': parte_final}

        df_indices = pd.DataFrame(indices)
        linhas_entre_indices = []
        for linha in df_indices.iterrows():
            indice_inicial = linha[1]['Indice_Inicial']
            indice_final = linha[1]['Indice_Final']
            if indice_final >= indice_inicial and indice_final < len(df['principal']):
                linhas_entre_indices.append(df['principal'].iloc[indice_inicial:indice_final])
            else:
                print(f"Índices inválidos: [{indice_inicial}, {indice_final}]")

        # Concatenar todas as linhas em um único DataFrame
        resultado = pd.DataFrame(columns=['data'])
        resultado['data'] = pd.concat(linhas_entre_indices).reset_index(drop=True)

        resultado['Categoria'] = resultado['data'].apply(lambda x: categorize(x, tipo))

        resultado = resultado[resultado['Categoria'] != 'Outros']

        # Criar um novo DataFrame tabular com base nas categorias
        tabular_data = {'Produto': [], 'Preco_Original': [], 'Preco_Atual': [], 'Parcelamento': []}

        produto_atual = None
        for _, row in resultado.iterrows():
            categoria = row['Categoria']
            if 'Placa De Vídeo Gigabyte NVIDIA GeForce RTX 4090 AORUS MASTER' in row['data']:
                pass
            if categoria != 'Outros':

                # Tratamento específico para cada categoria
                if categoria == 'Produto':
                    if produto_atual:
                        # Adicione os dados ao DataFrame tabular
                        for key, value in produto_atual.items():
                            tabular_data[key].append(value)
                    # Inicialize os dados do produto atual
                    produto_atual = {key: None for key in tabular_data.keys()}
                    produto_atual[categoria] = row['data']

                elif categoria == 'Preco_Original':
                    # Tratamento para Preco_Original
                    preco_original_tratado = tratar_preco_atual(row['data'])
                    produto_atual[categoria] = preco_original_tratado

                elif categoria == 'Preco_Atual':
                    # Tratamento para Preco_Atual
                    preco_atual_tratado = tratar_preco_atual(row['data'])
                    produto_atual[categoria] = preco_atual_tratado
                elif categoria == 'Parcelamento':

                    # Tratamento para Parcelamento
                    parcelamento_tratado = tratar_parcelamento(row['data'], categoria)
                    produto_atual[categoria] = parcelamento_tratado


        # Adiciona os dados do último produto ao DataFrame tabular
        for key, value in produto_atual.items():
            tabular_data[key].append(value)

        df_tabular = pd.DataFrame(tabular_data)

        df_tabular['Preco_Original'] = pd.to_numeric(df_tabular['Preco_Original'].str.replace(',', '.'))
        df_tabular['Preco_Atual'] = pd.to_numeric(df_tabular['Preco_Atual'].str.replace(',', '.'))

        df_tabular['Desconto'] = df_tabular['Preco_Original'] - df_tabular['Preco_Atual']

        # Aplicar a função à coluna Parcelamento
        df_tabular['Parcelas'], df_tabular['Valor_Parcela'] = zip(*df_tabular['Parcelamento'].apply(tratar_preco_parcelado))

        # Calcular o preço parcelado
        df_tabular['Preco_Parcelado'] = df_tabular['Parcelas'] * df_tabular['Valor_Parcela']
        # Converter a string para um objeto datetime
        data = datetime.datetime.strptime(file.split('_')[2][:8], "%Y%m%d")

        # Formatar a data no formato 'DD-MM-YYYY'
        data_formatada = data.strftime("%d-%m-%Y")
        df_tabular['Extract_date'] = data_formatada

        if tipo == 'placavideo':
            obtain_info.separate_placa_de_video(df_tabular)

            ordem_colunas = ['Produto', 'Marca', 'Modelo', 'Gigas', 'Preco_Original', 'Preco_Atual', 'Desconto', 'Parcelamento', 'Preco_Parcelado', 'Extract_date']

            # Reordena as colunas do DataFrame
            df_tabular = df_tabular[ordem_colunas]
        else:
            obtain_info.separate_processador(df_tabular)

            ordem_colunas = ['Produto', 'Fabricante', 'Modelo', 'Frequencia_base', 'Cores_threads', 'Socket', 'Preco_Original', 'Preco_Atual', 'Desconto', 'Parcelamento', 'Preco_Parcelado', 'Extract_date']

            # Reordena as colunas do DataFrame
            df_tabular = df_tabular[ordem_colunas]

        df_tabular.to_excel(f'output_data/{file.replace(".xlsx", "")}_COMPLETED.xlsx', header=True, index=False)

    pass
