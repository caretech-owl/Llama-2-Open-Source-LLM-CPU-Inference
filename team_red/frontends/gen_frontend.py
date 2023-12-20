import logging
from typing import Iterable, Tuple

import gradio as gr
import difflib as dl
import re

from team_red.backend import TRANSPORTER

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())

_field_labels = {
    "history": "Patientengeschichte",
    "doctor_name": "Name des behandelnden Hausarztes",
    "patient_name": "Name des Patienten",
    "hospital": "Name des Krankenhauses",
}

logging.basicConfig(level=logging.DEBUG)


def _pairwise(
    fields: Tuple[gr.Textbox, ...]
) -> Iterable[Tuple[gr.Textbox, gr.Textbox, gr.Textbox]]:
    a = iter(fields)
    return zip(a, a, a)


def generate(*fields: gr.Textbox) -> str:
    params = {}
    for key, name, value in _pairwise(fields[3:]):
        if not value:
            msg = f"Feld '{name}' darf nicht leer sein!"
            raise gr.Error(msg)
        params[key] = value
    response = TRANSPORTER.generate(params)
    return [response.text, response.text]


def set_hasEdited(state: gr.State) -> bool:
    state = True
    return state


def get_sentence_difference(str1: str, str2: str) -> str:
    d = dl.Differ()
    sentences1 = re.split('(?<=[,.!?:;]) +', str1)
    sentences2 = re.split('(?<=[,.!?:;]) +', str2)
    diff = list(d.compare(sentences1, sentences2))
    same = []
    added = []
    for i in diff:
        if i[0] == ' ':
            same.append(i[2:])
        elif i[0] == '+':
            added.append(i[2:])
    same = ' '.join(same)
    added = ' '.join(added)
    return added


def rephrase(*fields) -> str:
    params = {}
    connect = "These notes have been added. Connect them to the previous text."
    for key, name, value in _pairwise(fields[3:]):
        if not value:
            msg = f"Feld '{name}' darf nicht leer sein!"
            raise gr.Error(msg)
        params[key] = value

    params['history'] += connect + get_sentence_difference(fields[1], fields[2])

    response = TRANSPORTER.generate(params)
    return [response.text, response.text]


def generate_handler(*fields: gr.Textbox) -> str:
    if fields[0]:
        return rephrase(*fields)
    else:
        return generate(*fields)
    

demo = gr.Blocks()

with demo:
    config = TRANSPORTER.get_gen_prompt()

    gr.Markdown("# Entlassbrief generieren")

    has_edited = gr.State(False)
    old_history = gr.State("")
    
    fields = []
    for key in config.parameters:
        fields.append(gr.Textbox(key, visible=False))
        fields.append(gr.Textbox(_field_labels.get(key, key), visible=False))
        fields.append(gr.Textbox(label=_field_labels.get(key, key)))
    output = gr.TextArea(label="Dokument", interactive=True)
    submit_button = gr.Button("Generiere Dokument")
    output.input(fn=set_hasEdited, inputs=has_edited, outputs=has_edited)
    submit_button.click(fn=generate_handler,
                        inputs=[has_edited] + [old_history] + [output] + fields,
                        outputs=[output, old_history])


if __name__ == "__main__":
    demo.launch()
