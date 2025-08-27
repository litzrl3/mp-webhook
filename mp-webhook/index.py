from flask import Flask, request, jsonify
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (para testes locais e para a Vercel)
load_dotenv()

app = Flask(__name__)

# Configura o Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# A rota agora é a raiz da API, que a Vercel expõe em /api
@app.route('/', methods=['POST'])
def handle_webhook():
    data = request.json
    print(f"Webhook recebido: {data}")

    if data and data.get("action") == "payment.updated":
        payment_id = data.get("data", {}).get("id")
        if payment_id:
            try:
                supabase.table('webhook_events').insert({
                    'mp_payment_id': int(payment_id),
                    'status': 'received'
                }).execute()
                print(f"Evento para o pagamento {payment_id} inserido na base de dados.")
            except Exception as e:
                print(f"Erro ao inserir na base de dados: {e}")
    
    return jsonify(success=True), 200

# Rota para verificar se o servidor está online (opcional)
@app.route('/', methods=['GET'])
def index():
    return "Servidor de Webhook está online."
