from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.clima.previsaoTempo import informacoesTempo
from utils.previsao import previsaoSensores
from utils.filtroPlaca import placa_filter
import os

from dash_bootstrap_templates import ThemeSwitchAIO
import dash

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server

tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {
        "yanchor": "top",
        "y": 0.9,
        "xanchor": "left",
        "x": 0.1,
        "title": {"text": None},
        "font": {"color": "white"},
        "bgcolor": "rgba(0,0,0,0.5)"
    },
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": False, "showTips": False}
template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

df = pd.read_csv('data\\dados_sensores.csv')
df['Data_Coleta'] = pd.to_datetime(df['Data_Coleta'])

ultima_data = df['Data_Coleta'].max().normalize()
ultimos_7_dias = [(ultima_data - pd.Timedelta(days=i)).date() for i in range(7)]

options_placa = [{'label': i, 'value': i} for i in df['placa'].unique()]
options_dias = [{'label': dia.strftime('%d/%m'), 'value': dia.isoformat()} for dia in sorted(ultimos_7_dias)]
options_dias.insert(0, {'label': 'Últimos 7 Dias', 'value': 'todos'})


def day_filter(dia_str):
    df['Data_Coleta'] = pd.to_datetime(df['Data_Coleta'])  # Garante conversão correta
    if dia_str == 'todos':
        ultima_data = df['Data_Coleta'].max().normalize()
        sete_dias_atras = ultima_data - pd.Timedelta(days=6)
        mask = (df['Data_Coleta'] >= sete_dias_atras) & (df['Data_Coleta'] <= ultima_data)
    else:
        dia = pd.to_datetime(dia_str).date()
        mask = df['Data_Coleta'].dt.date == dia
    return mask



app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([html.Legend("AgroTech")], sm=8),
                        dbc.Col([
                            html.Img(src="assets\\images\\logo.png", style={'width': '100%', 'maxHeight': '100px'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])])
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(dbc.Col([
                        html.H4('Previsão de Próxima Irrigação'),
                        html.Div(id='previsaoIrrigacao', style={'text-align': 'center', 'margin-top': '20px'}, className='dbc')
                    ])),
                    dbc.Row(dbc.Col([
                        html.Div(id='previsaoUmidade', style={'text-align': 'center', 'margin-top': '20px'}, className='dbc')
                    ]))
                ])
            ], style=tab_card)
        ], sm=12, lg=5),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(dbc.Col([
                        html.H4('Clima Atual'),
                        html.Div(id='temperatura', style={'text-align': 'center', 'margin-top': '20px'}, className='dbc')
                    ])),
                    dbc.Row(dbc.Col([
                        html.Div(id='descricao', style={'text-align': 'center', 'margin-top': '5px'}, className='dbc')
                    ]))
                ])
            ], style=tab_card)
        ], sm=12, lg=4)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Sensores ao Longo do Tempo"),
                    dcc.Graph(id='graph1', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=8),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(dbc.Col([
                        html.H5('Escolha o Dia'),
                        dbc.RadioItems(
                            id="radio-dia",
                            options=options_dias,
                            value='todos',
                            inline=True,
                            labelCheckedClassName="text-success",
                            inputCheckedClassName="border border-success bg-success"
                        ),
                        html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                    ]))
                ])
            ], style=tab_card)
        ], sm=12, lg=4)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Umidade ao Longo do Tempo"),
                    dcc.Graph(id='graph2', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Umidade ao Longo do Tempo"),
                    dcc.Graph(id='graph3', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=4),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha a Placa'),
                    dbc.RadioItems(
                        id="radio-team",
                        options=options_placa,
                        value=df['placa'].unique()[0],
                        inline=True,
                        labelCheckedClassName="text-warning",
                        inputCheckedClassName="border border-warning bg-warning"
                    ),
                    html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '100vh'})


