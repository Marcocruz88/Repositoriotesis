from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json
import base64
import io
from xgboost import XGBClassifier
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash import no_update, callback_context


# Cargar datos
Filepath = "C:/Users/user/OneDrive/Documentos/semestres uniandes/Clases 2025-1/Tesis IIND/Solo sector salud/Base analisis exploratorio.csv"
df = pd.read_csv(Filepath)

# Cargar columnas del modelo
columns_filepath = "C:/Users/user/OneDrive/Documentos/semestres uniandes/Clases 2025-1/Tesis IIND/Solo sector salud/muestra dummies.csv"
df_columns = pd.read_csv(columns_filepath)
columnas_modelo = df_columns.columns.tolist()

# Cargar modelo
modelo = XGBClassifier()
modelo.load_model('modelo_final_entrenado.json')

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
    dcc.Tab(label="Entrada de Datos-Caso Individual", value="tab1"),
    dcc.Tab(label="Resultados-Caso Individual", value="tab2"),
    dcc.Tab(label="Revisión Excel- Caso Multiple", value="tab3")  
]),
            width=12
        )
    ]),

    html.Div(id="tab1-content", children=[
        html.Br(),
        html.Div(
        dbc.Alert(
            html.Span([
                "Por favor, rellena todos los campos con la información completa del contrato para obtener una predicción precisa.",
                html.Br(),
                "Posteriormente diríjase a la pestaña de resultados."
            ]),
            color="info",
            dismissable=True,
            className="text-center"
        )
        
        ),
        dbc.Row([
            html.Div(
                dbc.Button("🔄 Reiniciar", id="boton-reiniciar-individual", color="secondary", className="mt-4"),
                className="text-center"
            ),
            dbc.Col([
                html.Label("Nombre Entidad:"),
                dcc.Dropdown(id="nombre_entidad", options=[{"label": i, "value": i} for i in df['nombre entidad'].dropna().unique()]),

                html.Br(),
                html.Label("NIT Entidad:"),
                dcc.Dropdown(id="nit_entidad", options=[{"label": i, "value": i} for i in df['nit entidad'].dropna().unique()]),

                html.Br(),
                html.Label("Departamento:"),
                dcc.Dropdown(id="departamento", options=[{"label": i, "value": i} for i in df['departamento'].dropna().unique()]),

                html.Br(),
                html.Label("Ciudad:"),
                dcc.Dropdown(id="ciudad", options=[{"label": i, "value": i} for i in df['ciudad'].dropna().unique()]),

                html.Br(),
                html.Label("Orden:"),
                dcc.Dropdown(id="orden", options=[{"label": i, "value": i} for i in df['orden'].dropna().unique()]),

                html.Br(),
                html.Label("Rama:"),
                dcc.Dropdown(id="rama", options=[{"label": i, "value": i} for i in df['rama'].dropna().unique()]),

                html.Br(),
                html.Label("Entidad Centralizada:"),
                dcc.Dropdown(id="entidad_centralizada", options=[{"label": i, "value": i} for i in df['entidad centralizada'].dropna().unique()]),

                html.Br(),
                html.Label("Estado Contrato:"),
                dcc.Dropdown(id="estado_contrato", options=[{"label": i, "value": i} for i in df['estado contrato'].dropna().unique()]),

                html.Br(),
                html.Label("Código de Categoría Principal:"),
                dcc.Dropdown(id="codigo_categoria", options=[{"label": i, "value": i} for i in sorted(df['codigo de categoria principal'].dropna().unique())]),

                html.Br(),
                html.Label("Tipo de Contrato:"),
                dcc.Dropdown(id="tipo_contrato", options=[{"label": i, "value": i} for i in df['tipo de contrato'].dropna().unique()]),

                html.Br(),
                html.Label("Modalidad de Contratación:"),
                dcc.Dropdown(id="modalidad_contratacion", options=[{"label": i, "value": i} for i in df['modalidad de contratacion'].dropna().unique()]),

                html.Br(),
                html.Label("Justificación Modalidad de Contratación:"),
                dcc.Dropdown(id="justificacion_modalidad", options=[{"label": i, "value": i} for i in df['justificacion modalidad de contratacion'].dropna().unique()]),

                html.Br(),
                html.Label("Condiciones de Entrega:"),
                dcc.Dropdown(id="condiciones_entrega", options=[{"label": i, "value": i} for i in df['condiciones de entrega'].dropna().unique()]),

                html.Br(),
                html.Label("¿Es Pyme?"),
                dcc.Dropdown(id="es_pyme", options=[{"label": i, "value": i} for i in df['es pyme'].dropna().unique()]),

                html.Br(),
                html.Label("¿Está Liquidado?"),
                dcc.Dropdown(id="liquidacion", options=[{"label": i, "value": i} for i in df['liquidación'].dropna().unique()]),

                
                
            ], width=6),

            dbc.Col([
                html.Br(),
                html.Label("Origen de los Recursos:"),
                dcc.Dropdown(id="origen_recursos", options=[{"label": i, "value": i} for i in df['origen de los recursos'].dropna().unique()]),

                html.Br(),
                html.Label("Destino del Gasto:"),
                dcc.Dropdown(
                    id="destino_gasto", 
                    options=[{"label": i, "value": i} for i in df['destino gasto'].dropna().unique()],
                    style={"marginBottom": "15px"}
                ),

                html.Label("Valor del Contrato:"),
                dcc.Input(
                    id="valor_contrato", 
                    type="text", 
                    debounce=True, 
                    style={"marginBottom": "15px"}
                ),

                html.Br(), html.Br(),
                html.Label("Valor Pendiente de Pago:"),
                dcc.Input(id="valor_pendiente", type="text", debounce=True),

                html.Br(), html.Br(),
                html.Label("Estado BPIN:"),
                dcc.Dropdown(id="estado_bpin", options=[{"label": i, "value": i} for i in df['estado bpin'].dropna().unique()]),

                html.Br(),
                html.Label("Año BPIN:"),
                dcc.Dropdown(id="anno_bpin", options=[{"label": i, "value": i} for i in sorted(df['anno bpin'].dropna().unique())]),

                html.Br(),
                html.Label("¿Contrato Prorrogable?"),
                dcc.Dropdown(id="puede_prorrogar", options=[{"label": i, "value": i} for i in df['el contrato puede ser prorrogado'].dropna().unique()]),

                html.Br(),
                html.Label("Fase:"),
                dcc.Dropdown(id="fase", options=[{"label": i, "value": i} for i in df['fase'].dropna().unique()]),

                html.Br(),
                html.Label("Precio Base:"),
                dcc.Input(id="precio_base", type="text", debounce=True),

                html.Br(), html.Br(),
                html.Label("Unidad de Contratación:"),
                dcc.Dropdown(id="unidad_contratacion", options=[{"label": i, "value": i} for i in df['nombre de la unidad de contratación'].dropna().unique()]),

                html.Br(),
                html.Label("Departamento Proveedor:"),
                dcc.Dropdown(id="departamento_proveedor", options=[{"label": i, "value": i} for i in df['departamento proveedor'].dropna().unique()]),

                html.Br(),
                html.Label("Ciudad Proveedor:"),
                dcc.Dropdown(id="ciudad_proveedor", options=[{"label": i, "value": i} for i in df['ciudad proveedor'].dropna().unique()]),

                html.Br(),
                html.Label("Tiempo de Duración (días):"),
                dcc.Input(id="tiempo_duracion", type="text", debounce=True),

                html.Br(), html.Br(),
                html.Label("Duración del Proceso (días):"),
                dcc.Input(id="duracion_proceso", type="text", debounce=True),

                html.Br(), html.Br(),
                html.Label("Año de Publicación:"),
                dcc.Dropdown(id="anio_publicacion", options=[{"label": i, "value": i} for i in sorted(df['año_publicacion'].dropna().unique())]),

                html.Br(),
                html.Label("Porcentaje Pagado:"),
                dcc.Dropdown(id="porcentaje_pagado", options=[{"label": i, "value": i} for i in df['porcentaje_pagado'].dropna().unique()]),

                
            ], width=6)
        ])
    ], style={"display": "block"}),

    html.Div(id="tab2-content", children=[
        html.Br(),
        dbc.Row([
            dbc.Col(html.H3("Resultado de la Predicción:", className="text-light mb-4 text-center"), width=12)
        ]),
        
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("🔍 Predecir", id="boton-predecir", color="warning", size="lg", className="px-4 mb-2"),
                    html.Br(),
                    dbc.Button("🔄 Reiniciar", id="boton-reiniciar-individual", color="secondary")
                ]),
                width="auto",
                className="mx-auto text-center"
            )
        ], justify="center", className="mb-3"),

        dbc.Row([
            dbc.Col(
                html.Div(id="resultado-prediccion", children=[
                    dbc.Alert("ℹ️ Aún no se ha realizado ninguna predicción. Completa todos los campos en la pestaña de entrada y haz clic en 'Predecir'.", 
                            id="mensaje-inicial", color="info", className="text-center")
                ]), 
                width=12
            )
        ]),
    ], style={"display": "none"}),

    html.Div(id="tab3-content", children=[
    html.Br(),

    html.Div([
        dbc.Alert(
            "Por favor, adjunte los datos de los contratos a predecir en un archivo .xlsx con la primera fila con el nombre de la variable.",
            id="mensaje-carga",
            color="info",
            className="text-center",
            is_open=True
        ),
        dbc.Alert(
            "✅ Archivo cargado correctamente.",
            id="mensaje-exito",
            color="success",
            className="text-center",
            is_open=False,
            dismissable=True
        ),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(
                dbc.Button("🔄 Reiniciar", id="boton-reiniciar-masiva", color="secondary", className="mt-2"),
                className="text-center"
            ),
            html.Div(id='output-table'),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Arrastra o haz click para cargar el archivo .xlsx']),
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                    'textAlign': 'center', 'margin': '10px'
                },
                multiple=False
            )
        ])
    ])
], style={"display": "none"})
], fluid=True)

