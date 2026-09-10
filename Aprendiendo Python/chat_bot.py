from openai import OpenAI
client = OpenAI()

respuesta = client.chat.completions.create(
    model="gpt-4o-mini",  # o el modelo que estés usando
    messages=[{"role": "user", "content": "Hola"}]
)
print(respuesta.choices[0].message.content)