document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript para ng_final carregado.");

    function iniciarSorteio() {
        // Oculta mensagens existentes
        var mensagens = document.querySelector('.messages');
        if (mensagens) mensagens.style.display = 'none';

        // Submete o formulário, enviando a requisição POST para o servidor
        document.getElementById('formulario-sorteio').submit();
    }

    // Adiciona o ouvinte de evento ao botão de sorteio
    document.getElementById('botao-iniciar').addEventListener('click', function(event) {
        event.preventDefault(); // Previne o comportamento padrão do botão
        iniciarSorteio();
    });
});
