# Introdução à Estatística na Prática

Programa independente em Python dedicado ao **capítulo 1, “Introdução ao estudo da Estatística”**, de *Estatística e probabilidade: conceitos e aplicações*, de Luiz Roberto Dias de Macedo. Foi criado como demonstração prática para uso local e divulgação no GitHub. A interface, os exemplos e os dados fictícios estão em português do Brasil. O PDF é uma referência de desenvolvimento e **não é necessário durante a execução**.

## O que explorar

O menu apresenta os sete tópicos do capítulo:

1. **Crescimento da Estatística moderna:** linha do tempo navegável, censos, IBGE, aplicações e interpretação de evidências.
2. **O estudo da Estatística:** resumo descritivo de valores, lançamentos de moeda e comparação entre população e amostra.
3. **Natureza dos dados:** classificação nominal, ordinal, discreta e contínua com atividade corrigida.
4. **População e amostra:** população fictícia identificada, sorteio e comparação de uma característica.
5. **Processos de amostragem:** aleatória simples, estratificada proporcional, sistemática, por conglomerados e por conveniência sobre a mesma população.
6. **Fases do método estatístico:** oito etapas de uma pesquisa fictícia, tabela editável, auditoria de respostas inválidas, frequências e interpretação.
7. **Somatórios e produtórios:** sequências editáveis, índices e exclusões, fórmulas, expansão, tabela de acumulados, gráfico, identidades e somas parciais de uma série geométrica.

Há desafios com correção comentada ao fim de cada tópico. Os painéis **“Ver o código Python executado”** mostram as funções chamadas nos exemplos. Os sorteios ficam preservados durante a sessão até que o usuário clique no botão de sortear, e o botão lateral restaura os valores iniciais.

## Tecnologias e estrutura

- Python 3.10 ou superior; Streamlit para interface; pandas e NumPy para dados; Plotly para gráficos; pytest para testes.
- `app.py`: páginas e interação.
- `content.py`: explicações, cronologia e desafios.
- `calculations.py`: geração fictícia, amostragem, apuração e operações matemáticas.
- `tests/test_calculations.py`: verificações dos cálculos e sorteios.

## Instalação no Windows 11 (PowerShell e VS Code)

Abra a pasta deste projeto no VS Code. No terminal PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Se o PowerShell bloquear a ativação, use diretamente `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` e `.\.venv\Scripts\python.exe -m streamlit run app.py`. O endereço local aparece no terminal, normalmente `http://localhost:8501`.

Para rodar os testes:

```powershell
python -m pytest -q
```

## Exemplos de uso

- Em **1.2**, altere a lista de treinos; observe como média, mediana, tabela e gráfico respondem aos novos valores. Mude a semente da moeda e clique em **Lançar novamente**.
- Em **1.5**, defina N=103 e n=17, clique em **Sortear e comparar os cinco métodos**. Observe as posições da amostragem sistemática e como a conveniência prioriza o bairro Centro.
- Em **1.6**, substitua uma resposta por `18` ou `sem resposta`: a entrada permanece na auditoria e é excluída do resumo.
- Em **1.7**, escolha **Produto**, modelo **xᵢ / xᵢ₊₁**, limites 1 a 3, e X=`2, 4, 6, 8`; o resultado é `2/8 = 0,25`. Para uma constante repetida, escolha **constante c** e compare com c elevado ao número de fatores.

## Critérios e notas de correção

- A alocação estratificada usa **maiores restos**: calcula cotas proporcionais, toma o piso e distribui as vagas restantes pelos maiores restos. Empates são resolvidos pelo nome do estrato. Isso preserva o tamanho total pedido.
- A sistemática usa passo real `N/n` e um início aleatório em `[0, N/n)`, produzindo exatamente n posições distintas inclusive quando N não é múltiplo de n. A ordem da lista pode conter padrões periódicos.
- A conveniência segue a regra visível Centro → Norte → Sul → Oeste, depois a posição. É **não probabilística**; aumentar n não elimina automaticamente o viés.
- O exemplo de sorteio por arredondamento na p. 21 do livro não assegura seleção uniforme entre os identificadores nem evita duplicatas. Aqui o sorteio aleatório é uniforme **sem reposição**.
- O livro usa “infinita” para uma população muito grande ou difícil de contar (p. 20). Este programa distingue essa situação de uma população **matematicamente infinita**.
- Em um trecho da p. 18, “alta, média ou baixa” aparece como “quantitativa ordinal”; pela definição e pelos exemplos do próprio capítulo, a classificação adequada é **qualitativa ordinal**.
- Na fórmula visual da p. 28, o produto telescópico de `xᵢ/xᵢ₊₁`, de `i=p` até `q`, deve resultar em **`xₚ/x₍q₊₁₎`**, se os denominadores forem não nulos. O texto impresso exibe `xₚ/xq`. O programa usa a identidade correta.
- Na contagem de termos, somente exclusões **distintas e dentro dos limites** reduzem `NT = superior − inferior + 1`.

## Limitações conhecidas

Os dados e a população são inteiramente fictícios. As demonstrações são introdutórias: não calculam intervalos de confiança, margens de erro nem ajustam planos amostrais complexos. A seleção por conglomerados é uma demonstração de dois estágios, com grupos sorteados até reunirem elementos suficientes. As conclusões do estudo editável valem apenas para as respostas válidas do exemplo. Sequências no laboratório são limitadas a 100 valores e resultados não finitos são recusados.

## Referência

MACEDO, Luiz Roberto Dias de. *Estatística e probabilidade: conceitos e aplicações*. IESDE BRASIL, 2021. Capítulo 1, pp. 9–31 (páginas 11–33 no PDF de referência).

## Verificação

Consulte [VERIFICACOES.md](VERIFICACOES.md) para os comandos executados e o resultado da inspeção da interface.
