import pdfplumber
import pandas as pd

dados_tabelas = [] #array onde os dados vão ser copulados

with pdfplumber.open("src/pdf_exemplo.pdf") as pdf:
    for pagina in pdf.pages:
        tabelas = pagina.extract_tables()
        # print(tabelas)
        # print(len(tabelas))
        for tabela in tabelas:
            # print(tabela)
            # print(len(tabela))
            if len(tabela) > 1:
                data, historico, valor = '','',''
                # print(data,historico,valor)
                # print("Aqui tem mais ",len(tabela))
                for linha in tabela:
                    # print(linha)
                    if linha[0] != '':
                        data += ' ' + linha[0]
                    if historico == '' and linha[1] != '':
                        historico += ' ' + linha[1]
                    elif linha[1] != '':
                        historico += ', ' + linha[1]
                    if linha[1] != '':
                        historico += ', ' + linha[1]
                    if linha[2] != '':
                        valor += ' ' + linha[2]
                if data != ''and historico != '' and valor != '':
                    dados_tabelas.append([data,historico,valor])
                    
df = pd.DataFrame(dados_tabelas,  columns=['Data', 'Histórico', 'Valor'])             
print(df)     
                    
        
        
        