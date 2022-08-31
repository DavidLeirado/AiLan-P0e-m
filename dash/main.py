import json

import requests
from dash import Dash
from dash.exceptions import PreventUpdate

from components.components import *

app = Dash(__name__)


@app.callback(
    Output('my-poems', 'children'),
    Input('submit-button', 'n_clicks'),
    State('top-p', 'value'),
    State('temp', 'value'),
    State('poem-length', 'value'),
    State('n-poems', 'value'),
    State('input-text', 'value')
)
def generate_poems(n_clicks, top_p, temp, poem_length, n_poems, text):
    if n_clicks == 0:
        raise PreventUpdate

    gen_request_data = {
        "text": text,
        "entry_count": n_poems,
        "entry_length": poem_length,
        "temperature": temp,
        "top_p": top_p
    }
    res = requests.post("http://api:8000", json=gen_request_data)
    returning = []
    for response_poem in json.loads(res.text)["generated"]:
        poem = []
        for i in response_poem.split("\n"):
            poem.append(i)
            poem.append(html.Br())
        poem.pop()
        returning.append(html.Div(html.P(children=poem), className="poem-generated", style={"animation-name":"fade"}))
    return returning


components = [header, subheader, body, button, footer]

page = html.Div(children=components, style={'color': "#111111", "heigth": "100%", "width": "100%"})

app.layout = page

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
