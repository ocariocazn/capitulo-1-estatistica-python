"""Verificações numéricas e de sorteio; compatível com pytest e unittest."""

import math
import unittest

import pandas as pd

import calculations as c


class TestAmostragem(unittest.TestCase):
    def setUp(self):
        self.pop = c.criar_populacao(103)

    def verificar_amostra(self, amostra, n):
        self.assertEqual(len(amostra), n)
        self.assertTrue(amostra["id"].is_unique)
        self.assertTrue(set(amostra["id"]).issubset(set(self.pop["id"])))

    def test_populacao_ficticia(self):
        self.assertTrue(self.pop["id"].is_unique)
        self.assertEqual(self.pop["id"].iloc[0], "P0001")
        with self.assertRaises(ValueError):
            c.criar_populacao(0)

    def test_aleatoria_reprodutivel_sem_reposicao(self):
        a = c.amostra_aleatoria(self.pop, 42, 99)
        b = c.amostra_aleatoria(self.pop, 42, 99)
        self.assertEqual(a["id"].tolist(), b["id"].tolist())
        self.verificar_amostra(a, 42)
        for n in (1, 102, 103):
            self.verificar_amostra(c.amostra_aleatoria(self.pop, n, 7), n)

    def test_alocacao_maiores_restos(self):
        contagens = pd.Series({"A": 7, "B": 5})
        self.assertEqual(c.alocacao_proporcional(contagens, 5).to_dict(), {"A": 3, "B": 2})
        for n in range(1, 13):
            a = c.alocacao_proporcional(contagens, n)
            self.assertEqual(int(a.sum()), n)
            self.assertTrue((a <= contagens).all())
        with self.assertRaises(ValueError):
            c.alocacao_proporcional(contagens, 13)

    def test_estratificada(self):
        a, cotas = c.amostra_estratificada(self.pop, 37, 8)
        b, _ = c.amostra_estratificada(self.pop, 37, 8)
        self.verificar_amostra(a, 37)
        self.assertEqual(a["id"].tolist(), b["id"].tolist())
        self.assertEqual(int(cotas.sum()), 37)
        self.assertEqual(a["faixa"].value_counts().to_dict(), cotas.to_dict())

    def test_sistematica_com_divisao_nao_inteira(self):
        for n in (1, 2, 3, 17, 34, 102, 103):
            for semente in (0, 1, 42):
                a, inicio, posicoes = c.amostra_sistematica(self.pop, n, semente)
                b, _, mesmas = c.amostra_sistematica(self.pop, n, semente)
                self.verificar_amostra(a, n)
                self.assertEqual(posicoes, mesmas)
                self.assertEqual(a["id"].tolist(), b["id"].tolist())
                self.assertEqual(len(set(posicoes)), n)
                self.assertTrue(all(1 <= p <= len(self.pop) for p in posicoes))
                self.assertGreaterEqual(inicio, 0)

    def test_conglomerados_e_conveniencia(self):
        a, grupos = c.amostra_conglomerados(self.pop, 30, 3)
        b, mesmos = c.amostra_conglomerados(self.pop, 30, 3)
        self.verificar_amostra(a, 30)
        self.assertEqual(grupos, mesmos)
        self.assertEqual(a["id"].tolist(), b["id"].tolist())
        self.assertTrue(set(a["bairro"]).issubset(grupos))
        v = c.amostra_conveniencia(self.pop, 15)
        self.verificar_amostra(v, 15)
        self.assertEqual(set(v["bairro"]), {"Centro"})

    def test_tamanhos_invalidos(self):
        for n in (0, 104):
            with self.assertRaises(ValueError):
                c.amostra_aleatoria(self.pop, n, 1)
            with self.assertRaises(ValueError):
                c.amostra_sistematica(self.pop, n, 1)
        repetida = pd.concat([self.pop.iloc[:1], self.pop.iloc[:1]], ignore_index=True)
        with self.assertRaises(ValueError):
            c.amostra_aleatoria(repetida, 1, 1)


