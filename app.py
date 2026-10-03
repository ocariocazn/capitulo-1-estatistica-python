"""Introdução à Estatística na Prática — capítulo 1."""

import inspect
import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import calculations as calc
import content


st.set_page_config(page_title="Introdução à Estatística na Prática", page_icon="📊", layout="wide")


def codigo(*funcoes):
    with st.expander("Ver o código Python executado"):
        st.code("\n\n".join(inspect.getsource(funcao) for funcao in funcoes), language="python")


def grafico_barras(tabela: pd.DataFrame, x: str, y: str, titulo: str):
    figura = px.bar(tabela, x=x, y=y, title=titulo, text_auto=True)
    figura.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(figura, width="stretch")


def pagina_11():
    st.header(content.TOPICOS[0])
    st.write("A Estatística cresceu de levantamentos ligados ao Estado para uma ciência usada em diversas áreas. A origem exata do termo é discutida; questionar a fonte e o contexto faz parte da leitura estatística.")
    st.subheader("Linha do tempo")
    indice = st.slider("Navegue pelos marcos", 0, len(content.LINHA_DO_TEMPO) - 1, 0)
    data, descricao = content.obter_marco(indice)
    st.info(f"**{data}** — {descricao}")
    st.caption("O capítulo também cita Hawkins (1829), Kolmogorov (1929) e Bradford Hill (1937). O registro brasileiro de 1808 teve finalidade militar; o censo nacional de 1872 é tratado como o primeiro Censo Geral do Império.")
    st.write("Censos descrevem uma população delimitada e ajudam a planejar serviços, mercados e políticas. O IBGE produz e dissemina informações oficiais no Brasil. Computadores reduziram o custo de organizar e visualizar grandes volumes de dados, mas não substituem boas perguntas.")
    aplicacao = st.selectbox("Aplicação", list(content.APLICACOES))
    st.success(content.obter_aplicacao(aplicacao))
    st.subheader("Interprete a evidência")
    st.write("**Dados fictícios:** em 40 respostas voluntárias de uma escola, 24 pessoas disseram praticar atividade física ao menos três vezes por semana.")
    resposta = st.radio("Qual conclusão os dados sustentam?", [
        "60% das 40 pessoas que responderam relataram essa frequência.",
        "60% de todos os estudantes da cidade praticam essa frequência.",
    ], index=None, key="quiz_11")
    if st.button("Conferir interpretação", key="check_11"):
        if resposta is None:
            st.warning("Escolha uma resposta.")
        elif resposta.startswith("60% das 40"):
            st.success("Correto. 24 ÷ 40 = 60%; a pesquisa voluntária não permite estender isso à cidade.")
        else:
            st.error("A conclusão extrapola os dados: não houve uma amostra representativa de todos os estudantes da cidade.")
    codigo(content.obter_marco, content.obter_aplicacao)


