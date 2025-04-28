from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json
from tensorflow.keras.models import model_from_json

Filepath = "C:/Users/user/OneDrive/Documentos/semestres uniandes/Clases 2025-1/Tesis IIND/Solo sector salud/Base analisis exploratorio.csv"
df=pd.read_csv(Filepath)

# Cargar modelo
with open('modelo_final_entrenado_json', 'r') as json_file:
    loaded_model_json = json_file.read()
modelo = model_from_json(loaded_model_json)

# (Aquí falta cargar los pesos si fueran necesarios)

# Inicializar app
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], suppress_callback_exceptions=True)

# Layout principal
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Predicción de Adición en Contratos Públicos", className="text-center text-light mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Tabs(id="tabs", value="tab1", children=[
                dcc.Tab(label="Entrada de Datos", value="tab1"),
                dcc.Tab(label="Resultados", value="tab2")
            ]),
            width=12
        )
    ]),

    # Contenido de la pestaña 1
    html.Div(id="tab1-content", children=[
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Label("Nombre Entidad:"),
                dcc.Dropdown(id="nombre_entidad", options=[{"label": i, "value": i} for i in df['nombre entidad'].unique()]),

                html.Br(),
                html.Label("NIT Entidad:"),
                dcc.Dropdown(id="nit_entidad", options=[{"label": i, "value": i} for i in df['nit entidad'].unique()]),

                html.Br(),
                html.Label("Departamento:"),
                dcc.Dropdown(id="departamento", options=[{"label": i, "value": i} for i in df['departamento'].unique()]),

                html.Br(),
                html.Label("Ciudad:"),
                dcc.Dropdown(id="ciudad", options=[{"label": i, "value": i} for i in df['ciudad'].unique()]),
            ], width=6),

            dbc.Col([
                html.Label("Orden:"),
                dcc.Dropdown(id="orden", options=[{"label": i, "value": i} for i in df['orden'].unique()]),

                html.Br(),
                html.Label("Rama:"),
                dcc.Dropdown(id="rama", options=[{"label": i, "value": i} for i in df['rama'].unique()]),

                html.Br(),
                html.Label("Entidad Centralizada:"),
                dcc.Dropdown(id="entidad_centralizada", options=[{"label": i, "value": i} for i in df['entidad centralizada'].unique()]),

                html.Br(),
                html.Label("Estado Contrato:"),
                dcc.Dropdown(id="estado_contrato", options=[{"label": i, "value": i} for i in df['estado contrato'].unique()]),

                html.Br(),
                html.Label("Código de Categoría Principal:"),
                dcc.Dropdown(id="codigo_categoria", options=[{"label": i, "value": i} for i in df['codigo de categoria principal'].unique()]),

                html.Br(),
                html.Label("Tipo de Contrato:"),
                dcc.Dropdown(id="tipo_contrato", options=[{"label": i, "value": i} for i in df['tipo de contrato'].unique()]),

                html.Br(),
                dbc.Button("Predecir", id="boton-predecir", color="primary", className="mt-3"),
            ], width=6)
        ])
    ], style={"display": "block"}),

    # Contenido de la pestaña 2
    html.Div(id="tab2-content", children=[
        html.Br(),
        dbc.Row([
            dbc.Col(html.H3("Resultado de la Predicción:", className="text-light mb-7 text-center"), width=12)
        ]),

        dbc.Row([
            dbc.Col(html.H1(id="resultado-prediccion", className="display-3 text-center"), width=12)
        ]),
    ], style={"display": "none"})
], fluid=True)

# Alternar pestañas
@app.callback(
    [Output("tab1-content", "style"), Output("tab2-content", "style")],
    [Input("tabs", "value")]
)
def alternar_pestanas(tab):
    if tab == "tab1":
        return {"display": "block"}, {"display": "none"}
    elif tab == "tab2":
        return {"display": "none"}, {"display": "block"}
    return {"display": "none"}, {"display": "none"}

# Predicción
@app.callback(
    Output("resultado-prediccion", "children"),
    [Input("boton-predecir", "n_clicks")],
    [
        State("nombre_entidad", "value"),
        State("nit_entidad", "value"),
        State("departamento", "value"),
        State("ciudad", "value"),
        State("orden", "value"),
        State("rama", "value"),
        State("entidad_centralizada", "value"),
        State("estado_contrato", "value"),
        State("codigo_categoria", "value"),
        State("tipo_contrato", "value"),
    ]
)
def predecir(n_clicks, nombre_entidad, nit_entidad, departamento, ciudad, orden, rama, entidad_centralizada, estado_contrato, codigo_categoria, tipo_contrato):
    if not n_clicks:
        raise PreventUpdate

    # (Aquí deberíamos transformar las entradas en el array que espera el modelo, usando dummies)
    # Por ahora, devolver "Modelo no entrenado todavía"

    return "(Predicción aquí)"

if __name__ == "__main__":
    app.run_server(debug=True)
