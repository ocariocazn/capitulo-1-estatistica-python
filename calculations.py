"""Cálculos e simulações do capítulo 1; sem dependência do Streamlit."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np
import pandas as pd


def criar_populacao(tamanho: int) -> pd.DataFrame:
    """População fictícia estável, com um identificador por pessoa."""
    if not 8 <= tamanho <= 2000:
        raise ValueError("O tamanho deve estar entre 8 e 2.000.")
    ids = np.arange(1, tamanho + 1)
    bairros = np.array(["Centro", "Norte", "Sul", "Oeste"])
    grupos = np.array(["A", "B", "C"])
    # Dados determinísticos: a conveniência por bairro pode causar distorção visível.
    pratica = ((ids * 7 + ids // 4) % 11 < 3) | ((ids % 4 == 1) & (ids % 3 == 0))
    return pd.DataFrame(
        {
            "id": [f"P{x:04d}" for x in ids],
            "posição": ids,
            "bairro": bairros[(ids - 1) % 4],
            "faixa": grupos[(ids * 5 + ids // 7) % 3],
            "pratica_atividade": np.where(pratica, "Sim", "Não"),
        }
    )


def validar_amostra(populacao: pd.DataFrame, tamanho: int) -> None:
    if populacao.empty or not populacao["id"].is_unique:
        raise ValueError("A população precisa ter identificadores únicos.")
    if not isinstance(tamanho, int) or not 1 <= tamanho <= len(populacao):
        raise ValueError("A amostra deve ter entre 1 e N elementos.")


def amostra_aleatoria(populacao: pd.DataFrame, tamanho: int, semente: int) -> pd.DataFrame:
    """Sorteio uniforme de identificadores sem reposição."""
    validar_amostra(populacao, tamanho)
    posicoes = np.random.default_rng(semente).choice(len(populacao), size=tamanho, replace=False)
    return populacao.iloc[posicoes].reset_index(drop=True)


def alocacao_proporcional(contagens: pd.Series, tamanho: int) -> pd.Series:
    """Maiores restos: piso das cotas; sobras aos maiores restos, empate por ordem."""
    if contagens.empty or (contagens <= 0).any() or int(contagens.sum()) < tamanho or tamanho < 1:
        raise ValueError("Estratos ou tamanho inválidos.")
    cotas = contagens.astype(float) * tamanho / int(contagens.sum())
    alocacao = np.floor(cotas).astype(int)
    faltam = tamanho - int(alocacao.sum())
    restos = cotas - alocacao
    for chave in sorted(contagens.index, key=lambda x: (-float(restos.loc[x]), str(x)))[:faltam]:
        alocacao.loc[chave] += 1
    return alocacao


def amostra_estratificada(
    populacao: pd.DataFrame, tamanho: int, semente: int, coluna: str = "faixa"
) -> tuple[pd.DataFrame, pd.Series]:
    validar_amostra(populacao, tamanho)
    if coluna not in populacao or populacao[coluna].isna().any():
        raise ValueError("Coluna de estratos inválida.")
    contagens = populacao[coluna].value_counts().sort_index()
    alocacao = alocacao_proporcional(contagens, tamanho)
    rng = np.random.default_rng(semente)
    partes = []
    for estrato, quantidade in alocacao.items():
        bloco = populacao.loc[populacao[coluna] == estrato]
        if quantidade:
            partes.append(bloco.iloc[rng.choice(len(bloco), size=quantidade, replace=False)])
    return pd.concat(partes, ignore_index=True), alocacao


def amostra_sistematica(
    populacao: pd.DataFrame, tamanho: int, semente: int
) -> tuple[pd.DataFrame, float, list[int]]:
    """Passo fracionário N/n e início uniforme em [0, N/n)."""
    validar_amostra(populacao, tamanho)
    passo = len(populacao) / tamanho
    inicio = float(np.random.default_rng(semente).uniform(0, passo))
    indices = [math.floor(inicio + j * passo) for j in range(tamanho)]
    if len(set(indices)) != tamanho or max(indices) >= len(populacao):
        raise ArithmeticError("Falha interna no sorteio sistemático.")
    return populacao.iloc[indices].reset_index(drop=True), inicio, [i + 1 for i in indices]


def amostra_conglomerados(
    populacao: pd.DataFrame, tamanho: int, semente: int, coluna: str = "bairro"
) -> tuple[pd.DataFrame, list[str]]:
    """Dois estágios: sorteia grupos até haver N suficiente; depois pessoas."""
    validar_amostra(populacao, tamanho)
    if coluna not in populacao or populacao[coluna].isna().any():
        raise ValueError("Coluna de conglomerados inválida.")
    rng = np.random.default_rng(semente)
    grupos = rng.permutation(populacao[coluna].unique())
    escolhidos = []
    disponiveis = 0
    for grupo in grupos:
        escolhidos.append(str(grupo))
        disponiveis += int((populacao[coluna] == grupo).sum())
        if disponiveis >= tamanho:
            break
    bloco = populacao.loc[populacao[coluna].isin(escolhidos)]
    indices = rng.choice(len(bloco), size=tamanho, replace=False)
    return bloco.iloc[indices].reset_index(drop=True), escolhidos


def amostra_conveniencia(populacao: pd.DataFrame, tamanho: int) -> pd.DataFrame:
    """Regra visível: Centro, Norte, Sul, Oeste; depois posição crescente."""
    validar_amostra(populacao, tamanho)
    ordem = {"Centro": 0, "Norte": 1, "Sul": 2, "Oeste": 3}
    if not set(populacao["bairro"]).issubset(ordem):
        raise ValueError("Bairro desconhecido na população fictícia.")
    return (
        populacao.assign(_prioridade=populacao["bairro"].map(ordem))
        .sort_values(["_prioridade", "posição"])
        .head(tamanho)
        .drop(columns="_prioridade")
        .reset_index(drop=True)
    )


def composicao(populacao: pd.DataFrame, amostra: pd.DataFrame, coluna: str = "bairro") -> pd.DataFrame:
    total = populacao[coluna].value_counts(normalize=True)
    parte = amostra[coluna].value_counts(normalize=True)
    return pd.DataFrame(
        {"população (%)": (100 * total).round(1), "amostra (%)": (100 * parte).round(1)}
    ).fillna(0).sort_index()


def lancamentos_moeda(quantidade: int, semente: int) -> tuple[pd.DataFrame, float]:
    if not 1 <= quantidade <= 10000:
        raise ValueError("Use entre 1 e 10.000 lançamentos.")
    resultados = np.random.default_rng(semente).integers(0, 2, size=quantidade)
    df = pd.DataFrame({"lançamento": np.arange(1, quantidade + 1), "cara": resultados})
    df["proporção acumulada"] = df["cara"].expanding().mean()
    return df, float(df["cara"].mean())


def apurar_respostas(editadas: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Mantém valores digitados; aceita somente contagens inteiras de 0 a 14."""
    if not {"id", "treinos_semana"}.issubset(editadas.columns):
        raise ValueError("As colunas id e treinos_semana são obrigatórias.")
    auditoria = editadas[["id", "treinos_semana"]].copy()
    numeros = pd.to_numeric(auditoria["treinos_semana"], errors="coerce")
    validos = numeros.notna() & np.isfinite(numeros) & numeros.between(0, 14) & (numeros % 1 == 0)
    auditoria["tratamento"] = np.where(validos, "Incluído", "Excluído: valor inválido")
    limpos = auditoria.loc[validos, ["id"]].copy()
    limpos["treinos_semana"] = numeros.loc[validos].astype(int)
    return auditoria, limpos.reset_index(drop=True)