def pagina_12():
    st.header(content.TOPICOS[1])
    st.write("**Estatística** designa métodos para coletar, organizar, analisar e interpretar dados para decidir. **Estatísticas** também pode designar os números e resumos produzidos. Descrição resume o observado; probabilidade estuda o acaso; inferência usa uma parte para aprender sobre o todo, com incerteza.")
    st.subheader("Descrição: resuma valores")
    texto = st.text_input("Treinos na semana, separados por vírgulas — dados fictícios", "2, 3, 0, 4, 2, 1, 3, 5", key="descr_valores")
    try:
        valores = calc.analisar_sequencia(texto)
        tabela = pd.DataFrame({"pessoa": range(1, len(valores) + 1), "treinos": valores})
        c1, c2, c3 = st.columns(3)
        c1.metric("Respostas", len(valores))
        c2.metric("Média", f"{pd.Series(valores).mean():.2f}")
        c3.metric("Mediana", f"{pd.Series(valores).median():.2f}")
        st.dataframe(tabela, hide_index=True)
        grafico_barras(tabela, "pessoa", "treinos", "Dados observados")
        st.caption("A média e a mediana descrevem somente os valores digitados.")
    except ValueError as erro:
        st.error(str(erro))
    st.subheader("Probabilidade: lançamentos de moeda")
    c1, c2 = st.columns(2)
    n = c1.slider("Número de lançamentos", 10, 1000, 80)
    semente = c2.number_input("Semente", 0, 999999, 42, key="moeda_semente")
    if "moeda_resultado" not in st.session_state or st.button("Lançar novamente"):
        st.session_state.moeda_resultado = (calc.lancamentos_moeda(n, int(semente)), n, int(semente))
    (lancamentos, proporcao), n_usado, seed_usada = st.session_state.moeda_resultado
    if (n, int(semente)) != (n_usado, seed_usada):
        st.caption(f"Resultado preservado: {n_usado} lançamentos e semente {seed_usada}. Clique em 'Lançar novamente' para usar os novos controles.")
    st.metric("Proporção de caras", f"{proporcao:.1%}")
    fig = px.line(lancamentos, x="lançamento", y="proporção acumulada", title="Frequência relativa acumulada de caras")
    fig.add_hline(y=0.5, line_dash="dash", annotation_text="probabilidade teórica 0,5")
    st.plotly_chart(fig, width="stretch")
    st.write("A frequência observada pode diferir de 50%. Uma nova simulação com a mesma semente reproduz o mesmo resultado.")
    st.subheader("Inferência: amostra e população")
    populacao = calc.criar_populacao(80)
    n_amostra = st.slider("Tamanho da amostra", 5, 60, 16, key="inf_n")
    if "infer_resultado" not in st.session_state or st.button("Sortear amostra", key="inf_sortear"):
        amostra = calc.amostra_aleatoria(populacao, n_amostra, int(semente))
        st.session_state.infer_resultado = (amostra, n_amostra, int(semente))
    amostra, n_usado, seed_usada = st.session_state.infer_resultado
    if (n_amostra, int(semente)) != (n_usado, seed_usada):
        st.caption("A amostra exibida foi preservada. Sorteie para aplicar os novos parâmetros.")
    taxa_pop = (populacao["pratica_atividade"] == "Sim").mean()
    taxa_amostra = (amostra["pratica_atividade"] == "Sim").mean()
    st.dataframe(pd.DataFrame({"grupo": ["População fictícia", "Amostra"], "n": [len(populacao), len(amostra)], "praticam (%)": [round(taxa_pop * 100, 1), round(taxa_amostra * 100, 1)]}), hide_index=True)
    st.write(f"A amostra sugere **{taxa_amostra:.1%}**, enquanto a população simulada tem **{taxa_pop:.1%}**. Em estudos reais, a taxa populacional costuma ser desconhecida e a estimativa traz incerteza.")
    codigo(calc.analisar_sequencia, calc.lancamentos_moeda, calc.amostra_aleatoria)


def pagina_13():
    st.header(content.TOPICOS[2])
    st.write("Variáveis **qualitativas** descrevem categorias: nominais não têm ordem natural; ordinais têm ordem ou intensidade. Variáveis **quantitativas** representam quantidades: discretas costumam resultar de contagem e contínuas de medição.")
    st.info("Classifique pelo significado e pela forma de obtenção, não pelo tipo da coluna no pandas. Código numérico de modalidade é nominal; estatura medida e arredondada para inteiro continua sendo contínua.")
    exemplo = st.selectbox("Escolha uma variável", list(content.VARIAVEIS))
    classificacao, motivo = content.classificar_exemplo(exemplo)
    st.write(f"**{classificacao}.** {motivo}")
    st.subheader("Teste sua classificação")
    exemplo_atividade = st.selectbox("Variável para classificar", list(content.VARIAVEIS), key="var_atividade")
    resposta = st.radio("Sua resposta", ["Qualitativa nominal", "Qualitativa ordinal", "Quantitativa discreta", "Quantitativa contínua"], index=None, key="var_resposta")
    if st.button("Corrigir classificação"):
        if resposta is None:
            st.warning("Selecione uma classificação.")
        else:
            correta, razao = content.classificar_exemplo(exemplo_atividade)
            (st.success if resposta == correta else st.error)(f"Resposta: {correta}. {razao}")
    st.write("**Ordenação e intensidade:** 'baixo, médio, alto' expressa ordem, mas não informa que a distância entre níveis seja constante. Contar treinos e medir tempo são operações diferentes.")
    codigo(content.classificar_exemplo)


