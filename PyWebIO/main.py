import pywebio
from pywebio.input import textarea, slider, input_group, input
from pywebio.output import put_text, put_button, put_loading, put_markdown
from pywebio.session import run_js

import os
import requests
import json


async def generate_poem(data):
    api_add = os.environ.get('GENERATION_API_ADDR', 'localhost')
    api_port = os.environ.get('GENERATION_API_PORT', '8000')
    poem = requests.post(url=f"http://{api_add}:{api_port}/", json=data, timeout=8000)
    if poem.status_code != 200:
        print(poem.status_code)
        return ["Algo malo ocurrió :(, por favor, intentalo de nuevo más tarde"]

    generated = json.loads(poem.text)
    return generated["generated"]

async def main():
    data = await input_group("Ailan Poem - Por David Leirado", [
        input("Tu nombre", name="name"),
        textarea("Aquí el comienzo de un poema", rows=1, placeholder="Empezamos el poema\neso es una cosa buena\nescribe un input ",
                 name="text"),
        slider("Top P", value=0.8, min_value=0.1, max_value=1.0, name="top_p"),
        slider("Temperature", value=1.0, min_value=0.1, max_value=2.0, name="temperature"),
        slider("Poem Length", value=80, min_value=40, max_value=125, step=10, name="entry_length")
    ])

    data["entry_count"] = 1

    with put_loading():
        put_text("Este proceso puede llevar unos minutos, espere por favor")
        put_text("Su poema está siendo generado por GTP-2, un modelo de 1'5 billones de parámetros")
        generated = await generate_poem(data)

    put_markdown("# Su Poema Generado")
    for poem in generated:
        poem = poem.replace("<|endoftext|>", ".")
        poem = poem.replace("\n\n", "\n")
        put_text(poem)

    put_button("Volver a generar!", onclick=lambda: run_js('window.location.reload()'))

if __name__ == '__main__':
    pywebio.start_server(main, port=8081, debug=bool(int(os.environ.get("DEBUG", 1))), host="0.0.0.0", allowed_origins=["*"])
