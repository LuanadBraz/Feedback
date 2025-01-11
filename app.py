# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

# Inicializando a aplicação Flask
app = Flask(__name__)
CORS(app)  # Para permitir requisições de outros domínios

# Configuração do banco de dados
db_config = {
    'host': 'localhost',   # ou '127.0.0.1'
    'user': 'root',        # Substitua com o usuário do seu banco de dados
    'password': '',        # Substitua com a senha do seu banco de dados
    'database': 'feedbacks_db'
}

# Função para conectar ao banco de dados MySQL
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Rota para obter todos os feedbacks
@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedbacks")
    feedbacks = cursor.fetchall()
    conn.close()
    return jsonify(feedbacks)

# Rota para adicionar um feedback
@app.route('/api/feedbacks', methods=['POST'])
def add_feedback():
    data = request.get_json()
    
    # Pegando os dados enviados no corpo da requisição
    username = data['username']
    level = data['level']
    area = data['area']
    feedback = data['feedback']
    date = datetime.now().strftime('%Y-%m-%d')  # Data atual formatada

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedbacks (date, username, level, area, feedback)
        VALUES (%s, %s, %s, %s, %s)
    """, (date, username, level, area, feedback))
    conn.commit()
    conn.close()

    return jsonify({"message": "Feedback adicionado com sucesso!"}), 201

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)