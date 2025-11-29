from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

# -------------------------------
# Função de formatar CNPJ
# -------------------------------
def formatar_cnpj(cnpj):
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    
    if len(cnpj_limpo) != 14:
        return cnpj_limpo
    
    return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"

# -------------------------------
# Função de consulta ao banco
# -------------------------------
def buscar_cnpj_banco(cnpj_input):
    cnpj = ''.join(filter(str.isdigit, cnpj_input))
    
    if len(cnpj) != 14:
        return None

    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="Dados_RFB",
            user="postgres",
            password=""
        )
        cur = conn.cursor()

        query = """
            SELECT
                e.cnpj_basico || e.cnpj_ordem || e.cnpj_dv AS cnpj,
                em.razao_social,
                e.situacao_cadastral,
                e.logradouro,
                e.numero,
                e.bairro,
                e.cep,
                e.municipio,
                e.uf
            FROM estabelecimento e
            JOIN empresa em
                ON em.cnpj_basico = e.cnpj_basico
            WHERE (e.cnpj_basico || e.cnpj_ordem || e.cnpj_dv) = %s;
        """

        cur.execute(query, (cnpj,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            return None

        cnpj, nome, status, logradouro, numero, bairro, cep, municipio, uf = row

        return {
            "cnpj": formatar_cnpj(cnpj),
            "nome": nome,
            "situacao": status,
            "endereco": f"{logradouro}, {numero}, {bairro}",
            "cep": cep,
            "municipio": municipio,
            "uf": uf,
            "ativa": status == "02"
        }
    
    except Exception as e:
        print(f"Erro no banco de dados: {e}")
        return None

# -------------------------------
# Rota para servir o HTML com nome correto
# -------------------------------
@app.route("/")
def index():
    # Verifica se o arquivo Index.html existe e usa ele
    templates_dir = os.path.join(app.root_path, 'templates')
    index_upper = os.path.join(templates_dir, 'Index.html')
    index_lower = os.path.join(templates_dir, 'index.html')
    
    if os.path.exists(index_upper):
        return render_template("Index.html")
    elif os.path.exists(index_lower):
        return render_template("index.html")
    else:
        return "Arquivo Index.html não encontrado na pasta templates", 404

# -------------------------------
# Rota de consulta (POST)
# -------------------------------
@app.route("/consultar", methods=["POST"])
def consultar():
    dados = request.json
    cnpj = dados.get("cnpj", "")

    resultado = buscar_cnpj_banco(cnpj)

    if not resultado:
        return jsonify({"erro": "CNPJ não encontrado"}), 404

    return jsonify(resultado)

# -------------------------------
# Inicialização do Flask
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)