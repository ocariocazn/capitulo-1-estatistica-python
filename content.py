"""Textos originais e atividades introdutórias do capítulo 1."""

TOPICOS = [
    "1.1 Crescimento da Estatística moderna",
    "1.2 O estudo da Estatística",
    "1.3 Natureza dos dados estatísticos",
    "1.4 População e amostra",
    "1.5 Processos de amostragem",
    "1.6 Fases do método estatístico",
    "1.7 Somatórios e produtórios",
]

LINHA_DO_TEMPO = [
    ("Antiguidade", "Levantamentos de pessoas e recursos já apoiavam decisões públicas em diversas civilizações."),
    ("1589–1633", "A origem do termo é debatida. O capítulo relata registros atribuídos a Girolamo Ghilini, com evidência documental de 1633."),
    ("1654", "Pascal e Fermat contribuíram para o desenvolvimento da teoria das probabilidades."),
    ("Século XVIII", "John Sinclair ampliou o uso de levantamentos sociais e econômicos na Escócia; Achenwall usou Statistik para estudos do Estado."),
    ("1733–1812", "De Moivre e, posteriormente, Gauss e Laplace contribuíram para o estudo da distribuição normal."),
    ("1833–1834", "Quételet impulsionou estudos demográficos e sociais; foi fundada a Royal Statistical Society."),
    ("1872", "O Censo Geral do Império é considerado o primeiro censo brasileiro de abrangência nacional."),
    ("1938–1940", "A reorganização que consolidou o IBGE foi seguida pelo V Recenseamento Geral do Brasil."),
    ("Século XX em diante", "Computadores e programas estatísticos aceleraram coleta, apuração, simulação e visualização."),
]

APLICACOES = {
    "Educação": "Comparar resultados de turmas e planejar apoio pedagógico, sem concluir que uma diferença isolada foi causada pelo professor.",
    "Atividade física": "Contar frequências de treino e estudar hábitos, delimitando quem respondeu e como foi selecionado.",
    "Comércio": "Analisar vendas por período e ajustar estoques, considerando sazonalidade e promoções.",
    "Satisfação": "Resumir respostas de clientes e identificar temas de melhoria; quem não respondeu pode ter opinião diferente.",
}

VARIAVEIS = {
    "Modalidade esportiva": ("Qualitativa nominal", "Categorias sem ordem natural: corrida, natação, dança."),
    "Grau de satisfação": ("Qualitativa ordinal", "Categorias ordenáveis por intensidade; os códigos 1–5 continuam rótulos."),
    "Quantidade de filhos": ("Quantitativa discreta", "Resultado de contagem em números inteiros não negativos."),
    "Número de treinos na semana": ("Quantitativa discreta", "Conta sessões realizadas durante um período definido."),
    "Estatura": ("Quantitativa contínua", "É medida; a precisão do instrumento determina o registro."),
    "Idade em anos completos": ("Quantitativa discreta", "No dado registrado, contamos os aniversários completos."),
    "Tempo de vida com maior precisão": ("Quantitativa contínua", "Tempo decorrido é mensurável com a precisão escolhida."),
    "Código 1=corrida, 2=natação": ("Qualitativa nominal", "Números são códigos de categorias, não quantidades."),
    "Estatura arredondada para centímetros inteiros": ("Quantitativa contínua", "O registro é inteiro, mas a grandeza medida continua contínua."),
}

FASES = [
    ("1. Definição do problema", "Pergunta: qual a frequência semanal de atividade física entre as pessoas pesquisadas?"),
    ("2. Delimitação do problema", "Exemplo fictício: oito participantes de uma turma; período: última semana."),
    ("3. Planejamento para obtenção dos dados", "Registrar identificador e número de treinos em uma ficha; aceitar 0 a 14 treinos."),
    ("4. Coleta de dados", "A tabela editável representa as respostas recebidas, incluindo eventuais erros."),
    ("5. Apuração dos dados", "Marcar respostas ausentes, não inteiras ou fora de 0–14. Preservar a entrada bruta e excluir inválidas do resumo."),
    ("6. Apresentação dos dados", "Tabela de frequências e gráfico mostram a distribuição das respostas válidas."),
    ("7. Análise dos dados", "Calcular média e proporção com pelo menos três treinos."),
    ("8. Interpretação dos dados", "Descrever apenas as respostas válidas desta turma; não generalizar à população sem plano amostral."),
]

DESAFIOS = [
    {
        "pergunta": "'Estatísticas' (plural) e 'Estatística' (singular) indicam, respectivamente:",
        "opcoes": ["Dados resumidos e ciência/métodos", "Ciência/métodos e dados resumidos", "A mesma coisa"],
        "certa": 0,
        "comentario": "O plural pode designar informações numéricas; o singular, os métodos de coleta, organização, análise e interpretação.",
    },
    {
        "pergunta": "Qual sequência descreve os três campos introdutórios?",
        "opcoes": ["Descrição, probabilidade, inferência", "Censo, gráfico, planilha", "Média, moda, mediana"],
        "certa": 0,
        "comentario": "A descrição resume o observado, a probabilidade modela o acaso e a inferência usa amostras para estudar populações.",
    },
    {
        "pergunta": "Uma nota de satisfação codificada como 1 a 5 é, no exemplo, uma variável:",
        "opcoes": ["Quantitativa contínua", "Qualitativa ordinal", "Qualitativa nominal"],
        "certa": 1,
        "comentario": "Há ordem entre níveis de satisfação, mas a distância entre categorias não é necessariamente numérica.",
    },
    {
        "pergunta": "Em N=20 e n=5, qual método escolhe uma posição inicial e depois mantém um passo?",
        "opcoes": ["Conveniência", "Estratificada", "Sistemática"],
        "certa": 2,
        "comentario": "A sistemática percorre uma lista ordenada com um intervalo; a ordem deve ser examinada em busca de periodicidade.",
    },
    {
        "pergunta": "Após coletar respostas, que fase marca respostas inválidas e tabula as válidas?",
        "opcoes": ["Apuração", "Delimitação", "Interpretação"],
        "certa": 0,
        "comentario": "Na apuração, criticamos e organizamos os dados antes de analisar.",
    },
    {
        "pergunta": "Quantos termos há de i=2 até 8, excluindo i=3 e i=5?",
        "opcoes": ["7", "5", "4"],
        "certa": 1,
        "comentario": "8 − 2 + 1 = 7 posições; duas exclusões distintas e válidas deixam 5.",
    },
    {
        "pergunta": "Com x=(2, 4, 6), qual é a soma dos quadrados dos três termos?",
        "opcoes": ["144", "56", "12"],
        "certa": 1,
        "comentario": "2² + 4² + 6² = 56; o quadrado da soma seria (2+4+6)² = 144.",
    },
    {
        "pergunta": "Qual é o produto de (i+1) para i de 1 a 4?",
        "opcoes": ["24", "120", "10"],
        "certa": 1,
        "comentario": "(1+1)(2+1)(3+1)(4+1) = 2×3×4×5 = 120.",
    },
]


def obter_marco(indice: int) -> tuple[str, str]:
    return LINHA_DO_TEMPO[indice]


def obter_aplicacao(nome: str) -> str:
    return APLICACOES[nome]


def classificar_exemplo(nome: str) -> tuple[str, str]:
    return VARIAVEIS[nome]