def pagina_14():
    st.header(content.TOPICOS[3])
    st.write("**População** é o conjunto de pessoas ou objetos definido pela pergunta e por uma característica comum. **Amostra** é um subconjunto. Censo observa todos os elementos; pesquisa por amostragem observa parte deles.")
    st.write("Uma população finita tem número finito de unidades, mesmo que seja enorme ou desconhecido. Uma população matematicamente infinita tem infinitas unidades possíveis, como uma sequência ilimitada de lançamentos de moeda. Tamanho maior, por si só, não corrige viés de seleção.")
    c1, c2, c3 = st.columns(3)
    n_pop = c1.slider("Tamanho da população fictícia", 8, 500, 80, key="pop_n")
    n_amostra = c2.number_input("Tamanho da amostra", 1, n_pop, min(16, n_pop), key="pop_amostra_n")
    semente = c3.number_input("Semente", 0, 999999, 17, key="pop_semente")
    if "pop_resultado" not in st.session_state or st.button("Selecionar amostra", key="pop_sortear"):
        populacao = calc.criar_populacao(n_pop)
        amostra = calc.amostra_aleatoria(populacao, int(n_amostra), int(semente))
        st.session_state.pop_resultado = (populacao, amostra, (n_pop, int(n_amostra), int(semente)))
    populacao, amostra, parametros = st.session_state.pop_resultado
    if parametros != (n_pop, int(n_amostra), int(semente)):
        st.caption("A seleção anterior está preservada. Clique em 'Selecionar amostra' para aplicar os novos parâmetros.")
    st.write(f"**População delimitada:** {len(populacao)} pessoas fictícias identificadas de P0001 em diante. **Amostra:** {len(amostra)} identificadores únicos.")
    st.dataframe(amostra, hide_index=True, width="stretch")
    compara = calc.composicao(populacao, amostra, "pratica_atividade").reset_index(names="pratica_atividade")
    st.dataframe(compara, hide_index=True)
    fig = px.bar(compara.melt(id_vars="pratica_atividade", var_name="grupo", value_name="%"), x="pratica_atividade", y="%", color="grupo", barmode="group", title="Prática de atividade na população e na amostra")
    st.plotly_chart(fig, width="stretch")
    st.write("Diferenças entre percentuais surgem mesmo em sorteios corretos; uma seleção por facilidade pode criar diferenças sistemáticas.")
    codigo(calc.criar_populacao, calc.amostra_aleatoria, calc.composicao)


def executar_cinco(populacao: pd.DataFrame, n: int, semente: int):
    aleatoria = calc.amostra_aleatoria(populacao, n, semente)
    estratificada, alocacao = calc.amostra_estratificada(populacao, n, semente)
    sistematica, inicio, posicoes = calc.amostra_sistematica(populacao, n, semente)
    conglomerados, bairros = calc.amostra_conglomerados(populacao, n, semente)
    conveniencia = calc.amostra_conveniencia(populacao, n)
    return {
        "Aleatória": (aleatoria, "Sorteio uniforme sem reposição."),
        "Estratificada": (estratificada, f"Alocação proporcional por faixa: {alocacao.to_dict()}."),
        "Sistemática": (sistematica, f"Início zero baseado {inicio:.3f}; passo N/n={len(populacao)/n:.3f}; posições na lista: {posicoes}."),
        "Conglomerados": (conglomerados, f"Bairros sorteados: {', '.join(bairros)}; pessoas sorteadas dentro desses bairros."),
        "Conveniência": (conveniencia, "Regra: Centro, Norte, Sul, Oeste; dentro do bairro, menor posição primeiro."),
    }


