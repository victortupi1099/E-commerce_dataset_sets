import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib
matplotlib.use('TkAgg',force=True)


def func_consulta(Df_sells):
 while True:
    userinp = input("\n\ndigite a função a ser aplicada\n você: ").strip().upper()
    
    while userinp not in ['HEAD', 'INFO', 'DESCRIBE', 'PROXIMO']:
        userinp = input("Digite CORRETAMENTE a função a ser aplicada: ").strip().upper()
    
    if userinp == 'HEAD':
        print("\n")
        print(Df_sells.head(20))
    
    elif userinp == 'INFO':
        print("\n")
        print(Df_sells.info())
    
    elif userinp == 'DESCRIBE':
        print("\n")
        print(Df_sells.describe())
    
    elif userinp == "PROXIMO":
        print("Indo para a próxima tarefa...")
        break

    print('Para as tarefas,de exibição profunda de dados digite "PROXIMO".')


def grafico_geral(Df_sells):
    
    soma_valores = Df_sells.groupby("Description")['TotalValue'].sum().reset_index()
    # ordenando valores maiores 
    soma_valores = soma_valores.sort_values(by="TotalValue", ascending=False).head(10)
    #exibição grafica
    plt.figure(figsize=(10,8))
    plt.bar(soma_valores["Description"],soma_valores["TotalValue"],color ="darkcyan")

    plt.title("10 Maiores Vendas por Produto")

    # Aplicando o formatter ao eixo y usando uma expressão lambda
    ax = plt.gca()
    ax.yaxis.set_major_formatter((lambda x, _: f'R$ {x:,.2f}'))

    plt.grid(axis='y')
    plt.xticks(rotation=55, ha="right" )
    plt.tight_layout()
    plt.show()


    

def produtos_por_pais(user_country,Df_sells):                      
    Df_sellsn = Df_sells[Df_sells["Country"] == user_country] #filtro para o País declarado pelo usuario
    soma_valores = Df_sellsn.groupby("Description")['TotalValue'].sum().reset_index()
    # ordenando valores maiores 
    soma_valores = soma_valores.sort_values(by="TotalValue", ascending=False).head(10)
    #exibição grafica
    
    plt.bar(soma_valores["Description"],soma_valores["TotalValue"],color ="darkcyan")

    plt.title("10 Maiores Vendas por Produto")

    # Aplicando o formatter ao eixo y usando uma expressão lambda
    ax = plt.gca()
    ax.yaxis.set_major_formatter((lambda x, _: f'R$ {x:,.2f}'))

    plt.grid(axis='y')
    plt.xticks(rotation=55, ha="right" )
    plt.tight_layout()
    plt.show()


def menos_produtos_vendidos(user_country,Df_sells):
    Df_sells = Df_sells[Df_sells['Quantity'] >= 0]
    Df_sells = Df_sells[Df_sells["Country"] == user_country] #filtro para o País declarado pelo usuario
    soma_valores = Df_sells.groupby("Description")['TotalValue'].sum().reset_index()
    # ordenando valores maiores 
    soma_valores = soma_valores.sort_values(by="TotalValue", ascending=True).head(10)
    #exibição grafica
    
    plt.bar(soma_valores["Description"],soma_valores["TotalValue"],color ="darkcyan")

    plt.title("10 Maiores Vendas por Produto")

    # Aplicando o formatter ao eixo y usando uma expressão lambda
    ax = plt.gca()
    ax.yaxis.set_major_formatter((lambda x, _: f'R$ {x:,.2f}'))

    plt.grid(axis='y')
    plt.xticks(rotation=55, ha="right" )
    plt.tight_layout()
    plt.show() 
  
def listar_datas(Df_sells):
    exb_date = Df_sells["InvoiceDate"].dt.strftime('%Y-%m-%d').unique() #data para exibição
    print(exb_date)


def exibir_por_data(user_data,Df_sells):
    Df_sells["InvoiceDate"] = Df_sells["InvoiceDate"].dt.date #removendo horas do dataset
    user_data = pd.to_datetime(user_data).date()
    Df_sells = Df_sells[Df_sells["InvoiceDate"] == user_data] #filtro para DAta declarada pelo usuario.
    
    soma_valores = Df_sells.groupby("Description")['TotalValue'].sum().reset_index()
    # ordenando valores maiores 
    soma_valores = soma_valores.sort_values(by="TotalValue", ascending=False).head(10)
    #exibição grafica
    
    plt.bar(soma_valores["Description"],soma_valores["TotalValue"],color ="darkcyan")

    plt.title("10 Maiores Vendas por Produto")

    # Aplicando o formatter ao eixo y usando uma expressão lambda
    ax = plt.gca()
    ax.yaxis.set_major_formatter((lambda x, _: f'R$ {x:,.2f}'))

    plt.grid(axis='y')
    plt.xticks(rotation=55, ha="right" )
    plt.tight_layout()
    plt.show()



def predicao_por_país(user_country,Df_sells):
    Df_sells['Year'] = Df_sells['InvoiceDate'].dt.year
    Df_sells['Month'] = Df_sells['InvoiceDate'].dt.month
    # Filtrando os dados pelo país informado pelo usuario
    country_data = Df_sells[Df_sells["Country"].str.strip().str.lower() == user_country.strip().lower()]
    if country_data.empty:
        return f"Nenhum dado encontrado para: {user_country}"
    # Agrupando gastos totais por ano e mês 
    monthly_data = country_data.groupby(['Year', 'Month'])['TotalValue'].sum().reset_index()
    # Verificar se há dados suficientes para a previsão
    if monthly_data.empty:
        return f" dados insuficientes para prever o  gasto total em {user_country}."  
    # Criar variáveis X e y para predição
    X = monthly_data[['Year', 'Month']]
    y = monthly_data['TotalValue']
    
    # Dividindo os dados em conjunto de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # configurando o modelo de regressão linear
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    #previsões para todos os meses do ano 
    future_months = pd.DataFrame({
        'Year': [2024] * 12,
        'Month': list(range(1, 13))
    })
    
    predicted_values = model.predict(future_months)
    
    # previsões
    future_months['Predicted_TotalValue'] = predicted_values
    
    #configurando exibição
    plt.figure(figsize=(10, 5))
    plt.bar(future_months["Month"].astype(str), future_months["Predicted_TotalValue"], color="darkcyan")
    plt.title(f"Previsão de Total Gasto em {user_country} para 2024")
    plt.xlabel("Meses")
    plt.ylabel("Total Gasto Previsto (Dollar)")
    
    ax = plt.gca()
    ax.yaxis.set_major_formatter((lambda x, _: f' {x:,.2f}'))
    
    plt.grid(axis='y')
    plt.xticks(rotation=55, ha="right")
    plt.tight_layout()
    plt.show()
    
    return future_months[['Year', 'Month', 'Predicted_TotalValue']]
