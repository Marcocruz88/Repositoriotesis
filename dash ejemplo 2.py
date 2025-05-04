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
Filepath = "C:/Users/user/OneDrive/Documentos/semestres uniandes/Clases 2025-1/Tesis IIND/Solo sector salud/Base analisis exploratorio sinnombre.csv"
df = pd.read_csv(Filepath)


# Cargar columnas del modelo
columns_filepath = "C:/Users/user/OneDrive/Documentos/semestres uniandes/Clases 2025-1/Tesis IIND/Solo sector salud/muestra dummies2.csv"
df_columns = pd.read_csv(columns_filepath)
columnas_modelo = df_columns.columns.tolist()

# Cargar modelo
modelo = XGBClassifier()
modelo.load_model('modelo_final_entrenado2.json')

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
        dbc.Alert(
            html.Span([
                "Por favor, rellena todos los campos con la información completa del contrato para obtener una predicción precisa.",
                html.Br(),
                "Posteriormente diríjase a la pestaña de resultados."
            ]),
            color="info",
            dismissable=False,
            className="text-center"
        ),

        html.Div(
            dbc.Button("🔄 Reiniciar", id="boton-reiniciar-individual-tab1", color="secondary", className="mt-4"),
            className="d-flex justify-content-end"
        ),

        html.Br(),

        # Fila 2
        dbc.Row([
            dbc.Col([
                html.Label("NIT Entidad:"),
                dcc.Dropdown(id="nit_entidad", options=[{"label": i, "value": i} for i in df['nit entidad'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Destino del Gasto:"),
                dcc.Dropdown(id="destino_gasto", options=[{"label": i, "value": i} for i in df['destino gasto'].dropna().unique()])
            ], width=6)
        ], className="mb-2"),

        # Fila 3
        dbc.Row([
            dbc.Col([
                html.Label("Departamento:"),
                dcc.Dropdown(id="departamento", options=[{"label": i, "value": i} for i in df['departamento'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Valor del Contrato:"),
                dcc.Input(id="valor_contrato", type="number", debounce=True, style={"width": "100%"})
            ], width=6)
        ], className="mb-2"),

        # Fila 4
        dbc.Row([
            dbc.Col([
                html.Label("Ciudad:"),
                dcc.Dropdown(id="ciudad", options=[{"label": i, "value": i} for i in df['ciudad'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Valor Pendiente de Pago:"),
                dcc.Input(id="valor_pendiente", type="text", debounce=True, style={"width": "100%"})
            ], width=6)
        ], className="mb-2"),

        # Fila 5
        dbc.Row([
            dbc.Col([
                html.Label("Orden:"),
                dcc.Dropdown(id="orden", options=[{"label": i, "value": i} for i in df['orden'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Estado BPIN:"),
                dcc.Dropdown(id="estado_bpin", options=[{"label": i, "value": i} for i in df['estado bpin'].dropna().unique()])
            ], width=6)
        ], className="mb-2"),

        # Fila 6
        dbc.Row([
            dbc.Col([
                html.Label("Rama:"),
                dcc.Dropdown(id="rama", options=[{"label": i, "value": i} for i in df['rama'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Año BPIN:"),
                dcc.Dropdown(id="anno_bpin", options=[{"label": i, "value": i} for i in sorted(df['anno bpin'].dropna().unique())])
            ], width=6)
        ], className="mb-2"),

        # Fila 7
        dbc.Row([
            dbc.Col([
                html.Label("Entidad Centralizada:"),
                dcc.Dropdown(id="entidad_centralizada", options=[{"label": i, "value": i} for i in df['entidad centralizada'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("¿Contrato Prorrogable?"),
                dcc.Dropdown(id="puede_prorrogar", options=[{"label": i, "value": i} for i in df['el contrato puede ser prorrogado'].dropna().unique()])
            ], width=6)
        ], className="mb-2"),

        # Fila 8
        dbc.Row([
            dbc.Col([
                html.Label("Estado Contrato:"),
                dcc.Dropdown(id="estado_contrato", options=[{"label": i, "value": i} for i in df['estado contrato'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Fase:"),
                dcc.Dropdown(id="fase", options=[{"label": i, "value": i} for i in df['fase'].dropna().unique()])
            ], width=6)
        ], className="mb-2"),

        # Fila 9
        dbc.Row([
            dbc.Col([
                html.Label("Código de Categoría Principal:"),
                dcc.Dropdown(id="codigo_categoria", options=[{"label": i, "value": i} for i in sorted(df['codigo de categoria principal'].dropna().unique())])
            ], width=6),
            dbc.Col([
                html.Label("Precio Base:"),
                dcc.Input(id="precio_base", type="text", debounce=True, style={"width": "100%"})
            ], width=6)
        ], className="mb-2"),

        # Fila 10
        dbc.Row([
            dbc.Col([
                html.Label("Tipo de Contrato:"),
                dcc.Dropdown(id="tipo_contrato", options=[{"label": i, "value": i} for i in df['tipo de contrato'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Unidad de Contratación:"),
                dcc.Dropdown(id="unidad_contratacion", options=[{"label": i, "value": i} for i in df['nombre de la unidad de contratación'].dropna().unique()])
            ], width=6)
        ], className="mb-2"),

        # Fila 11
        dbc.Row([
            dbc.Col([
                html.Label("Modalidad de Contratación:"),
                dcc.Dropdown(id="modalidad_contratacion", options=[{"label": i, "value": i} for i in df['modalidad de contratacion'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Departamento Proveedor:"),
                dcc.Dropdown(id="departamento_proveedor", options=[{"label": i, "value": i} for i in df['departamento proveedor'].dropna().unique()])
            ], width=6)
        ], className="mb-2"),

        # Fila 12
        dbc.Row([
            dbc.Col([
                html.Label("Justificación Modalidad de Contratación:"),
                dcc.Dropdown(id="justificacion_modalidad", options=[{"label": i, "value": i} for i in df['justificacion modalidad de contratacion'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Ciudad Proveedor:"),
                dcc.Dropdown(id="ciudad_proveedor", options=[{"label": i, "value": i} for i in df['ciudad proveedor'].dropna().unique()])
            ], width=6)
        ], className="mb-2"),

        # Fila 13
        dbc.Row([
            dbc.Col([
                html.Label("Condiciones de Entrega:"),
                dcc.Dropdown(id="condiciones_entrega", options=[{"label": i, "value": i} for i in df['condiciones de entrega'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Tiempo de Duración (días):"),
                dcc.Input(id="tiempo_duracion", type="text", debounce=True, style={"width": "100%"})
            ], width=6)
        ], className="mb-2"),

        # Fila 14
        dbc.Row([
            dbc.Col([
                html.Label("¿Es Pyme?"),
                dcc.Dropdown(id="es_pyme", options=[{"label": i, "value": i} for i in df['es pyme'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Duración del Proceso (días):"),
                dcc.Input(id="duracion_proceso", type="text", debounce=True, style={"width": "100%"})
            ], width=6)
        ], className="mb-2"),

        # Fila 15
        dbc.Row([
            dbc.Col([
                html.Label("¿Está Liquidado?"),
                dcc.Dropdown(id="liquidacion", options=[{"label": i, "value": i} for i in df['liquidación'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Año de Publicación:"),
                dcc.Dropdown(id="anio_publicacion", options=[{"label": i, "value": i} for i in sorted(df['año_publicacion'].dropna().unique())])
            ], width=6)
        ], className="mb-2"),

        # Fila 16
        dbc.Row([
            dbc.Col([
                html.Label("Origen de los Recursos:"),
                dcc.Dropdown(id="origen_recursos", options=[{"label": i, "value": i} for i in df['origen de los recursos'].dropna().unique()])
            ], width=6),
            dbc.Col([
                html.Label("Porcentaje Pagado:"),
                dcc.Dropdown(id="porcentaje_pagado", options=[{"label": i, "value": i} for i in df['porcentaje_pagado'].dropna().unique()])
            ], width=6)
        ], className="mb-2")

    ]),

    html.Div(id="tab2-content", children=[
        html.Br(),
        dbc.Row([
            dbc.Col(html.H3("Resultado de la Predicción:", className="text-light mb-4 text-center"), width=12)
        ]),
        
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("🔍 Predecir", id="boton-predecir", color="warning", size="lg", className="px-4 mb-2"),
                ], className="text-center"),
                width="auto",
                className="mx-auto"
            )
        ]),

        dbc.Row([
            dbc.Col(
                html.Div(
                    dbc.Button("🔄 Reiniciar", id="boton-reiniciar-individual", color="secondary"),
                    className="d-flex justify-content-end"
                ),
                width=12
            )
        ], className="mb-3"),

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
                className="d-flex justify-content-end"
            ),
            html.Div(id='output-table'),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Arrastra o haz click para cargar el archivo .xlsx'],style={"color": "#ffffff", "fontWeight": "bold"}),
                
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                    'textAlign': 'center', 'margin': '10px','backgroundColor': '#154360'
                },
                multiple=False
            )
        ])
    ])
], style={"display": "none"})
], fluid=True)

# Para alterar entre pestañas
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




# Callback para reiniciar todos los campos tipo Dropdown/Input en la pestaña de entrada individual (excepto los numéricos)
@app.callback(
    [Output("nit_entidad", "value"),
     Output("departamento", "value"),
     Output("ciudad", "value"),
     Output("orden", "value"),
     Output("rama", "value"),
     Output("entidad_centralizada", "value"),
     Output("estado_contrato", "value"),
     Output("codigo_categoria", "value"),
     Output("tipo_contrato", "value"),
     Output("modalidad_contratacion", "value"),
     Output("justificacion_modalidad", "value"),
     Output("condiciones_entrega", "value"),
     Output("es_pyme", "value"),
     Output("liquidacion", "value"),
     Output("origen_recursos", "value"),
     Output("destino_gasto", "value"),
     Output("estado_bpin", "value"),
     Output("anno_bpin", "value"),
     Output("puede_prorrogar", "value"),
     Output("fase", "value"),
     Output("unidad_contratacion", "value"),
     Output("departamento_proveedor", "value"),
     Output("ciudad_proveedor", "value"),
     Output("anio_publicacion", "value"),
     Output("porcentaje_pagado", "value")],
    Input("boton-reiniciar-individual-tab1", "n_clicks"),
    prevent_initial_call=True
)
def reiniciar_dropdowns(n_clicks):
    return [None] * 25

# Callback para ejecutar la predicción individual y mostrar mensaje de reinicio en la pestaña de resultados
@app.callback(
    Output("resultado-prediccion", "children"),
    [Input("boton-predecir", "n_clicks"),
     Input("boton-reiniciar-individual", "n_clicks")],
    [State("nit_entidad", "value"),
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

    # Lista de campos esperados
    nombres_inputs = [
        "nit_entidad", "departamento", "ciudad", "orden", "rama", "entidad_centralizada",
        "estado_contrato", "codigo_categoria", "tipo_contrato", "modalidad_contratacion", "justificacion_modalidad",
        "condiciones_entrega", "es_pyme", "liquidacion", "origen_recursos", "destino_gasto", "valor_contrato",
        "valor_pendiente", "estado_bpin", "anno_bpin", "puede_prorrogar", "fase", "precio_base",
        "unidad_contratacion", "departamento_proveedor", "ciudad_proveedor", "tiempo_duracion",
        "duracion_proceso", "anio_publicacion", "porcentaje_pagado"
    ]

    datos_dict = dict(zip(nombres_inputs, inputs))

    # Validar que no haya campos vacíos
    if any(v is None or v == '' for v in datos_dict.values()):
        return dbc.Alert("⚠️ Por favor completa todos los campos.", color="warning")

    # Función para convertir valores con comas a float
    def convertir_a_float(valor):
        if valor is None:
            return 0.0
        if isinstance(valor, (int, float)):
            return float(valor)
        try:
            return float(str(valor).replace(",", "").replace(" ", "").strip())
        except ValueError:
            return 0.0

    # Convertir campos numéricos a float
    campos_numericos = ["valor del contrato", "valor pendiente de pago", "precio base", "tiempo duracion (dias)", "duracion_proceso_dias"]
    
    # Crear DataFrame base con los datos del usuario
    df_input = pd.DataFrame([datos_dict])

   # Limpiar strings en campos no numéricos
    for col in df_input.columns:
        if col not in campos_numericos and df_input[col].dtype == object:
            df_input[col] = df_input[col].astype(str).str.strip().str.title()

    df_input.to_excel("debug_original_individual.xlsx", index=False)
    # Ahora sí: convertir a dummies

    df_input.rename(columns={
        "origen_recursos": "origen de los recursos",
        "destino_gasto": "destino gasto",
        "estado_contrato": "estado contrato",
        "codigo_categoria": "codigo de categoria principal",
        "departamento_proveedor": "departamento proveedor",
        "ciudad_proveedor": "ciudad proveedor",
        "fase": "fase",
        "justificacion_modalidad": "justificacion modalidad de contratacion",
        "modalidad_contratacion": "modalidad de contratacion",
        "unidad_contratacion": "nombre de la unidad de contratación",
        "tipo_contrato": "tipo de contrato"
    }, inplace=True)

    df_input_dummies = pd.get_dummies(df_input)
    df_input_dummies.to_excel("apenasdummies.xlsx", index=False)

    # Reindex para que tenga solo las columnas del modelo (asegura orden y consistencia)
    df_input_dummies = df_input_dummies.reindex(columns=columnas_modelo, fill_value=0)
    df_input_dummies.to_excel("apenasdummies2.xlsx", index=False)

   # 🔁 Reinsertar valores numéricos reales después del reindex
    mapa_campos_numericos = {
        "valor del contrato": "valor_contrato",
        "valor pendiente de pago": "valor_pendiente",
        "precio base": "precio_base",
        "tiempo duracion (dias)": "tiempo_duracion",
        "duracion_proceso_dias": "duracion_proceso",
        "año_publicacion": "anio_publicacion"  # ⬅️ este es clave por el tema de la tilde
    }

    for col_final, col_input in mapa_campos_numericos.items():
        if col_final in df_input_dummies.columns:
            df_input_dummies.at[df_input_dummies.index[0], col_final] = datos_dict[col_input]
        
    df_input_dummies = df_input_dummies.astype(int)
    df_input_dummies.to_excel("debug_dummies_individual.xlsx", index=False)

    # Realizar predicción
    X_pred = df_input_dummies.values
    probs = modelo.predict_proba(X_pred)[:, 1]
    probabilidad = round(probs[0], 3)
    prediccion_final = int(probabilidad >= 0.75)

    # Mostrar resultado
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

    # Gráfico tipo gauge
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

# Callback para cargar archivo Excel en la pestaña de revisión masiva, predecir y mostrar tabla de resultados
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

        df = df.applymap(lambda x: x.strip().title() if isinstance(x, str) else x)
        df_dummies = pd.get_dummies(df_numeric)
        df_dummies = df_dummies.reindex(columns=columnas_modelo, fill_value=0)
        df_dummies = df_dummies.astype(int)
        df_dummies.to_excel("debug_dummies_masivo.xlsx", index=False)




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