def pagina_15():
    st.header(content.TOPICOS[4])
    st.write("Compare cinco procedimentos sobre **a mesma população fictícia**. Estratos são categorias cujos membros são selecionados em cada estrato; conglomerados são grupos naturais sorteados antes da seleção de pessoas dentro deles.")
    c1, c2, c3 = st.columns(3)
    n_pop = c1.slider("População N", 20, 400, 120, key="met_n_pop")
    n = c2.number_input("Amostra n", 1, n_pop, min(20, n_pop), key="met_n")
    seed = c3.number_input("Semente", 0, 999999, 21, key="met_seed")
    if "met_resultado" not in st.session_state or st.button("Sortear e comparar os cinco métodos", type="primary"):
        populacao = calc.criar_populacao(n_pop)
        resultados = executar_cinco(populacao, int(n), int(seed))
        st.session_state.met_resultado = (populacao, resultados, (n_pop, int(n), int(seed)))
    populacao, resultados, parametros = st.session_state.met_resultado
    if parametros != (n_pop, int(n), int(seed)):
        st.caption("A comparação exibida foi preservada. Clique no botão para usar os parâmetros atuais.")
    st.caption("Estratificada: cotas n × Nₕ/N, piso de cada cota e distribuição das vagas restantes pelos maiores restos; empate por nome do estrato. A soma é sempre n.")
    resumo = []
    for nome, (amostra, detalhe) in resultados.items():
        taxa = 100 * (amostra["pratica_atividade"] == "Sim").mean()
        resumo.append({"método": nome, "n": len(amostra), "praticam (%)": round(taxa, 1), "diferença vs população (p.p.)": round(taxa - 100 * (populacao["pratica_atividade"] == "Sim").mean(), 1)})
    st.dataframe(pd.DataFrame(resumo), hide_index=True, width="stretch")
    grafico_barras(pd.DataFrame(resumo), "método", "praticam (%)", "Composição obtida em cada método")
    st.write(f"Na população, **{(populacao['pratica_atividade'] == 'Sim').mean():.1%}** praticam atividade. Nesta realização, os percentuais das amostras variam conforme o método e o acaso.")
    for nome, (amostra, detalhe) in resultados.items():
        with st.expander(f"{nome}: elementos e composição ({len(amostra)})"):
            st.write(detalhe)
            st.dataframe(amostra, hide_index=True, width="stretch")
            st.dataframe(calc.composicao(populacao, amostra).reset_index(names="bairro"), hide_index=True)
    st.warning("Conveniência é não probabilística e pode distorcer a composição. Na sistemática, padrões periódicos na ordem da lista podem coincidir com o passo e produzir viés; examine a ordenação antes do sorteio.")
    codigo(calc.amostra_aleatoria, calc.alocacao_proporcional, calc.amostra_estratificada, calc.amostra_sistematica, calc.amostra_conglomerados, calc.amostra_conveniencia)


def pagina_16():
    st.header(content.TOPICOS[5])
    st.write("Uma pesquisa clara define a pergunta, delimita quem participa, planeja a coleta, registra respostas, verifica qualidade, apresenta, analisa e interpreta. Edite as respostas fictícias abaixo para acompanhar as oito fases.")
    for titulo, explicacao in content.FASES[:4]:
        st.markdown(f"**{titulo}.** {explicacao}")
    inicial = pd.DataFrame({"id": [f"R{i:02d}" for i in range(1, 9)], "treinos_semana": ["2", "3", "0", "5", "2", "4", "sem resposta", "3"]})
    if "pesquisa_original" not in st.session_state:
        st.session_state.pesquisa_original = inicial.copy(deep=True)
    if st.button("Restaurar respostas fictícias", key="reset_estudo"):
        st.session_state.pesquisa_original = inicial.copy(deep=True)
        st.session_state.pop("editor_pesquisa", None)
        st.rerun()
    st.caption("A coluna de identificação é fixa; altere os treinos. Válidos: inteiros de 0 a 14. A entrada original permanece visível para auditoria.")
    editadas = st.data_editor(st.session_state.pesquisa_original, key="editor_pesquisa", disabled=["id"], num_rows="fixed", hide_index=True)
    auditoria, limpos = calc.apurar_respostas(editadas)
    st.subheader("5. Apuração: original e tratamento")
    st.dataframe(auditoria, hide_index=True, width="stretch")
    st.write(f"{len(limpos)} resposta(s) válida(s) e {len(auditoria)-len(limpos)} inválida(s). As inválidas continuam na tabela de auditoria.")
    st.subheader("6. Apresentação")
    if limpos.empty:
        st.warning("Nenhuma resposta válida para tabular.")
    else:
        frequencias = limpos["treinos_semana"].value_counts().sort_index().rename_axis("treinos_semana").reset_index(name="frequência")
        st.dataframe(frequencias, hide_index=True)
        grafico_barras(frequencias, "treinos_semana", "frequência", "Frequência semanal observada")
    st.subheader("7. Análise e 8. Interpretação")
    resumo = calc.analisar_treinos(limpos)
    if resumo["n"]:
        st.write(f"Nas **{resumo['n']} respostas válidas**, a média foi **{resumo['media']:.2f} treinos/semana** e **{resumo['proporcao_ativa']:.1%}** relataram pelo menos três treinos.")
        st.info("Esses números descrevem somente as pessoas desta turma fictícia que forneceram respostas válidas. O exemplo não sustenta generalizações para outras turmas; exclusões também podem afetar o resultado.")
    else:
        st.info("Sem valores válidos, não é possível tirar uma conclusão numérica.")
    codigo(calc.apurar_respostas, calc.analisar_treinos)