# Alternar pestañas
@app.callback(
    [Output("tab1-content", "style"),
     Output("tab2-content", "style"),
     Output("tab3-content", "style")],
    Input("tabs", "value")
)
def alternar_pestanas(tab):
    return [
        {"display": "block"} if tab == "tab1" else {"display": "none"},
        {"display": "block"} if tab == "tab2" else {"display": "none"},
        {"display": "block"} if tab == "tab3" else {"display": "none"}
    ]

# Función para formatear números con comas
def formatear_miles(value):
    if value is None or value == '':
        return ''
    try:
        value_clean = str(value).replace(',', '')
        value_int = int(float(value_clean))
        return f"{value_int:,}"
    except:
        return value

# Callbacks de formateo
@app.callback(
    Output("valor_contrato", "value"),
    Input("valor_contrato", "value")
)
def actualizar_valor_contrato(value):
    return formatear_miles(value)

@app.callback(
    Output("valor_pendiente", "value"),
    Input("valor_pendiente", "value")
)
def actualizar_valor_pendiente(value):
    return formatear_miles(value)

@app.callback(
    Output("precio_base", "value"),
    Input("precio_base", "value")
)
def actualizar_precio_base(value):
    return formatear_miles(value)

@app.callback(
    Output("tiempo_duracion", "value"),
    Input("tiempo_duracion", "value")
)
def actualizar_tiempo_duracion(value):
    return formatear_miles(value)

