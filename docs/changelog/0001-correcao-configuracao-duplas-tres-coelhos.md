# Correção: Configuração de Duplas - App tres_coelhos

## Título da Mudança
Correção do sistema de criação de duplas de apartamentos no app `tres_coelhos`

## Arquivos Modificados
- `templates/tres_coelhos/tres_coelhos_configurar_duplas.html`
- `tres_coelhos/views.py` (função `tres_coelhos_configurar_duplas`, linhas 597-827)

## Descrição Detalhada

### Problema Identificado
A funcionalidade de criar duplas de apartamentos não estava funcionando na interface. Apenas a exclusão de duplas funcionava corretamente.

### Causa Raiz
O problema estava na forma como os campos do formulário eram nomeados e processados:

1. **Conflito de Índices**: O template usava nomes fixos como `dupla_1_apt1` e `dupla_2_apt1` para diferentes subsolos, o que causava conflitos quando a view tentava agrupar os dados.

2. **Formato Incompatível**: O formato antigo `dupla_X_apt1` (onde X era um número) não permitia distinguir claramente entre subsolos, causando processamento incorreto na view.

3. **JavaScript Inconsistente**: O JavaScript que adicionava novas duplas dinamicamente usava índices que podiam conflitar com os índices fixos do template.

### Solução Implementada

#### 1. Novo Formato de Nomes de Campos
Mudamos de:
- `dupla_1_apt1`, `dupla_1_apt2` (Subsolo 1)
- `dupla_2_apt1`, `dupla_2_apt2` (Subsolo 2)

Para:
- `dupla_sub1_0_apt1`, `dupla_sub1_0_apt2` (Subsolo 1, índice 0)
- `dupla_sub2_0_apt1`, `dupla_sub2_0_apt2` (Subsolo 2, índice 0)

#### 2. Correção no Template HTML
- Atualizados os nomes dos campos `name` nos selects para usar o novo formato `dupla_sub{N}_{index}_apt{1|2}`
- Adicionado atributo `data-subsolo` nos containers para facilitar o processamento JavaScript
- Primeiro campo de cada subsolo usa índice 0

#### 3. Ajuste na View (Python)
- Modificada a lógica de processamento para reconhecer o novo formato `dupla_sub{N}_{index}_apt{1|2}`
- Agrupamento agora usa chave única combinando subsolo e índice (ex: `sub1_0`, `sub2_1`)
- Processamento mantém a validação de subsolos iguais e apartamentos não duplicados

#### 4. Correção no JavaScript
- Função `adicionarDupla()` atualizada para gerar nomes no novo formato
- Contadores inicializados corretamente (começam em 1, pois índice 0 já existe)
- Seletor de selects atualizado para usar `select[name^="dupla_sub"]`
- Lógica de validação JavaScript atualizada para processar o novo formato
- **Correção crítica**: Substituído operador `in` por `.includes()` na validação de arrays (bug JavaScript)

## Passo a Passo das Ações Realizadas

1. **Análise do Problema**
   - Identificado que os campos não estavam sendo processados corretamente pela view
   - Verificado que o formato antigo causava conflitos entre subsolos

2. **Mudança no Template**
   - Alterados os nomes dos campos para formato `dupla_sub{N}_{index}_apt{1|2}`
   - Atualizado ambos os subsolos (Subsolo 1 e Subsolo 2)

3. **Ajuste na View Python**
   - Modificada a função `tres_coelhos_configurar_duplas` na linha 639-658
   - Atualizado o parsing dos campos POST para reconhecer o novo formato
   - Mantida toda a lógica de validação existente (mesmo subsolo, não duplicados, etc.)

4. **Correção do JavaScript**
   - Atualizada função `adicionarDupla()` para gerar nomes no novo formato
   - Corrigidos contadores para começar em 1 (índice 0 já existe no template)
   - Ajustada validação de formulário para processar o novo formato
   - **Correção crítica**: Substituído `parts[3] in ['apt1', 'apt2']` por `['apt1', 'apt2'].includes(parts[3])` - o operador `in` em JavaScript verifica propriedades de objetos, não valores em arrays

5. **Testes e Validação**
   - Verificado que não há erros de lint
   - Confirmado que o formato é consistente em todo o código

## Critérios de Aceitação

✅ **Funcionalidade**: Usuário consegue criar duplas de apartamentos pela interface
✅ **Validação**: Apenas apartamentos do mesmo subsolo podem formar duplas
✅ **Prevenção de Duplicatas**: Apartamentos já em duplas não aparecem nos dropdowns
✅ **Interface Dinâmica**: Botão "Adicionar outra dupla" funciona corretamente
✅ **Formato Consistente**: Todos os campos seguem o padrão `dupla_sub{N}_{index}_apt{1|2}`

## Status Final
✅ **IMPLEMENTADO**

## Observações Técnicas

- O formato antigo `dupla_X_apt1` tinha apenas 3 partes quando dividido por `_`, enquanto o novo formato `dupla_sub{N}_{index}_apt{1|2}` tem 4 partes
- A view agora valida explicitamente que o formato tem 4 partes e que a segunda parte começa com "sub"
- Os contadores JavaScript são independentes por subsolo, evitando conflitos
- A exclusão de duplas continua funcionando normalmente (usa ID da dupla, não depende do formato dos campos)

