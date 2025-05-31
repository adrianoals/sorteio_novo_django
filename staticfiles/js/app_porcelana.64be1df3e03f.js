function iniciarSorteio() {
    // Oculta mensagens existentes
    var mensagens = document.querySelector('.messages');
    if (mensagens) mensagens.style.display = 'none';

    // Oculta a seção completa de atribuição de vaga e exibição de apartamento
    var secaoPresenca = document.getElementById('secaoPresenca');
    if (secaoPresenca) secaoPresenca.style.display = 'none';

    // Mostra a animação de carregamento
    document.getElementById('loadingAnimation').style.display = 'block';
    
    // Oculta o formulário de sorteio para evitar múltiplas submissões
    document.querySelector('form').style.display = 'none';

    // Espera 5 segundos antes de submeter o formulário
    setTimeout(function() {
        // Submete o formulário, enviando a requisição POST para o servidor
        document.querySelector('form').submit();
    }, 5000); // 5000 milissegundos = 5 segundos
}

// Adiciona o ouvinte de evento ao botão de sorteio
document.querySelector('[type="submit"]').addEventListener('click', function(event) {
    event.preventDefault(); // Previne o comportamento padrão do botão
    iniciarSorteio();
});




// Versão 2
// function iniciarSorteio() {
//     // Oculta mensagens existentes
//     var mensagens = document.querySelector('.messages');
//     if (mensagens) mensagens.style.display = 'none';

//     // Mostra a animação de carregamento
//     document.getElementById('loadingAnimation').style.display = 'block';
    
//     // Oculta o formulário de sorteio para evitar múltiplas submissões
//     document.querySelector('form').style.display = 'none';

//     // Espera 5 segundos antes de submeter o formulário
//     setTimeout(function() {
//         // Submete o formulário, enviando a requisição POST para o servidor
//         document.querySelector('form').submit();
//     }, 5000); // 5000 milissegundos = 5 segundos
// }

// // Adiciona o ouvinte de evento ao botão de sorteio
// document.querySelector('[type="submit"]').addEventListener('click', function(event) {
//     event.preventDefault(); // Previne o comportamento padrão do botão
//     iniciarSorteio();
// });





//Versao 1
// function iniciarSorteio() {
//     // Mostra a animação de carregamento
//     document.getElementById('loadingAnimation').style.display = 'block';
    
//     // Oculta o formulário de sorteio para evitar múltiplas submissões
//     document.querySelector('form').style.display = 'none';

//     // Espera 5 segundos antes de submeter o formulário
//     setTimeout(function() {
//         // Submete o formulário, enviando a requisição POST para o servidor
//         document.querySelector('form').submit();
//     }, 5000); // 5000 milissegundos = 5 segundos
// }

// // Adiciona o ouvinte de evento ao botão de sorteio
// document.querySelector('[type="submit"]').addEventListener('click', function(event) {
//     event.preventDefault(); // Previne o comportamento padrão do botão
//     iniciarSorteio();
// });