@app.callback(
    Output("duracion_proceso", "value"),
    Input("duracion_proceso", "value")
)
def actualizar_duracion_proceso(value):
    return formatear_miles(value)


@app.callback(
    Output("resultado-prediccion", "children"),
    [Input("boton-predecir", "n_clicks"),
     Input("boton-reiniciar-individual", "n_clicks")],
    [State("nombre_entidad", "value"),
     State("nit_entidad", "value"),
     State("departamento", "value"),
     State("ciudad", "value"),
     State("orden", "value"),
     State("rama", "value"),
     State("entidad_centralizada", "value"),
     State("estado_contrato", "value"),
     State("codigo_categoria", "value"),
     State("tipo_contrato", "value"),
     State("modalidad_contratacion", "value"),
     State("justificacion_modalidad", "value"),
     State("condiciones_entrega", "value"),
     State("es_pyme", "value"),
     State("liquidacion", "value"),
     State("origen_recursos", "value"),
     State("destino_gasto", "value"),
     State("valor_contrato", "value"),
     State("valor_pendiente", "value"),
     State("estado_bpin", "value"),
     State("anno_bpin", "value"),
     State("puede_prorrogar", "value"),
     State("fase", "value"),
     State("precio_base", "value"),
     State("unidad_contratacion", "value"),
     State("departamento_proveedor", "value"),
     State("ciudad_proveedor", "value"),
     State("tiempo_duracion", "value"),
     State("duracion_proceso", "value"),
     State("anio_publicacion", "value"),
     State("porcentaje_pagado", "value")],
)

