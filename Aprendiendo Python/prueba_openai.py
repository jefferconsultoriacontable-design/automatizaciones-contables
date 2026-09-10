from openai import OpenAI

client = OpenAI()

respuesta = client.responses.create(
    model="gpt-5.6-luna",
    input="Explícame qué es una conciliación bancaria en términos sencillos."
)

print(respuesta.output_text)

from pandas import pandas
