from dash import Dash, html
from components.components import *


app = Dash(__name__)

app.layout = page

if __name__ == '__main__':
    app.run_server(debug=True)
