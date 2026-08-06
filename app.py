import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

CONTEXT = "Você é um especialista em manutenções residenciais e deve responder somente a este assunto"
error_message = ""

try:
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
except Exception as ex:
    error_message = f'Erro ao carregar o cliente Groq: {ex}'


@app.route("/")
def index():
    if len(error_message) == 0:
        return render_template("index.html")
    else:
        return {"message": error_message}


@app.route("/search")
def search():
    prompt = request.args.get("prompt")

    try:
        input_ia = f'{CONTEXT}: {prompt}'

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": input_ia
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return {
            "message": response.choices[0].message.content
        }
    except Exception as ex:
        print(f'Erro ao gerar resposta: {ex}')
        return {
            "message": "Ocorreu um erro ao processar sua solicitação."
        }
if __name__ == "__main__":
    app.run(debug=True)
