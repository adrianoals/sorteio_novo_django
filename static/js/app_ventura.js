function iniciarSorteio() {
    // Oculta todo o conteúdo do sorteio, mas mantém o título e o GIF visíveis
    document.getElementById('conteudoSorteio').style.display = 'none';
    document.getElementById('loadingAnimation').style.display = 'block';

    // Espera 2.2 segundos antes de submeter o formulário
    setTimeout(function() {
        document.querySelector('form').submit();
    }, 2200);
}

// Adiciona evento ao botão de sorteio
document.querySelector('[type="submit"]').addEventListener('click', function(event) {
    event.preventDefault(); // Previne o envio imediato
    iniciarSorteio(); // Inicia o efeito visual e o sorteio
});
