import pywebio
from pywebio.input import textarea, slider, input_group, input
from pywebio.output import put_text
import os

async def main():
    data = await input_group("Poems", [
        input("Tu nombre", name="name"),
        textarea("Aquí el comienzo de un poema", rows=1, placeholder="Empezamo el poema\neso es una cosa buena\n",
                 name="text"),
        slider("Top P", value=0.8, min_value=0.1, max_value=1.0, name="top_p"),
        slider("Temperature", value=0.8, min_value=0.1, max_value=2.0, name="temperature"),
        slider("Poem Length", value=250, min_value=100, max_value=500, name="entry_length")
    ])

    data["entry_count"] = 1
    print(data)
    put_text(data["text"])


if __name__ == '__main__':
    pywebio.start_server(main, port=8080, debug=bool(int(os.environ.get("DEBUG", 1))))
