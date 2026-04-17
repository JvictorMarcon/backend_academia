from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials, firestore
from auth import token_obrigatorio, gerar_token
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)

# Versão do OPEN API
app.config['SWAGGER'] = {
    'openapi' : '3.0.0'
}
# Chamar o OPENAPI para o código
swagger = Swagger(app, template_file = 'openapi.yaml')

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app, origins="*")
ADM_USUARIO = os.getenv("ADM_USUARIO")
ADM_SENHA = os.getenv("ADM_SENHA")

if os.getenv("VERCEL"):
    #ONLINE NA VERCEL
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_KEY")))

else:
    #LOCAL
    cred = credentials.Certificate("firebase.json")


firebase_admin.initialize_app(cred)

db = firestore.client()

#==============================
# Rotas Públicas
#==============================

# Rota incial
@app.route('/', methods = ['GET'])
def root():
    return jsonify({"api":"GYM",
                    "version":"1.0",
                    "authors":"João Victor and Guilherme"})
    
# Rota para verificar clientes
@app.route('/clientes', methods = ['GET'])
def buscar_clientes():
    clientes = []
    #Busca todos os dados da coleção "cliente" do Data Base
    lista = db.collection('clientes').stream() 
    
    for cliente in lista:
        dados = cliente.to_dict()
        clientes.append(dados)
    
    return jsonify(clientes), 200

#Rota para buscar cliente pelo cpf
@app.route('/clientes/<cpf>', methods = ['GET'])
def buscar_cliente_pelo_id(cpf):
    
    #Busca os dados da coleção "clientes" com filtro de cpf
    lista = db.collection('clientes').where('cpf', '==', cpf).stream()
    
    for cliente in lista:
        return jsonify(cliente.to_dict()),200
    
    return jsonify({"error":"Nenhum cliente com esse cpf encontrado"}),404
      
#=========================
# Rota de login para adm
#=========================
@app.route('/login',methods = ["POST"])
def login():
    dados = request.get_json()
    
    if not dados:
        return jsonify({"error":"Envie os dados para login"}), 400
    
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    
    if not usuario or not senha:
        return jsonify({"error":"Usuário e senha são obrigatórios"})
    
    if usuario == ADM_USUARIO and senha == ADM_SENHA:
        token = gerar_token(usuario)
        return jsonify({
            "message":"Login realizado com sucesso",
            "token": token
        }), 200
    return jsonify({"error":"Usuário ou senha inválido"}),401

#=======================
# Rotas Privadas
#=======================
#Rota para cadastrar um cliente
@app.route('/clientes', methods = ["POST"])
@token_obrigatorio
def adicionar_cliente():
    #Pegando os dados da requisição HTTP e guardando em "dados"
    dados = request.get_json()  
    #Verificando se o post de clientes irá ter nome e cpf
    if not dados or 'cpf' not in dados or 'nome' not in dados: 
        return jsonify({"error": "Dados inválidos ou faltando"}),400
    
    cpf_enviado = str(dados['cpf'])
    # 2. Forma mais simples e eficiente de verificar se o CPF existe
    # Fazemos uma query rápida apenas para esse CPF
    cliente_existente = db.collection('clientes').where('cpf', '==', cpf_enviado).get()

    if len(cliente_existente) > 0:
        return jsonify({"error": "Cliente com esse cpf já cadastrado"}), 400
    
    #Validação de CPF (Quantidade de caracteres)
    if len(cpf_enviado) != 11:
        return jsonify({"error": "O CPF deve conter exatamente 11 números"}),400
    #Busca pelo contador
    try:
        #Referenciando o contador no banco de dados
        contador_ref = db.collection("contador").document("controle_id")   
        #Armazenando o valor do contador
        contador_doc = contador_ref.get()
        #Tranformamos em dicionário e pegamos o valor guardado no campo "ultimo_id"
        ultimo_id = contador_doc.to_dict().get("ultimo_id")
        
        #Somar 1 ao ultimo id
        novo_id = ultimo_id + 1  
        #Atualiza o ultimo_id para o novo_id a fim de termos controle sobre quantos id's
        contador_ref.update({"ultimo_id": novo_id})
        
        #cadastrar novo cliente
        
        db.collection("clientes").add({
            "id" : novo_id,
            "cpf" : str(dados["cpf"]),
            "nome": dados['nome'],
            "status" : True
        })    
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201        
        
    except:
        return jsonify({"error": "Falha no cadastro do cliente"}), 400

#Rota para o método - PATCH - altera apenas algumas infomações
@app.route('/clientes/<cpf>', methods = ["PATCH"])
@token_obrigatorio
def editar_informacoes_cliente(cpf):
    dados = request.get_json()
    
    if not dados or ('nome' not in dados and 'status' not in dados and 'cpf' not in dados):
        return jsonify({"error":"Dados inválidos"}), 400
    if 'cpf' in dados:
            cpf_atual = dados["cpf"]    
            if len(cpf_atual) != 11:
                return jsonify({"error":"O CPF deve conter exatamente 11 números"})
    
    try:
        docs = db.collection("clientes").where("cpf","==",cpf).limit(1).get()
        if not docs:
            return jsonify({"error":"cliente não encontrado"}), 404
            
        doc_ref = db.collection("clientes").document(docs[0].id)
        update_cliente = {}
        if "nome" in dados:
            update_cliente["nome"] = dados["nome"]
        if "cpf" in dados:
           update_cliente["cpf"] = dados["cpf"]
        if "status" in dados:
            update_cliente["status"] = dados["status"]
            
           
        
        doc_ref.update(update_cliente)
           
        return jsonify({"message": "cliente alterado com sucesso"}), 200
    except:
        return jsonify({"error": "Falha na alteração do cliente"}), 400

#Rota para o método DELETE
@app.route('/clientes/<int:cpf>', methods = ['DELETE'])
@token_obrigatorio
def deletar_cliente(cpf): 
    
    docs = db.collection("clientes").where("cpf", "==", str(cpf)).limit(1).get()
    
    if not docs:
        return jsonify({"error": f"Cliente com CPF {cpf} não encontrado"}), 404
    
    try:
        # 3. Pegamos o ID do documento (a chave alfanumérica do Firestore)
        doc_id = docs[0].id
        
        # 4. Deletamos o documento usando esse ID
        db.collection("clientes").document(doc_id).delete()
        
        return jsonify({"message": "Cliente excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar exclusão: {str(e)}"}), 500

    

#=====================================
# Rotas de tratamento de erros
#=====================================
    

@app.errorhandler(404)
def erro404(error):
    return jsonify({"error": "URL não encontrada"}), 404
   
@app.errorhandler(500)
def erro500(error):
    return jsonify({"error": "Servidor interno com falhas. Tente mais tarde"}) 

if __name__ == "__main__":
    app.run(debug=True)