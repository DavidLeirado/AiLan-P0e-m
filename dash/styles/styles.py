colors = {
    'header_background': '#424242',
    'body_background': '#FFFFFF',
    'text': '#FFFFFF',
    'input_divs': '#EDEDED'
}

borders = {
    'body_borders': f"2px solid {colors['header_background']}"
}
fonts = ["Montserrat", "Helvetica"]

header_style = {'backgroundColor': colors['header_background'], 'font-family': fonts, "padding": 15}
header_text_style = {'textAlign': 'center', 'color': colors['text'], 'font-family': ["Copperplate Gothic", "Helvetica"], "font-size":58}
inputs_div_style = {'padding': 50, 'flex': 1, 'margin':5,}
div_header_child_style = {'textAlign': 'center', 'padding':5, 'font-family':["Copperplate Gothic", "Helvetica"], "font-size":"12px"}
text_area = {'width': '90%', 'height': 300, 'box-shadow':'2px 2px 5px', 'font-family':fonts, 'padding':20, 'margin':5, "text-align":"center"}
body_style = {'display': 'flex', 'flex-direction': 'row', 'font-family': fonts, 'background': colors["body_background"]}
footer_style = {'display': 'flex', 'flex-direction': 'row', 'font-family': fonts, 'background': colors["body_background"], "column-gap":"2%", "margin":"50px"}
under_div_style = {"height": "100%", "background": colors["body_background"], "textAlign":"center", "padding":20}

top_p_description = "Aumentar esta variable aumenta la variabilidad de los resultados, pero es más probable que pierda sentido"
temperature_description = "A menor temperatura, más se ciñe el resultado al tema. A mayor temperatura, mayor creatividad"
output_len_description = "El tamaño del poema generado"
options_num_description = "La cantidad de poemas a generar"
