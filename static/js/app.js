document.addEventListener('DOMContentLoaded', function() {
    revelarLinhasProgressivamente();
});

function revelarLinhasProgressivamente() {
    const linhas = document.querySelectorAll('.linha-apartamento');
    const loadingContainer = document.getElementById('loadingContainer');

    if (linhas.length > 0) {
        linhas.forEach((linha, index) => {
            setTimeout(() => {
                linha.style.opacity = 1; // Faz a linha aparecer gradualmente

                // Rola a página até a linha que acabou de se tornar visível
                linha.scrollIntoView({ behavior: 'smooth', block: 'end' });

                // Verifica se é a última linha
                if (index === linhas.length - 1) {
                    // Aguarda a última linha ficar visível antes de esconder a animação
                    setTimeout(() => {
                        loadingContainer.style.display = 'none';
                        // Opcional: rola para o fim da página após o último elemento ser revelado
                        document.body.scrollIntoView({behavior: 'smooth', block: 'end'});
                    }, 500); // Aguarda um pouco mais para garantir que a animação de carregamento desapareça suavemente
                }
            }, index * 250); // Ajusta para 250ms entre a revelação de cada linha para tornar a animação mais rápida
        });
    } else {
        loadingContainer.style.display = 'none';
    }
}

// document.addEventListener('DOMContentLoaded', function() {
//     revelarLinhasProgressivamente();
// });

// function revelarLinhasProgressivamente() {
//     const linhas = document.querySelectorAll('.linha-apartamento');
//     const loadingContainer = document.getElementById('loadingContainer'); // Certifique-se de que este ID corresponde ao seu HTML

//     if (linhas.length > 0) {
//         linhas.forEach((linha, index) => {
//             setTimeout(() => {
//                 linha.style.opacity = 1; // Faz a linha aparecer
//                 linha.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

//                 // Se for a última linha, ajusta o scroll para o final e esconde a animação de carregamento
//                 if (index === linhas.length - 1) {
//                     setTimeout(() => {
//                         window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
//                         // Esconde a animação de carregamento e o container
//                         loadingContainer.style.display = 'none';
//                     }, 5000); // Tempo adicional para a última linha ser revelada antes de esconder a animação
//                 }
//             }, index * 5000); // Intervalo entre a revelação de cada linha
//         });
//     } else {
//         // Se não houver linhas, esconde a animação imediatamente
//         loadingContainer.style.display = 'none';
//     }
// }


