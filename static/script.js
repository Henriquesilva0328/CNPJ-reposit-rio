// Listener correto para o formulário
document.getElementById("consulta-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const cnpj = document.getElementById("cnpj").value;
    const cep = document.getElementById("cep").value;

    try {
        // Chamada ao backend Flask
        const resposta = await fetch("/consultar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cnpj: cnpj, cep: cep })
        });

        const data = await resposta.json();

        // Exibir resultado na tela
        const box = document.getElementById("resultado");
        box.style.display = "block";

        if (data.erro) {
            box.innerHTML = `<p style="color: red;"><strong>Erro:</strong> ${data.erro}</p>`;
        } else {
            box.innerHTML = `
                <h3>Dados da Empresa:</h3>
                <p><strong>CNPJ:</strong> ${data.cnpj}</p>
                <p><strong>Nome da empresa:</strong> ${data.nome}</p>
                <p><strong>Município:</strong> ${data.municipio}</p>
                <p><strong>Situação cadastral:</strong> ${data.situacao}</p>
                <p><strong>Status:</strong> ${data.ativa ? "Ativa" : "Inativa"}</p>
                <p><strong>Endereço:</strong> ${data.endereco}</p>
                <p><strong>CEP:</strong> ${data.cep}</p>
                <p><strong>UF:</strong> ${data.uf}</p>
            `;
        }
    } catch (error) {
        console.error("Erro na consulta:", error);
        const box = document.getElementById("resultado");
        box.style.display = "block";
        box.innerHTML = `<p style="color: red;"><strong>Erro:</strong> Falha na comunicação com o servidor</p>`;
    }
});

// Mantém a animação fade-in que você já tinha
document.addEventListener("DOMContentLoaded", () => {
    const main = document.querySelector("main");
    main.classList.add("fade");
});