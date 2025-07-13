import dash
from dash import html, dcc
from collections import deque
import datetime
import dash_bootstrap_components as dbc

class Dashboard:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
        self.app.title = "Monitoramento de Sistema"

        self.dados_sensores = {}
        self.SENSOR_UNITS = {
            "Sensor CPU": "%",
            "Sensor Disco": "%",
            "Sensor Temperatura": "°C",
            "Sensor Tempo de Sistema": "s"
        }

        # --- Layout Principal do Dashboard ---
        self.app.layout = dbc.Container(
            [

                html.Div([
                    html.H1("Dashboard de Monitoramento de Sistema em Tempo Real", className="text-center text-light mt-4"),
                    html.P(
                        "Visualizando dados de sensores publicados via MQTT.",
                        className="text-center text-secondary mb-4"
                    )
                ]),
        
                html.Div(id="dashboard-content"),


                dcc.Interval(id="intervalo-atualizacao", interval=2000, n_intervals=0)
            ],
            fluid=True 
        )

        # --- Callback para atualizar todo o conteúdo do dashboard ---
        @self.app.callback(
            dash.dependencies.Output("dashboard-content", "children"),
            [dash.dependencies.Input("intervalo-atualizacao", "n_intervals")]
        )
        def atualizar_dashboard(n):
            if not self.dados_sensores:
                return html.Div(
                    dbc.Spinner(color="primary", children=[
                        html.H4("Aguardando recebimento de dados dos sensores...", className="text-center text-secondary mt-5")
                    ])
                )

            blocos_sensores = []

            for nome_sensor, dados in self.dados_sensores.items():
                
                
                ultimo_valor = dados['values'][-1] if dados['values'] else 0.0
                unidade = self.SENSOR_UNITS.get(nome_sensor, '')

                
                kpi_valor_formatado = f"{ultimo_valor:.1f} {unidade}"
                if nome_sensor == "Sensor Tempo de Sistema":

                    kpi_valor_formatado = datetime.datetime.fromtimestamp(ultimo_valor).strftime('%H:%M:%S')
                    unidade = "" 

                # --- Cria o Bloco do Sensor (KPI + Gráfico) ---
                bloco = dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row(
                                [

                                    dbc.Col(
                                        [
                                            html.H4(nome_sensor, className="card-title"),
                                            html.H2(kpi_valor_formatado, className="text-primary"),
                                            html.P("Última Leitura", className="text-muted"),
                                        ],
                                        md=3, 
                                        className="text-center my-auto"
                                    ),
                                    # Coluna do Gráfico
                                    dbc.Col(
                                        dcc.Graph(
                                            figure={
                                                "data": [{
                                                    "x": list(dados['timestamps']),
                                                    "y": list(dados['values']),
                                                    "type": "line",
                                                    "mode": "lines+markers",
                                                    "name": nome_sensor,
                                                    "line": {"color": "#00BFFF", "width": 3}, 
                                                    "marker": {"size": 6}
                                                }],
                                                "layout": {
                                                    "xaxis": {"showgrid": False, "color": "white"},
                                                    "yaxis": {"showgrid": True, "gridcolor": "#444", "color": "white", "title": unidade},
                                                    "plot_bgcolor": "rgba(0,0,0,0)",
                                                    "paper_bgcolor": "rgba(0,0,0,0)",
                                                    "height": 300, 
                                                    "margin": dict(l=40, r=20, t=20, b=40)
                                                }
                                            },
                                            config={'displayModeBar': False} 
                                        ),
                                        md=9, 
                                    ),
                                ],
                                align="center",
                            )
                        ]),
                        className="mb-4 shadow-sm", 
                    ),
                    width=12 
                )
                blocos_sensores.append(bloco)

            return html.Div(blocos_sensores)

    def adicionar_dado(self, nome_sensor, valor):
        """
        Adiciona um novo valor de um sensor. Chamado pelo subscriber MQTT.
        """
        if nome_sensor not in self.dados_sensores:
            self.dados_sensores[nome_sensor] = {
                'timestamps': deque(maxlen=30), 
                'values': deque(maxlen=30)
            }

        horario = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            valor_float = float(valor)
            self.dados_sensores[nome_sensor]['timestamps'].append(horario)
            self.dados_sensores[nome_sensor]['values'].append(valor_float)
        except (ValueError, TypeError):
            print(f"AVISO: Valor recebido do sensor '{nome_sensor}' não é numérico: '{valor}'. Ignorando.")

    def rodar(self):
        """ Inicia o servidor do dashboard. """
        self.app.run(debug=False, host='0.0.0.0', port=8050)
