import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

def previsaoSensores():
    # Carregar o CSV
    df = pd.read_csv('data\\dados_sensores.csv')

    # Garantir que os dados estejam limpos
    df = df.dropna()
    df['Temperatura_Ambiente'] = pd.to_numeric(df['Temperatura_Ambiente'])
    df['Umidade_Ambiente'] = pd.to_numeric(df['Umidade_Ambiente'])
    df['Umidade_Solo'] = pd.to_numeric(df['Umidade_Solo'])

    # Variáveis de entrada e saída
    X = df[['Temperatura_Ambiente', 'Umidade_Ambiente']]
    y = df['Umidade_Solo']

    # Treinar o modelo
    modelo = RandomForestRegressor(random_state=42)
    modelo.fit(X, y)

    # Simular previsões para os próximos 7 dias (exemplo com dados aleatórios)
    dias_previsao = 30
    media_temp = df['Temperatura_Ambiente'].mean()
    media_umidade = df['Umidade_Ambiente'].mean()
    np.random.seed(42)
    temperaturas_futuras = np.random.normal(media_temp, 2, dias_previsao)
    umidades_futuras = np.random.normal(media_umidade, 5, dias_previsao)

    # Criar DataFrame para previsão com os nomes corretos
    dados_futuros = pd.DataFrame({
        'Temperatura_Ambiente': temperaturas_futuras,
        'Umidade_Ambiente': umidades_futuras
    })

    # Prever umidade do solo para os próximos dias
    previsoes = modelo.predict(dados_futuros)

    # Verificar quais dias precisam de irrigação
    limite_umidade = 20.0 
    umidade_texto = ""

    molhar_planta = False
    dia = 0
    for i, umidade in enumerate(previsoes):
        if umidade < limite_umidade:
            dia = i+1
            umidade_texto = (f'(Umidade prevista: {umidade:.2f}%)')
            molhar_planta = True
            break
        else:
            umidade_texto = (f'(Umidade prevista: {umidade:.2f}%)')

    if molhar_planta:
        texto_padrao = f"🔔 Será necessário regar daqui a {dia} dias"
        return texto_padrao, umidade_texto
    else:
        texto_padrao = "✅ A umidade OK. Não precisa regar."
        return texto_padrao, umidade_texto