@app.callback(
    Output('previsaoIrrigacao', 'children'),
    Output('previsaoUmidade', 'children'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def valorPrevisao(filtro, value):
    qtde_dias, umidade = previsaoSensores(filtro)
    return html.P(qtde_dias, style={'font-size': '24px'}), html.P(umidade, style={'font-size': '24px'})


@app.callback(
    Output('temperatura', 'children'),
    Output('descricao', 'children'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def valoresClima(value):
    temperatura, descricao = informacoesTempo()
    return html.P(temperatura, style={'font-size': '24px'}), html.P(descricao, style={'font-size': '24px'})


@app.callback(
    Output('graph1', 'figure'),
    Input('radio-dia', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph10(dia, placa, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = day_filter(dia)
    df_filtrado = df.loc[mask]
    mask_placa = placa_filter(placa, df_filtrado)
    df_3 = df_filtrado.loc[mask_placa]

    df_legenda = df_3.rename(columns={
        'Temperatura_Ambiente': 'Temperatura Ambiente',
        'Umidade_Ambiente': 'Umidade Ambiente',
        'Umidade_Solo': 'Umidade Solo'
    })

    fig = px.line(
        df_legenda,
        x='Data_Coleta',
        y=['Temperatura Ambiente', 'Umidade Ambiente', 'Umidade Solo'],
        labels={'value': 'Valor', 'variable': 'Sensor'},
        color_discrete_map={
            'Temperatura Ambiente': 'orange',
            'Umidade Ambiente': 'skyblue',
            'Umidade Solo': 'green'
        },
        line_shape='spline'
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=200,
        template=template,
        showlegend=True
    )
    fig.update_layout(main_config)
    return fig


@app.callback(
    Output('graph2', 'figure'),
    Input('radio-dia', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph_umidade(dia, placa, toggle):
    template = template_theme1 if toggle else template_theme2

    print(dia)
    mask = day_filter(dia)
    df_filtrado = df.loc[mask]

    mask_placa = placa_filter(placa, df_filtrado)
    df_filtrado = df_filtrado.loc[mask_placa]

    df_agg = df_filtrado.groupby('Data_Coleta')['Umidade_Solo'].mean().reset_index()

    fig = go.Figure(go.Scatter(
        x=df_agg['Data_Coleta'],
        y=df_agg['Umidade_Solo'],
        mode='lines',
        fill='tonexty',
        name='Umidade do Solo'
    ))

    fig.add_annotation(
        text='Umidade do Solo por Dia',
        xref="paper", yref="paper",
        font=dict(size=17, color='gray'),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False
    )
    fig.add_annotation(
        text=f"Média: {round(df_agg['Umidade_Solo'].mean(), 2)}%",
        xref="paper", yref="paper",
        font=dict(size=20, color='gray'),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False
    )

    fig.update_layout(main_config, height=180, template=template)

    return fig


@app.callback(
    Output('graph3', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph_distribuicao_umidade(placa, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = placa_filter(placa, df)
    df_3 = df.loc[mask]

    fig = px.histogram(
        df_3,
        x='Umidade_Solo',
        nbins=30,
        color_discrete_sequence=['#4CAF50']
    )

    fig.update_layout(
        xaxis_title='Umidade do Solo (%)',
        yaxis_title='Nº de Registros',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template=template,
        height=200,
        bargap=0.05,
        margin={"l": 30, "r": 10, "t": 10, "b": 30}
    )

    fig.update_traces(marker_line_width=0.5, marker_line_color="black")

    return fig


@app.callback(
    Output('month-select', 'children'),
    Input('radio-dia', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def update_dia_label(dia, toggle):
    if dia == 'todos':
        return html.H5("Últimos 7 Dias")
    else:
        data = pd.to_datetime(dia)
        return html.H5(f"{data.strftime('%d/%m/%Y')}")


@app.callback(
    Output('team-select', 'children'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def update_team_label(team, toggle):
    return html.H5(f"{team}")


if __name__ == '__main__':
    app.run(debug=True, port=8080)
