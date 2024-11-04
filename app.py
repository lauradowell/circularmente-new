import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure paths for templates and static files
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return "Hello, Circularmente!"

def obtener_recomendaciones(producto):
    prompt = (f"Soy un chatbot de reciclaje. "
              f"El usuario quiere reciclar o reemplazar: {producto}. "
              f"Explica al usuario cómo puede reciclar el producto y en qué contenedor. "
              f"Ofrece alternativas de upcycling, opciones eco-friendly, "
              f"sugerencias de marcas o métodos, y consejos sobre su uso.")

    # Define style and tone
    estilo_tono = ("El bot debe tener un tono amigable y accesible, "
                   "siempre buscando educar y empoderar al usuario sobre el reciclaje. "
                   "Es un asistente neutral en cuanto a género y tiene una personalidad optimista, "
                   "útil y proactiva.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": estilo_tono},  # Style and tone
                {"role": "system", "content": "Eres un chatbot de reciclaje."},
                {"role": "user", "content": prompt}
            ]
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        print(f"Error al obtener recomendaciones: {e}")
        return "Lo siento, no puedo proporcionar recomendaciones en este momento."

@app.route('/api/recomendar', methods=['POST'])
def recomendar():
    data = request.json
    producto = data.get('producto')
    
    if not producto:
        return jsonify({"error": "El campo 'producto' es necesario"}), 400

    recomendaciones = obtener_recomendaciones(producto)
    return jsonify({"recomendaciones": recomendaciones})

# Removed the duplicate hello route
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Use Heroku's PORT
    app.run(host='0.0.0.0', port=port)
