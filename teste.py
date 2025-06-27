import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('data\\dados_sensores.csv')

df['data'] = pd.to_datetime(df['Data_Coleta'])

hoje = pd.Timestamp.today().normalize()

lista_ultimas_datas = []
lista_ultimas_datas.append(hoje.day)
for i in range(1,7):
    sete_dias_atras = hoje - pd.Timedelta(days=i) 
    lista_ultimas_datas.append(sete_dias_atras.day)


# sete_dias_atras = hoje - pd.Timedelta(days=6) 

# ultimos_7_dias = df[(df['data'] >= sete_dias_atras) & (df['data'] <= hoje)]

