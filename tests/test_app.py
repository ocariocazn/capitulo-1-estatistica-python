"""Smoke test das sete páginas com o testador oficial do Streamlit."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

import content


def test_sete_paginas_sem_excecoes():
    app = Path(__file__).resolve().parents[1] / "app.py"
    at = AppTest.from_file(str(app), default_timeout=30).run()
    assert not at.exception
    for topico in content.TOPICOS:
        at.sidebar.radio[0].set_value(topico).run()
        assert not at.exception, f"Falha em {topico}: {at.exception}"


def test_controles_e_sorteios_preservados():
    app = Path(__file__).resolve().parents[1] / "app.py"
    at = AppTest.from_file(str(app), default_timeout=30).run()
    # Linha do tempo, aplicação e correção da interpretação.
    at.slider[0].set_value(3).run()
    at.selectbox[0].set_value("Comércio").run()
    at.radio(key="quiz_11").set_value("60% das 40 pessoas que responderam relataram essa frequência.").run()
    at.button(key="check_11").click().run()
    assert not at.exception

    at.sidebar.radio[0].set_value(content.TOPICOS[1]).run()
    moeda_antes = at.session_state["moeda_resultado"][0][0].copy(deep=True)
    at.text_input(key="descr_valores").set_value("1, 2, 3").run()
    moeda_depois = at.session_state["moeda_resultado"][0][0]
    assert moeda_antes.equals(moeda_depois)
    at.button[0].click().run()  # Lançar novamente.
    assert not at.exception

    at.sidebar.radio[0].set_value(content.TOPICOS[2]).run()
    at.selectbox(key="var_atividade").set_value("Estatura").run()
    at.radio(key="var_resposta").set_value("Quantitativa contínua").run()
    at.button[0].click().run()
    assert not at.exception

    at.sidebar.radio[0].set_value(content.TOPICOS[3]).run()
    at.slider(key="pop_n").set_value(43).run()
    at.button(key="pop_sortear").click().run()
    assert len(at.session_state["pop_resultado"][0]) == 43
    at.number_input(key="pop_amostra_n").set_value(40).run()
    at.slider(key="pop_n").set_value(20).run()
    assert not at.exception

    at.sidebar.radio[0].set_value(content.TOPICOS[4]).run()
    sorteio_antes = at.session_state["met_resultado"][1]["Aleatória"][0]["id"].tolist()
    at.number_input(key="met_seed").set_value(99).run()
    assert sorteio_antes == at.session_state["met_resultado"][1]["Aleatória"][0]["id"].tolist()
    at.button[0].click().run()
    assert at.session_state["met_resultado"][2][2] == 99
    assert not at.exception

    at.sidebar.radio[0].set_value(content.TOPICOS[5]).run()
    assert "pesquisa_original" in at.session_state
    assert not at.exception

    at.sidebar.radio[0].set_value(content.TOPICOS[6]).run()
    at.text_input(key="lab_x").set_value("2, 4, 6, 8").run()
    at.selectbox[0].set_value("Produto").run()
    at.selectbox[1].set_value("xᵢ / xᵢ₊₁").run()
    assert not at.exception
