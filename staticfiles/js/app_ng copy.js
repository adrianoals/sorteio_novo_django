console.log("JavaScript carregado.");

function iniciarSorteio(formId, animationId) {
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
    const formSortear = document.querySelector('#sortearForm');
    const formSortearNovamente = document.querySelector('#sortearNovamenteForm');
    const formConfirmarVagas = document.querySelector('#confirmarVagasForm');

    function updateVagaOptions() {
        console.log("Atualizando opções de vagas.");
        const selectedVagas = Array.from(selects).map(select => select.value).filter(value => value);
        selects.forEach(select => {
            const currentVaga = select.value;
            select.querySelectorAll('option').forEach(option => {
                if (option.value && option.value !== currentVaga && selectedVagas.includes(option.value)) {
                    option.style.display = 'none';
                } else {
                    option.style.display = 'block';
                }
            });
        });
    }

    selects.forEach(select => {
        select.addEventListener('change', function () {
            updateVagaOptions();
        });
    });

    updateVagaOptions();

    if (formSortear) {
        formSortear.addEventListener('submit', function(event) {
            event.preventDefault(); // Previne o comportamento padrão do botão
            iniciarSorteio('sortearForm', 'loadingAnimation');
        });
    }

    if (formSortearNovamente) {
        formSortearNovamente.addEventListener('submit', function(event) {
            event.preventDefault(); // Previne o comportamento padrão do botão
            iniciarSorteio('sortearNovamenteForm', 'loadingAnimationNovamente');
        });
    }

    if (formConfirmarVagas) {
        formConfirmarVagas.addEventListener('submit', function() {
            // Garantir que o formulário de confirmação não acione a animação
            document.getElementById('loadingAnimation').style.display = 'none';
            document.getElementById('loadingAnimationNovamente').style.display = 'none';
        });
    }
});
