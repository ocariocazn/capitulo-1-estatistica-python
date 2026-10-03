# Verificações realizadas

Data: 3 de outubro de 2026. Ambiente de verificação: Windows, Python 3.12 do runtime local. Dependências de interface instaladas em `.vendor/`, pasta ignorada pelo Git; no computador do usuário, siga o ambiente virtual descrito no README.

| Verificação | Resultado |
| --- | --- |
| Leitura das páginas 11–33 do PDF e inspeção visual das fórmulas nas páginas 29–30 | Concluída. Identidades e imprecisões documentadas no README. |
| Compilação de sintaxe com `python -m compileall -q calculations.py content.py app.py` | Passou. |
| `python -m pytest -q` | 16 testes passaram: cálculos, identidades, entradas inválidas, sorteios e navegação/interações Streamlit. |
| Navegação por todas as sete páginas com `streamlit.testing.v1.AppTest` | Sem exceções. |
| Alteração de controles nos tópicos 1.1–1.5 e 1.7 com AppTest | Sem exceções; o sorteio permaneceu igual após alterações não relacionadas e mudou somente no botão. |
| Inicialização real do servidor Streamlit | Aplicativo abriu em `http://localhost:8501`. O runtime de teste exigiu `--global.developmentMode false`; uma instalação comum pelo README usa o comando padrão. |
| Inspeção visual no navegador | Menu e conteúdo renderizados; o laboratório 1.7 mostrou Σ de X de 1 a 4 = 20 e soma geométrica parcial de 10 termos ≈ 1,99805. |
| Edição real da tabela do tópico 1.6 | Ao mudar R01 de 2 para 18, válidas passaram de 7 para 6, inválidas de 1 para 2, e a média de 2,71 para 2,83. Auditoria marcou R01 como inválida. O botão restaurou os dados. |

As capturas foram examinadas no navegador de teste, mas não foram exportadas para o repositório. Os testes automatizados da interface e a verificação visual acima podem ser repetidos localmente.
