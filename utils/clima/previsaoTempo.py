import requests
import math

API_KEY = "b36d6245a16e41f410be3ce7b48a1f23"
cidade = "São Paulo"
link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"

def informacoesTempo():
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic["weather"][0]["description"]
    temperatura = requisicao_dic["main"]["temp"]
    temperatura = "🌡️\t" + str(math.floor(temperatura)) + " °C"
    descricao = "⛅\t" + descricao
    return temperatura, descricao