def ler_exclusoes(texto: str) -> list[int]:
    if not texto.strip():
        return []
    try:
        return [int(item.strip()) for item in texto.replace(";", ",").split(",")]
    except ValueError as erro:
        raise ValueError("Exclusões devem ser índices inteiros separados por vírgulas.") from erro


def pagina_17():
    st.header(content.TOPICOS[6])
    st.write("**Σ** soma parcelas; **Π** multiplica fatores. O indexador i percorre os limites inferior e superior. Sem exclusões, **NT = superior − inferior + 1**; exclusões distintas e dentro do intervalo reduzem essa contagem uma única vez cada.")
    st.caption("A posição matemática x₁ corresponde a x[0] em Python. Para produtos telescópicos, é preciso fornecer também x_(superior+1).")
    c1, c2 = st.columns(2)
    x_texto = c1.text_input("Sequência X (vírgulas)", "2, 4, 6, 8, 10, 12, 14, 16", key="lab_x")
    y_texto = c2.text_input("Sequência Y (vírgulas)", "1, 3, 5, 7, 9, 11, 13, 15", key="lab_y")
    c1, c2, c3, c4 = st.columns(4)
    operacao = c1.selectbox("Operação", ["Soma", "Produto"])
    modelo = c2.selectbox("Modelo de termo", list(calc.MODELOS))
    inferior = int(c3.number_input("Limite inferior", 1, 100, 1))
    superior = int(c4.number_input("Limite superior", 1, 100, 4))
    c1, c2 = st.columns(2)
    excl_texto = c1.text_input("Índices excluídos (opcional)", "", help="Ex.: 2, 4. Repetidos ou fora do intervalo não alteram NT.")
    constante = c2.number_input("Constante c ou base/razão", value=2.0, step=0.5)
    try:
        x = calc.analisar_sequencia(x_texto)
        y = calc.analisar_sequencia(y_texto)
        exclusoes = ler_exclusoes(excl_texto)
        tabela, resultado = calc.calcular_laboratorio(operacao, modelo, x, y, inferior, superior, exclusoes, constante)
        simbolo = "\\sum" if operacao == "Soma" else "\\prod"
        exclusoes_validas = sorted({i for i in exclusoes if inferior <= i <= superior})
        restricao = (r",\;i\notin\{" + ",".join(map(str, exclusoes_validas)) + r"\}") if exclusoes_validas else ""
        st.latex(rf"{simbolo}_{{i={inferior}{restricao}}}^{{{superior}}} {calc.MODELOS[modelo]} = {resultado:.6g}")
        st.write(f"**Número de termos/fatores:** {calc.contar_termos(inferior, superior, exclusoes)}")
        if exclusoes:
            st.caption(f"Índices válidos mantidos: {', '.join(map(str, tabela['índice i'].tolist())) or 'nenhum'}.")
        separador = " + " if operacao == "Soma" else " × "
        expansao = separador.join(f"({v:g})" for v in tabela["termo"]) if not tabela.empty else ("0" if operacao == "Soma" else "1")
        st.write(f"**Expansão:** {expansao}")
        st.dataframe(tabela, hide_index=True, width="stretch")
        if not tabela.empty:
            fig = px.line(tabela, x="índice i", y="acumulado", markers=True, title=f"{operacao} acumulado(a)")
            st.plotly_chart(fig, width="stretch")
        st.write(f"**Resultado final:** {resultado:g}")
    except (ValueError, OverflowError, ZeroDivisionError) as erro:
        st.error(str(erro))
    with st.expander("Identidades e exemplos comentados"):
        st.latex(r"\sum_{i=1}^{n}x_i^2\ne\left(\sum_{i=1}^{n}x_i\right)^2")
        st.write("Para X=(2,4,6): 2²+4²+6²=56, enquanto (2+4+6)²=144.")
        st.latex(r"\prod_{i=p}^{q}c=c^{q-p+1}")
        st.write("Uma constante em cada fator produz uma potência; em cada parcela da soma, produz c × NT.")
        st.latex(r"\prod_{i=p}^{q}\frac{x_i}{x_{i+1}}=\frac{x_p}{x_{q+1}}")
        st.write("O cancelamento só vale se todos os denominadores necessários forem diferentes de zero. Para a mesma base, o produto de potências soma os expoentes.")
        st.latex(r"\prod_{i=p}^{q}a^{x_i}=a^{\sum_{i=p}^{q}x_i}")
        st.write("Modelos disponíveis cobrem soma simples, quadrados, termos de duas sequências, constantes, potências e produto telescópico. Entradas livres nunca são executadas como código.")
    st.subheader("Soma parcial e soma infinita")
    c1, c2 = st.columns(2)
    razao = c1.number_input("Razão r na série 1 + r + r² + …", -3.0, 3.0, 0.5, step=0.1)
    termos = int(c2.slider("Parcelas da soma parcial", 1, 40, 10))
    try:
        geometricos, limite = calc.soma_geometrica_parcial(float(razao), termos)
        st.metric("Soma parcial", f"{geometricos['soma parcial'].iloc[-1]:.6g}")
        st.plotly_chart(px.line(geometricos, x="n", y="soma parcial", markers=True, title="Somas parciais"), width="stretch")
        if limite is None:
            st.info("Com |r| ≥ 1, esta série geométrica não converge para uma soma finita.")
        else:
            st.write(f"Como |r| < 1, a soma infinita é **1/(1−r) = {limite:.6g}**. O valor mostrado acima usa apenas {termos} parcelas.")
    except ValueError as erro:
        st.error(str(erro))
    codigo(calc.indices_validos, calc.contar_termos, calc.calcular_laboratorio, calc.soma_geometrica_parcial)