class TestLaboratorio(unittest.TestCase):
    def setUp(self):
        self.x = [2.0, 4.0, 6.0, 8.0]
        self.y = [1.0, 3.0, 5.0, 7.0]

    def calc(self, op, modelo, p=1, q=3, excluidos=(), cte=2):
        return c.calcular_laboratorio(op, modelo, self.x, self.y, p, q, excluidos, cte)[1]

    def test_somas_produtos_e_quadrados(self):
        self.assertEqual(self.calc("Soma", "xᵢ"), 12)
        self.assertEqual(self.calc("Soma", "xᵢ²"), 56)
        self.assertNotEqual(self.calc("Soma", "xᵢ²"), self.calc("Soma", "xᵢ") ** 2)
        self.assertEqual(self.calc("Soma", "xᵢ × yᵢ"), 44)
        self.assertEqual(self.calc("Produto", "xᵢ"), 48)
        self.assertEqual(self.calc("Produto", "xᵢ + yᵢ"), 3 * 7 * 11)

    def test_constantes_e_potencias(self):
        self.assertEqual(self.calc("Soma", "c × xᵢ", cte=3), 36)
        self.assertEqual(self.calc("Soma", "xᵢ + c", cte=3), 21)
        self.assertEqual(self.calc("Soma", "constante c", cte=3), 9)
        self.assertEqual(self.calc("Produto", "constante c", cte=3), 3**3)
        self.assertEqual(self.calc("Produto", "c × xᵢ", cte=3), 3**3 * 48)
        self.assertEqual(self.calc("Produto", "a elevado a xᵢ", cte=2), 2**sum(self.x[:3]))

    def test_telescopico(self):
        self.assertAlmostEqual(self.calc("Produto", "xᵢ / xᵢ₊₁"), self.x[0] / self.x[3])
        with self.assertRaises(ValueError):
            self.calc("Produto", "xᵢ / xᵢ₊₁", 1, 4)
        with self.assertRaises(ValueError):
            c.calcular_laboratorio("Produto", "xᵢ / xᵢ₊₁", [2, 0, 4], self.y, 1, 2)

    def test_exclusoes_repetidas_fora_do_intervalo(self):
        self.assertEqual(c.contar_termos(2, 8, [3, 3, 5, 99]), 5)
        tabela, total = c.calcular_laboratorio("Soma", "i", self.x, self.y, 1, 3, [2, 2, 9])
        self.assertEqual(tabela["índice i"].tolist(), [1, 3])
        self.assertEqual(total, 4)
        self.assertEqual(c.calcular_laboratorio("Produto", "i", self.x, self.y, 1, 1, [1])[1], 1)

    def test_entradas_invalidas(self):
        for p, q in ((0, 2), (3, 2), (1, 102)):
            with self.assertRaises(ValueError):
                c.indices_validos(p, q)
        with self.assertRaises(ValueError):
            self.calc("Soma", "modelo livre")
        with self.assertRaises(ValueError):
            c.analisar_sequencia("1,,2")
        with self.assertRaises(ValueError):
            c.analisar_sequencia("1, nan")

    def test_soma_geometrica_parcial(self):
        tabela, limite = c.soma_geometrica_parcial(0.5, 10)
        self.assertAlmostEqual(tabela["soma parcial"].iloc[-1], 2 * (1 - 0.5**10))
        self.assertEqual(limite, 2)
        _, limite = c.soma_geometrica_parcial(1.2, 4)
        self.assertIsNone(limite)


class TestEstudo(unittest.TestCase):
    def test_apuracao_preserva_entrada(self):
        dados = pd.DataFrame({"id": ["A", "B", "C", "D"], "treinos_semana": ["2", "sem resposta", "3.5", "15"]})
        antes = dados.copy(deep=True)
        auditoria, limpos = c.apurar_respostas(dados)
        pd.testing.assert_frame_equal(dados, antes)
        self.assertEqual(auditoria["treinos_semana"].tolist(), antes["treinos_semana"].tolist())
        self.assertEqual(limpos["treinos_semana"].tolist(), [2])
        resumo = c.analisar_treinos(limpos)
        self.assertEqual(resumo["media"], 2)
        self.assertEqual(resumo["proporcao_ativa"], 0)
        self.assertTrue(math.isnan(c.analisar_treinos(limpos.iloc[:0])["media"]))


if __name__ == "__main__":
    unittest.main()
