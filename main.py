import pandas as pd
import numpy as np
import plotly as plt
import matplotlib
matplotlib.use('TkAgg',force=True)
import matplotlib.pyplot as plt
print("Switched to:",matplotlib.get_backend())
import sklearn
import func
Df_sells = pd.read_csv('D:/Desktop/estudos_academicos/cursinhos/datascience/Trabalho_Conclusão_de_Curso/data_sets/ecom_data.csv', encoding="ISO-8859-1", dtype={'CustomerID': str})
#importação e tratamento

Df_sells["InvoiceDate"] = pd.to_datetime(Df_sells["InvoiceDate"])
Df_sells['Description'].replace(['nan', 'NAN'], np.nan) #filtrando valores vazios
Df_sells = Df_sells.dropna(subset=['Description'])
Df_sells = Df_sells.dropna(subset=['CustomerID'])


Df_sells["Description"] = Df_sells["Description"].str.upper()
Df_sells["Description"] =Df_sells["Description"].str.strip() #nivelando valores


Df_sells['TotalValue'] = Df_sells['UnitPrice'] * Df_sells['Quantity'] #crindo valor total de vendas

# Organizar o DataFrame por InvoiceDate e CustomerID
Df_sells = Df_sells.sort_values(by=['InvoiceDate', 'CustomerID'])
#___________________________________________________________________________________________________________________________________________________tratamento de dados acima







print("bem vindo a analise rapida do data frame\n podes escolher funções basicas para serem aplicadas sobre o Data_set\n")
print('as funções de carater informativos iniciais: \ninfo\n head\n describe')

#head

print("funções de consulta")
func.func_consulta(Df_sells)

     
while True:    
    print("\n\nselecione o parametro:  \n")
    parametros = ["grafico geral de produtos","produtos mais vendidos por país","produtos menos vendidos por país", "vendas por datas","predição de vendas por país","consulta","sair"]
    print("---------------------------------------------------")
    for i in range(7):
        print(f"{i+1}: {parametros[i]}")
    print("---------------------------------------------------")    
    print('\npara sair digite sair\npara voltar a consulta basica digite "consulta"')

    userinp = input("\n para a amostragem correta de grafico\ncopie e cole a opção desejada:\nvocê: ").strip()
    while userinp not in parametros:
       userinp = input("\n para a amostragem correta de grafico\ncopie e cole a opção desejada:\nvocê: ").strip()
       

    if  userinp == "grafico geral de produtos": 
     func.grafico_geral(Df_sells)
    
    if  userinp == "produtos mais vendidos por país":
     print(Df_sells["Country"].unique())
     user_country = input("digite o país desejado\nvocê:")
     func.produtos_por_pais(user_country,Df_sells)
    
    if userinp == "produtos menos vendidos por país":
       print(Df_sells["Country"].unique())
       user_country = input("digite o país desejado\nvocê:")
       func.menos_produtos_vendidos(user_country,Df_sells)
    
    if userinp == "vendas por datas":
       func.listar_datas(Df_sells)
       user_data = input("digite a data para analise\nvocê: ")
       func.exibir_por_data(user_data,Df_sells)
  
    if userinp == "predição de vendas por país":
       print(Df_sells["Country"].unique())
       user_country = input("digite o país desejado\nvocê:")
       func.predicao_por_país(user_country,Df_sells)


    if userinp == "consulta":
       func.func_consulta(Df_sells)

    if userinp == "sair":
       break 