def manejar_prediccion(n_clicks_predecir, n_clicks_reiniciar, *inputs):
    ctx = callback_context
    if not ctx.triggered:
        return no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "boton-reiniciar-individual":
        return dbc.Alert(
            ["ℹ️ Aún no se ha realizado ninguna predicción.",
             html.Br(),
             "Completa todos los campos en la pestaña de entrada y haz clic en 'Predecir'."],
            color="info",
            className="text-center"
        )

    # Continuar con la predicción si fue el botón de predecir
    nombres_inputs = [
        "nombre_entidad", "nit_entidad", "departamento", "ciudad", "orden", "rama", "entidad_centralizada",
        "estado_contrato", "codigo_categoria", "tipo_contrato", "modalidad_contratacion", "justificacion_modalidad",
        "condiciones_entrega", "es_pyme", "liquidacion", "origen_recursos", "destino_gasto", "valor_contrato",
        "valor_pendiente", "estado_bpin", "anno_bpin", "puede_prorrogar", "fase", "precio_base",
        "unidad_contratacion", "departamento_proveedor", "ciudad_proveedor", "tiempo_duracion",
        "duracion_proceso", "anio_publicacion", "porcentaje_pagado"
    ]

    datos_dict = dict(zip(nombres_inputs, inputs))

    if any(v is None or v == '' for v in datos_dict.values()):
        return dbc.Alert("⚠️ Por favor completa todos los campos.", color="warning")

    for key in ["valor_contrato", "valor_pendiente", "precio_base", "tiempo_duracion", "duracion_proceso"]:
        datos_dict[key] = float(str(datos_dict[key]).replace(",", ""))

    df_input = pd.DataFrame([datos_dict])
    df_input_dummies = pd.get_dummies(df_input)
    df_input_dummies = df_input_dummies.reindex(columns=columnas_modelo, fill_value=0)

    X_pred = df_input_dummies.values
    probs = modelo.predict_proba(X_pred)[:, 1]
    probabilidad = round(probs[0], 3)
    prediccion_final = int(probabilidad >= 0.75)

    if prediccion_final == 1:
        color_card = "danger"
        icono = "❌"
        titulo = "Riesgo de Adición Detectado"
        mensaje = "Alto riesgo de adición presupuestal.\nRecomendamos revisión detallada del contrato."
    else:
        color_card = "success"
        icono = "✅"
        titulo = "Sin Riesgo de Adición"
        mensaje = "No se espera adición al contrato.\nBajo riesgo de cambios presupuestales."

    # Indicador tipo gauge
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probabilidad * 100,
        title={'text': "Probabilidad de Adición (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 25], 'color': '#d4edda'},
                {'range': [25, 50], 'color': '#fff3cd'},
                {'range': [50, 75], 'color': '#ffeeba'},
                {'range': [75, 100], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': probabilidad * 100
            }
        }
    ))

    return dbc.Card(
        dbc.CardBody([
            html.H1(icono, className=f"text-{color_card} text-center", style={"fontSize": "90px"}),
            html.H2(titulo, className=f"text-{color_card} text-center"),
            html.P(mensaje, className="text-center"),
            html.H4(f"Probabilidad estimada de adición: {probabilidad:.3f}", className=f"text-{color_card} text-center mt-4"),
            dcc.Graph(figure=gauge_fig)
        ]),
        color=color_card,
        inverse=True,
        className="mt-4"
    )

@app.callback(
    [Output('output-table', 'children'),
     Output('mensaje-carga', 'is_open'),
     Output('mensaje-exito', 'is_open')],
    [Input('upload-data', 'contents'),
     Input('boton-reiniciar-masiva', 'n_clicks')],
    [State('upload-data', 'filename')],
    prevent_initial_call=True
)
def manejar_carga_y_reinicio(contents, n_clicks_reiniciar, filename):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'boton-reiniciar-masiva':
        return None, True, False

    # Si se activó por carga de archivo
    if contents is None:
        return None, True, False

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))

    if df.empty:
        return dbc.Alert("El archivo está vacío o no tiene columnas.", color="warning"), False, False

    try:
        df_numeric = df.copy()
        for col in df_numeric.select_dtypes(include=['object']).columns:
            df_numeric[col] = df_numeric[col].astype(str)

        df_dummies = pd.get_dummies(df_numeric)
        df_dummies = df_dummies.reindex(columns=columnas_modelo, fill_value=0)

        X_pred = df_dummies.values
        probs = modelo.predict_proba(X_pred)[:, 1]
        preds = (probs >= 0.75).astype(int)

        df_resultado = df.copy()
        df_resultado['Probabilidad de Adición'] = np.round(probs, 3)
        df_resultado['Predicción'] = np.where(preds == 1, "Sí", "No")

        # Tabla estilizada
        header = [html.Th(col) for col in df_resultado.columns]
        rows = []
        for i in range(len(df_resultado)):
            fila = []
            for col in df_resultado.columns:
                valor = df_resultado.iloc[i][col]
                if col == "Predicción":
                    texto = "Sí" if valor == "Sí" else "No"
                    color = "#f8d7da" if texto == "Sí" else "#d4edda"
                    fila.append(html.Td(texto, style={"backgroundColor": color, "textAlign": "center"}))
                else:
                    fila.append(html.Td(str(valor)))
            rows.append(html.Tr(fila))

        tabla = dbc.Table(
            [html.Thead(html.Tr(header))] + [html.Tbody(rows)],
            striped=True, bordered=True, hover=True, responsive=True
        )

        return tabla, False, True

    except Exception as e:
        return dbc.Alert(f"Error procesando el archivo: {e}", color="danger"), False, False


# Correr app
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)