def analisar_treinos(limpos: pd.DataFrame) -> dict[str, float]:
    if limpos.empty:
        return {"n": 0, "media": math.nan, "proporcao_ativa": math.nan}
    dados = limpos["treinos_semana"].to_numpy(dtype=float)
    return {"n": len(dados), "media": float(np.mean(dados)), "proporcao_ativa": float(np.mean(dados >= 3))}


def analisar_sequencia(texto: str) -> list[float]:
    partes = [p.strip() for p in texto.replace(";", ",").split(",")]
    if not partes or any(not p for p in partes):
        raise ValueError("Informe números separados por vírgulas; não deixe termos vazios.")
    try:
        valores = [float(p) for p in partes]
    except ValueError as exc:
        raise ValueError("A sequência contém um valor que não é número.") from exc
    if len(valores) > 100 or not all(math.isfinite(v) for v in valores):
        raise ValueError("Use até 100 valores finitos.")
    return valores


def indices_validos(inferior: int, superior: int, excluidos: Iterable[int] = ()) -> list[int]:
    if not isinstance(inferior, int) or not isinstance(superior, int) or inferior < 1 or superior < inferior:
        raise ValueError("Use limites inteiros com 1 ≤ inferior ≤ superior.")
    if superior - inferior > 100:
        raise ValueError("Use no máximo 101 posições no laboratório.")
    retirar = {i for i in excluidos if isinstance(i, int) and inferior <= i <= superior}
    return [i for i in range(inferior, superior + 1) if i not in retirar]


