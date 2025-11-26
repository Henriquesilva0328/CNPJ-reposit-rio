import psycopg2

def buscar_cnpj(cnpj_input):
    # Remove tudo que não for número
    cnpj = ''.join(filter(str.isdigit, cnpj_input))
    # Conexão com o Postgres
    conn = psycopg2.connect(
        host="localhost",
        dbname="Dados_RF13.B",
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
        print("CNPJ não encontrado.")
        return

    cnpj, nome, status, logradouro, numero, bairro, cep, municipio, uf = row

    print("\n--- RESULTADO ---")
    print("CNPJ:", cnpj)
    print("Nome:", nome)
    print("Situação Cadastral:", status)
    print("Endereço:", f"{logradouro}, {numero}, {bairro}")
    print("CEP:", cep)
    print("Município (código):", municipio)
    print("UF:", uf)
    print("-----------------\n")


if __name__ == "__main__":
    cnpj_input = input("Digite o CNPJ: ")
    buscar_cnpj(cnpj_input)
