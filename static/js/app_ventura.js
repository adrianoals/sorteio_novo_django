function iniciarSorteio() {
    // Oculta todo o conteúdo do container
    var container = document.getElementById('container-sorteio');
    var titulo = document.querySelector("h5.font_subtitle"); // Seleciona o título "SELECIONANDO OS APARTAMENTOS PRESENTES!"

    if (container) container.style.display = "none"; // Oculta o container
    if (titulo) titulo.style.display = "block"; // Garante que o título continua visível

    // Exibe apenas a animação do GIF
    document.getElementById('loadingAnimation').style.display = 'block';

    // Aguarda 2.2 segundos antes de exibir o conteúdo de volta e sortear o apartamento
    setTimeout(function() {
        document.querySelector('form').submit();
    }, 2200);
}

// Adiciona o evento ao botão de sorteio
document.querySelector('[type="submit"]').addEventListener('click', function(event) {
    event.preventDefault(); // Previne o envio imediato do formulário
    iniciarSorteio();
});




// function iniciarSorteio() {
//     // Oculta o resultado do sorteio anterior, mensagens e o rótulo do síndico selecionado, se existirem
//     var resultadoAnterior = document.getElementById('sindico');
//     var mensagens = document.querySelector('.alert');
//     var labelSindico = document.getElementById('labelSindico'); // Seleciona o rótulo pelo id
    
//     if (resultadoAnterior) resultadoAnterior.style.display = 'none';
//     if (mensagens) mensagens.style.display = 'none';
//     if (labelSindico) labelSindico.style.display = 'none'; // Oculta o rótulo

//     // Mostra a animação
//     document.getElementById('loadingAnimation').style.display = 'block';
    
//     // Oculta o formulário de sorteio para evitar múltiplas submissões
//     document.querySelector('form').style.display = 'none';

//     // Espera 5 segundos antes de submeter o formulário
//     setTimeout(function() {
//         // Aqui, em vez de recarregar a página, você submete o formulário
//         // Isso envia a requisição POST para o servidor
//         document.querySelector('form').submit();
//     }, 2200); // 5000 milissegundos = 5 segundos
// }

// // Adicione um ouvinte de evento ao seu botão de sorteio para iniciar o processo
// document.querySelector('[type="submit"]').addEventListener('click', function(event) {
//     event.preventDefault(); // Previne o comportamento padrão do formulário
//     iniciarSorteio();
// });

