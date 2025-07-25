function iniciarSorteio() {
    // Oculta o resultado do sorteio anterior, mensagens e o rótulo do síndico selecionado, se existirem
    var resultadoAnterior = document.getElementById('sindico');
    var mensagens = document.querySelector('.alert');
    var labelSindico = document.getElementById('labelSindico'); // Seleciona o rótulo pelo id
    
    if (resultadoAnterior) resultadoAnterior.style.display = 'none';
    if (mensagens) mensagens.style.display = 'none';
    if (labelSindico) labelSindico.style.display = 'none'; // Oculta o rótulo

    // Mostra a animação
    document.getElementById('loadingAnimation').style.display = 'block';
    
    // Oculta o formulário de sorteio para evitar múltiplas submissões
    document.querySelector('form').style.display = 'none';

    // Espera 5 segundos antes de submeter o formulário
    setTimeout(function() {
        // Aqui, em vez de recarregar a página, você submete o formulário
        // Isso envia a requisição POST para o servidor
        document.querySelector('form').submit();
    }, 5000); // 5000 milissegundos = 5 segundos
}

// Adicione um ouvinte de evento ao seu botão de sorteio para iniciar o processo
document.querySelector('[type="submit"]').addEventListener('click', function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário
    iniciarSorteio();
});

