document.addEventListener('DOMContentLoaded', function() {
    revelarLinhasProgressivamente();
});

function revelarLinhasProgressivamente() {
    const linhas = document.querySelectorAll('.linha-apartamento');
    const loadingContainer = document.getElementById('loadingContainer');

    // Se não houver loadingContainer, não fazer nada (página não precisa desta animação)
    if (!loadingContainer) {
        return;
    }

    if (linhas.length > 0) {
        linhas.forEach((linha, index) => {
            setTimeout(() => {
                if (linha) {
                    linha.style.opacity = 1; // Faz a linha aparecer gradualmente

                    // Rola a página até a linha que acabou de se tornar visível - SCROLL RÁPIDO
                    linha.scrollIntoView({ behavior: 'auto', block: 'end' });

                    // Verifica se é a última linha
                    if (index === linhas.length - 1) {
                        // Aguarda a última linha ficar visível antes de esconder a animação
                        setTimeout(() => {
                            if (loadingContainer) {
                                loadingContainer.style.display = 'none';
                            }
                            // Opcional: rola para o fim da página após o último elemento ser revelado - SCROLL RÁPIDO
                            document.body.scrollIntoView({behavior: 'auto', block: 'end'});
                        }, 150); // Reduzido para 100ms - MUITO MAIS RÁPIDO
                    }
                }
            }, index * 100); // Reduzido para 50ms - ANIMAÇÃO ULTRA RÁPIDA
        });
    } else {
        if (loadingContainer) {
            loadingContainer.style.display = 'none';
        }
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


