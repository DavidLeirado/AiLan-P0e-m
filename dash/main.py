from dash import Dash, html, dcc, Output, Input, State
from styles.styles import *

app = Dash(__name__)


def sliders(label, min, max, step, marks, value, id_name):
    br = html.Br()
    label = html.Label(label)
    slider = dcc.Slider(id=id_name, min=min, max=max, step=step, marks={i: str(i) for i in marks}, value=value)
    return [br, label, slider]


low_marks = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
generations = [1, 2, 3, 4, 5]
high_marks = [20, 30, 40, 50, 60]

top_p_slider = sliders("Top_P", 0.1, 1.0, 0.1, low_marks, 0.8, "top-p")
temperature_slider = sliders("Temperature", 0.1, 1.0, 0.1, low_marks, 1.0, "temp")
output_length = sliders("Poem Length", 20, 60, 10, high_marks, 30, "poem-length")
options_number = sliders("Number of poems", 1, 5, 1, generations, 1, "n-poems")

sliders_elements = top_p_slider + temperature_slider + output_length + options_number

header = html.Div(style=header_style, children=[
    html.H1(children='GENERADOR DE POESÍAS', style=header_text_style),
    html.Div(children='Un modelo entrenado por David Leirado Maroto', style=div_header_child_style)
])

body = html.Div([
    html.Div(children=sliders_elements, style={'padding': 50, 'flex': 1}),
    html.Div(children=[
        html.Label('Fragmento de input'),
        dcc.Textarea(style=text_area)
    ], style={'padding': 50, 'flex': 1})
], style=body_style)

button = html.Div(style=under_div_style, children=[
    html.Button("Generar", id="submit-button", style=button_style, n_clicks=0),
])

footer = html.Div(id="my-poems")


@app.callback(
    Output('my-poems', 'children'),
    Input('submit-button', 'n_clicks'),
    State('top-p', 'value'),
    State('temp', 'value'),
    State('poem-length', 'value'),
    State('n-poems', 'value')
)
def generate_poems(n_clicks, top_p, temp, poem_length, n_poems):
    string = f"{top_p}, {temp}, {poem_length}, {n_poems}"
    return string


components = [header, body, button, footer]

page = html.Div(children=components, style={'color': "#111111", "heigth": "100vh", "width": "100vw"})

app.layout = page

if __name__ == '__main__':
    app.run_server(debug=True)
