console.log("JavaScript para ng_adimplentes carregado.");

function iniciarSorteioAdimplentes(formId, animationId) {
    console.log(`Iniciando sorteio para ${formId} com animação ${animationId}`);
    // Oculta mensagens existentes
    var mensagens = document.querySelector('.messages');
    if (mensagens) mensagens.style.display = 'none';

    // Oculta todos os elementos dentro do container-sorteio, exceto a animação específica
    var container = document.getElementById('container-sorteio');
    Array.from(container.children).forEach(function(element) {
        if (element.id !== animationId) {
            element.style.display = 'none';
        }
    });

    // Mostra a animação de carregamento específica
    document.getElementById(animationId).style.display = 'block';

    // Espera 5 segundos antes de submeter o formulário
    setTimeout(function() {
        // Submete o formulário, enviando a requisição POST para o servidor
        document.getElementById(formId).submit();
    }, 5000); // 5000 milissegundos = 5 segundos
}

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM completamente carregado e analisado.");
    const selects = document.querySelectorAll('.vaga-selecionada');
    const selectedVagas = new Set();

    selects.forEach(select => {
        select.addEventListener('change', function () {
            const currentVaga = select.value;
            selectedVagas.add(currentVaga);

            selects.forEach(s => {
                if (s !== select) {
                    const options = s.querySelectorAll('option');
                    options.forEach(option => {
                        if (selectedVagas.has(option.value) && option.value !== s.value) {
                            option.style.display = 'none';
                        } else {
                            option.style.display = 'block';
                        }
                    });
                }
            });
        });
    });

    const formSortear = document.querySelector('#sortearForm');
    const formSortearNovamente = document.querySelector('#sortearNovamenteForm');

    if (formSortear) {
        formSortear.addEventListener('submit', function(event) {
            event.preventDefault(); // Previne o comportamento padrão do botão
            iniciarSorteioAdimplentes('sortearForm', 'loadingAnimation');
        });
    }

    if (formSortearNovamente) {
        formSortearNovamente.addEventListener('submit', function(event) {
            event.preventDefault(); // Previne o comportamento padrão do botão
            iniciarSorteioAdimplentes('sortearNovamenteForm', 'loadingAnimation');
        });
    }
});
