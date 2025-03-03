import pdfplumber
import pandas as pd

def extrair_tabelas_do_pdf(arquivo_pdf, arquivo_excel): #Função principal do projeto
    dados_tabelas = [] #array onde os dados vão ser copulados

    ano = extrair_ano_do_periodo(arquivo_pdf) # executa função que estrai o ano do documento e coloca e armazena
    
    with pdfplumber.open(arquivo_pdf) as pdf: #Abrindo o PDF de onde serão extraidos os dados da planilha
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables() #extrai as tabelas presentes no pdf
            for tabela in tabelas:
                if len(tabela) > 1: #garante que somente linhas com tres colunas sejam analizadas
                    data, historico, valor = '','',''
                    for linha in tabela:
                        if linha[0] != '': #Se o campo de data daquela linha não for vazio
                            data += ' ' + linha[0] + "/" + ano #preenche a data com o ano antes recolhido
                        if historico == '' and linha[1] != '':#Se o campo de historico daquela linha não for vazio e o campo de historico tambem estiver vazio
                            historico += ' ' + linha[1] #preenche a primeira linha do historico
                        elif linha[1] != '':#caso haja mais linhas com informações
                            historico += ', ' + linha[1] #acrecenta ao historico separando com ","
                        if linha[2] != '':#Se o campo de valor não for vazio
                            letra = linha[2][-1] #guarda a letra no final do valor
                            numero = linha[2][:-1] #guarda o numero do valor
                            if letra == "D":
                                valor = "-" + numero #Se a letra for "D" o valor vai ser negativo
                            elif letra == "C":
                                valor = numero #Se a letra for "C" o valor vai ser positivo
                            print(valor)     
                    if data != ''and historico != '' and valor != '': #Se os dados da linha forem preenchidos corratamente, adiciona a lista a tabela
                        dados_tabelas.append([data,historico,valor])
                
        print("array copulada com os dados das transações")
        

    conta = extrair_numero_conta(arquivo_pdf) #executa a função que puxa o numero da conta no pdf
    print("numero da conta: ",conta)
    
     #inclui o numero da conta em cada linha da tabela
    for linha in dados_tabelas:
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

def extrair_ano_do_periodo(arquivo_pdf):
    with pdfplumber.open(arquivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            for linha in texto.split("\n"):
                if "PERÍODO:" in linha:
                    partes = linha.split()
                    for parte in partes:
                        if "/" in parte and len(parte) == 10:  # Formato dd/mm/aaaa
                            ano = parte.split("/")[-1]  # Pega o ano
                            return ano
    return None  # Retorna None se não encontrar

# Executando o programa
extrair_tabelas_do_pdf("src/pdf_exemplo.pdf", "src/planilha.xlsx")

