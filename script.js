// Listener correto para o formulário
document.getElementById("consulta-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const cnpj = document.getElementById("cnpj").value;
    const cep = document.getElementById("cep").value;

    // Chamada ao backend Flask
    const resposta = await fetch("/consultar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cnpj, cep })
    });

    const data = await resposta.json();

    // Exibir resultado na tela
    const box = document.getElementById("resultado");
    box.style.display = "block";

    box.innerHTML = `
        <p><strong>Nome da empresa:</strong> ${data.nome}</p>
        <p><strong>Município:</strong> ${data.municipio}</p>
        <p><strong>Situação cadastral:</strong> ${data.situacao}</p>
        <p><strong>Natureza Jurídica:</strong> ${data.natureza}</p>
        <p><strong>Status:</strong> ${data.ativa ? "Ativa" : "Inativa"}</p>
    `;
});

// Mantém a animação fade-in que você já tinha
document.addEventListener("DOMContentLoaded", () => {
    const main = document.querySelector("main");
    main.classList.add("fade");
});
