from flask import Flask, request, jsonify
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (para testes locais)
load_dotenv()

app = Flask(__name__)

# Configura o Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/mp-webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    print(f"Webhook recebido: {data}") # Para depuração na Vercel

    # Verifica se é uma notificação de pagamento atualizado
    if data and data.get("action") == "payment.updated":
        payment_id = data.get("data", {}).get("id")
        if payment_id:
            try:
                # Insere um evento na tabela do Supabase para o bot processar
                supabase.table('webhook_events').insert({
                    'mp_payment_id': int(payment_id),
                    'status': 'received'
                }).execute()
                print(f"Evento para o pagamento {payment_id} inserido na base de dados.")
            except Exception as e:
                print(f"Erro ao inserir na base de dados: {e}")
    
    # Responde 200 OK para o Mercado Pago saber que recebemos
    return jsonify(success=True), 200

# Rota principal para verificar se o servidor está online
@app.route('/', methods=['GET'])
def index():
    return "Servidor de Webhook para o Bot de Vendas está online."