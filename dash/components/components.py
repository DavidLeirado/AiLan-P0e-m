from dash import html, dcc, Input, Output, State
from styles.styles import *


def sliders(label, description, min, max, step, marks, value, id_name):
    br = html.Br()
    label = html.Label(label)
    desc = html.P(description, className="description")
    slider = dcc.Slider(id=id_name, min=min, max=max, step=step, marks={i: str(i) for i in marks}, value=value)
    return [br, label, desc, slider]


low_marks = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
generations = [1, 2, 3, 4, 5]
high_marks = [20, 30, 40, 50, 60]

top_p_slider = sliders("Top P", top_p_description, 0.1, 1.0, 0.1, low_marks, 0.8, "top-p")
temperature_slider = sliders("Temperature", temperature_description, 0.1, 1.0, 0.1, low_marks, 1.0, "temp")
output_length = sliders("Poem Length", output_len_description, 20, 60, 10, high_marks, 30, "poem-length")
options_number = sliders("Number of poems", options_num_description, 1, 5, 1, generations, 1, "n-poems")

sliders_elements = top_p_slider + temperature_slider + output_length + options_number

header = html.Div(style=header_style, children=[
    html.H1(children='AiLan-P03m', style=header_text_style)
    ])

subheader = html.Div(children=[
    html.H2('Generador de poemas basado en Transformers')], style=div_header_child_style)

body = html.Div([
    html.Div(children=sliders_elements, style=inputs_div_style, id="inputs-left"),
    html.Div(children=[
        html.Label('Fragmento de input'),
        html.P(className="description", children="Insertar el fragmento de poesía a partir del cual al modelo hará la generación"),
        dcc.Textarea(style=text_area, id="input-text",
                     value="Esto es un ejemplo\ndel input que debes dar\nsustituye estas líneas\npor tu poema")
    ], style=inputs_div_style, id="inputs-right")
], style=body_style)

button = html.Div(style=under_div_style, children=[
    html.Button("Generar", id="submit-button", n_clicks=0),
])

footer = dcc.Loading(children=html.Div(id="my-poems", style=footer_style), type="graph", fullscreen=False)