def contar_termos(inferior: int, superior: int, excluidos: Iterable[int] = ()) -> int:
    return len(indices_validos(inferior, superior, excluidos))


MODELOS = {
    "xᵢ": "x_i",
    "i": "i",
    "xᵢ²": "x_i^2",
    "xᵢ × yᵢ": "x_i y_i",
    "xᵢ + yᵢ": "x_i+y_i",
    "c × xᵢ": "c x_i",
    "xᵢ + c": "x_i+c",
    "constante c": "c",
    "xᵢ / xᵢ₊₁": "x_i/x_{i+1}",
    "a elevado a xᵢ": "a^{x_i}",
    "r elevado a (i−1)": "r^{i-1}",
}


def calcular_laboratorio(
    operacao: str,
    modelo: str,
    x: list[float],
    y: list[float],
    inferior: int,
    superior: int,
    excluidos: Iterable[int] = (),
    constante: float = 2.0,
) -> tuple[pd.DataFrame, float]:
    """Avalia somente modelos predefinidos; índices matemáticos começam em 1."""
    if operacao not in {"Soma", "Produto"} or modelo not in MODELOS:
        raise ValueError("Operação ou modelo desconhecido.")
    if not math.isfinite(constante):
        raise ValueError("A constante deve ser finita.")
    indices = indices_validos(inferior, superior, excluidos)
    if modelo == "xᵢ / xᵢ₊₁" and superior >= len(x):
        raise ValueError("O produto telescópico requer x_(superior+1).")
    precisa_x = modelo not in {"i", "constante c", "r elevado a (i−1)"}
    precisa_y = modelo in {"xᵢ × yᵢ", "xᵢ + yᵢ"}
    if (precisa_x and superior > len(x)) or (precisa_y and superior > len(y)):
        raise ValueError("Os limites ultrapassam a sequência necessária.")
    acumulado = 0.0 if operacao == "Soma" else 1.0
    linhas = []
    for i in indices:
        xi = x[i - 1] if precisa_x else 0.0
        yi = y[i - 1] if precisa_y else 0.0
        if modelo == "xᵢ": termo = xi
        elif modelo == "i": termo = float(i)
        elif modelo == "xᵢ²": termo = xi**2
        elif modelo == "xᵢ × yᵢ": termo = xi * yi
        elif modelo == "xᵢ + yᵢ": termo = xi + yi
        elif modelo == "c × xᵢ": termo = constante * xi
        elif modelo == "xᵢ + c": termo = xi + constante
        elif modelo == "constante c": termo = constante
        elif modelo == "a elevado a xᵢ": termo = constante**xi
        elif modelo == "r elevado a (i−1)": termo = constante ** (i - 1)
        else:
            denominador = x[i]
            if denominador == 0:
                raise ValueError(f"Divisão por zero em x_{i+1}.")
            termo = xi / denominador
        if isinstance(termo, complex) or not math.isfinite(termo):
            raise ValueError("Termo indefinido ou grande demais.")
        acumulado = acumulado + termo if operacao == "Soma" else acumulado * termo
        if not math.isfinite(acumulado):
            raise ValueError("Resultado acumulado grande demais.")
        linhas.append({"índice i": i, "termo": termo, "acumulado": acumulado})
    return pd.DataFrame(linhas, columns=["índice i", "termo", "acumulado"]), acumulado


def soma_geometrica_parcial(razao: float, termos: int) -> tuple[pd.DataFrame, float | None]:
    if not math.isfinite(razao) or not 1 <= termos <= 100:
        raise ValueError("Razão finita e 1 a 100 termos são necessários.")
    indices = np.arange(termos)
    parcelas = razao**indices
    if not np.isfinite(parcelas).all():
        raise ValueError("Parcelas grandes demais.")
    tabela = pd.DataFrame({"n": indices + 1, "parcela": parcelas, "soma parcial": np.cumsum(parcelas)})
    limite = 1 / (1 - razao) if abs(razao) < 1 else None
    return tabela, limite