def desafios():
    with st.expander("Desafios finais do capítulo — correção comentada"):
        for numero, desafio in enumerate(content.DESAFIOS, 1):
            st.markdown(f"**{numero}. {desafio['pergunta']}**")
            escolha = st.radio("Escolha", desafio["opcoes"], index=None, key=f"desafio_{numero}", label_visibility="collapsed")
            if st.button("Corrigir", key=f"corrigir_{numero}"):
                if escolha is None:
                    st.warning("Escolha uma opção.")
                else:
                    (st.success if escolha == desafio["opcoes"][desafio["certa"]] else st.error)(desafio["comentario"])


def main():
    st.title("Introdução à Estatística na Prática")
    st.write("Um laboratório interativo e independente para o **capítulo 1** de *Estatística e probabilidade: conceitos e aplicações*, de Luiz Roberto Dias de Macedo. Todos os dados das simulações são **fictícios**.")
    with st.sidebar:
        st.header("Capítulo 1")
        pagina = st.radio("Escolha um tópico", content.TOPICOS)
        if st.button("Restaurar valores iniciais", width="stretch"):
            st.session_state.clear()
            st.rerun()
        st.caption("Sorteios só mudam ao clicar nos botões próprios. O PDF não é necessário para executar o programa.")
    paginas = [pagina_11, pagina_12, pagina_13, pagina_14, pagina_15, pagina_16, pagina_17]
    paginas[content.TOPICOS.index(pagina)]()
    desafios()
    st.divider()
    st.caption("Fonte conceitual: Macedo, Luiz Roberto Dias de. Estatística e probabilidade: conceitos e aplicações, capítulo 1, pp. 9–31. Textos e dados deste programa são originais; veja as notas de correção no README.")


if __name__ == "__main__":
    main()
