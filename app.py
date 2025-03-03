import pdfplumber
import pandas as pd

def extrair_tabelas_do_pdf(arquivo_pdf, arquivo_excel): #Função principal do projeto
    dados_tabelas = [] #array onde os dados vão ser copulados

    with pdfplumber.open(arquivo_pdf) as pdf:
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
                    tabela = [data,historico,valor]
                    if data != ''and historico != '' and valor != '':
                        dados_tabelas.append([data,historico,valor])
        print("array copulada com os dados das transações")
        

    conta = extrair_numero_conta(arquivo_pdf) #executa a função que puxa o numero da conta no pdf
    print("numero da conta: ",conta)
    
     #inclui o numero da conta em cada linha da tabela
    for linha in dados_tabelas:
        print(linha)
        linha.insert(3,conta)
    
    # Cria um DataFrame do Pandas
    df = pd.DataFrame(dados_tabelas,columns=['Data', 'Histórico', 'Valor','Conta'])
    print(df)
    # Salvar em um arquivo Excel
    df.to_excel(arquivo_excel, index=False, header=True)

    print(f"Conversão concluída! Arquivo salvo como {arquivo_excel}")

def extrair_numero_conta(arquivo): #Função que encontra o numero da conta no pdf
    with pdfplumber.open(arquivo) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            for linha in texto.split("\n"):
                if "CONTA:" in linha:  # Verifica se a linha contém "CONTA:"
                    numero_conta = linha.split(":")[1].strip()  # Pega o número após ":"
                    return numero_conta
    return None  # Retorna None se não encontrar

# Executando o programa
extrair_tabelas_do_pdf("src/pdf_exemplo.pdf", "src/planilha.xlsx")

