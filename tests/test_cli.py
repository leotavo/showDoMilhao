from showdomilhao.cli import (
    formatar_pergunta,
    formatar_resultado,
    interpretar_entrada,
    jogar,
    rodadas_padrao,
)
from showdomilhao.partida import PREMIO_RODADA_1, Partida, Pergunta, Rodada


def perguntas_rodada_1():
    return [
        Pergunta("Pergunta 1", ("A", "B", "C", "D"), correta=0),
        Pergunta("Pergunta 2", ("A", "B", "C", "D"), correta=1),
        Pergunta("Pergunta 3", ("A", "B", "C", "D"), correta=2),
        Pergunta("Pergunta 4", ("A", "B", "C", "D"), correta=3),
        Pergunta("Pergunta 5", ("A", "B", "C", "D"), correta=0),
    ]


def partida_uma_rodada():
    return Partida([Rodada(tuple(perguntas_rodada_1()), premio_por_acerto=PREMIO_RODADA_1)])


def entrada_fake(respostas):
    fila = list(respostas)

    def _entrada(_prompt):
        return fila.pop(0)

    return _entrada


def saida_fake():
    linhas = []
    return linhas, linhas.append


# --- formatar_pergunta / formatar_resultado ---------------------------------


def test_formatar_pergunta_inclui_enunciado_e_alternativas_lettradas():
    pergunta = Pergunta("Qual a capital da França?", ("Londres", "Paris", "Roma", "Berlim"), correta=1)

    texto = formatar_pergunta(pergunta)

    assert "Qual a capital da França?" in texto
    assert "A) Londres" in texto
    assert "B) Paris" in texto
    assert "C) Roma" in texto
    assert "D) Berlim" in texto


def test_formatar_resultado_acerto_e_erro():
    assert "R$ 1000" in formatar_resultado(True, 1000)
    assert "R$ 500" in formatar_resultado(False, 500)


def test_formatar_pergunta_sem_eliminadas_nao_marca_nada():
    pergunta = Pergunta("X", ("A", "B", "C", "D"), correta=0)

    assert "(eliminada)" not in formatar_pergunta(pergunta)


def test_formatar_pergunta_marca_alternativas_eliminadas():
    pergunta = Pergunta(
        "Qual a capital da França?", ("Londres", "Paris", "Roma", "Berlim"), correta=1
    )

    texto = formatar_pergunta(pergunta, eliminadas=frozenset({0, 2}))
    por_letra = {linha[0]: linha for linha in texto.splitlines() if linha[:1] in "ABCD"}

    assert "(eliminada)" in por_letra["A"]
    assert "(eliminada)" not in por_letra["B"]
    assert "(eliminada)" in por_letra["C"]
    assert "(eliminada)" not in por_letra["D"]


# --- interpretar_entrada -----------------------------------------------------


def test_interpretar_entrada_aceita_letra_maiuscula_ou_minuscula():
    assert interpretar_entrada("A", 4) == 0
    assert interpretar_entrada("b", 4) == 1
    assert interpretar_entrada("D", 4) == 3


def test_interpretar_entrada_aceita_numero():
    assert interpretar_entrada("1", 4) == 0
    assert interpretar_entrada("4", 4) == 3


def test_interpretar_entrada_aceita_parar_case_insensitive():
    assert interpretar_entrada("parar", 4) == "parar"
    assert interpretar_entrada("PARAR", 4) == "parar"
    assert interpretar_entrada("p", 4) == "parar"


def test_interpretar_entrada_invalida_retorna_none():
    assert interpretar_entrada("", 4) is None
    assert interpretar_entrada("xyz", 4) is None
    assert interpretar_entrada("0", 4) is None  # 1-indexado pro usuário, 0 é fora do range
    assert interpretar_entrada("5", 4) is None  # só existem 4 alternativas
    assert interpretar_entrada("E", 4) is None


def test_interpretar_entrada_com_digito_nao_decimal_nao_lanca_excecao():
    # '²' (sobrescrito) passa em str.isdigit() mas int('²') levanta ValueError.
    # interpretar_entrada precisa tratar isso como entrada inválida, não crashar.
    assert interpretar_entrada("²", 4) is None


def test_interpretar_entrada_aceita_pular_case_insensitive():
    assert interpretar_entrada("pular", 4) == "pular"
    assert interpretar_entrada("PULAR", 4) == "pular"
    assert interpretar_entrada("pu", 4) == "pular"


def test_interpretar_entrada_aceita_cartas_case_insensitive():
    assert interpretar_entrada("cartas", 4) == "cartas"
    assert interpretar_entrada("CARTAS", 4) == "cartas"
    assert interpretar_entrada("ca", 4) == "cartas"


# --- jogar (loop com entrada/saida injetadas, sem tocar input()/print() reais) ---


def test_jogar_com_todas_respostas_corretas_termina_com_premio_maximo():
    partida = partida_uma_rodada()
    entrada = entrada_fake(["A", "B", "C", "D", "A"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 5000
    assert any("5000" in linha for linha in linhas)


def test_jogar_para_no_meio_preserva_premio():
    partida = partida_uma_rodada()
    entrada = entrada_fake(["A", "B", "parar"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 2000


def test_jogar_erra_reduz_premio_pela_metade_e_encerra():
    partida = partida_uma_rodada()
    entrada = entrada_fake(["A", "B", "A"])  # erra a 3a (correta é C/índice 2)
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 1000  # metade dos 2000 que já tinha


def test_jogar_com_eof_na_entrada_encerra_sem_lancar_excecao():
    # input() real levanta EOFError quando o stdin fecha (Ctrl+D, pipe que acaba).
    # jogar() precisa terminar graciosamente, não deixar a exceção propagar.
    partida = partida_uma_rodada()
    entrada = entrada_fake(["A"])  # só 1 resposta na fila; a 2a chamada estoura EOFError
    linhas, saida = saida_fake()

    def entrada_com_eof(prompt):
        try:
            return entrada(prompt)
        except IndexError:
            raise EOFError from None

    jogar(partida, entrada=entrada_com_eof, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 1000  # preserva o que já tinha, como um "parar"


def test_jogar_com_entrada_invalida_pede_de_novo_sem_avancar():
    partida = partida_uma_rodada()
    entrada = entrada_fake(["xyz", "A", "B", "C", "D", "A"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 5000
    assert any("inválida" in linha.lower() for linha in linhas)


def test_jogar_com_pular_avanca_sem_responder_e_sem_gastar_premio():
    partida = partida_uma_rodada()
    entrada = entrada_fake(["pular", "B", "C", "D", "A"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 4000  # 4 acertos, 1 pergunta pulada (sem prêmio nem perda)
    assert partida.pulos_restantes == 2
    assert any("pulou" in linha.lower() for linha in linhas)


def test_jogar_com_pulos_esgotados_trata_como_invalido_sem_crashar():
    # Gasta os 3 pulos (chega na pergunta 4), tenta um 4º pulo (deve ser recusado
    # sem lançar exceção nem consumir a pergunta atual), depois termina a rodada.
    partida = partida_uma_rodada()
    entrada = entrada_fake(["pular", "pular", "pular", "pular", "D", "A"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 2000  # só as 2 respostas certas (D, A) valeram prêmio
    assert partida.pulos_restantes == 0
    assert any("sem pulos" in linha.lower() for linha in linhas)


def test_jogar_com_cartas_elimina_alternativas_sem_avancar_pergunta():
    partida = Partida(
        [Rodada(tuple(perguntas_rodada_1()), premio_por_acerto=PREMIO_RODADA_1)],
        sortear_carta=lambda: "2",
        escolher_eliminados=lambda errados, quantidade: errados[:quantidade],
    )
    entrada = entrada_fake(["cartas", "A", "parar"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.cartas_usada is True
    assert partida.finalizada is True
    assert partida.premio == 1000  # só a resposta certa (A) valeu; a ajuda não mexe no prêmio
    assert any("(eliminada)" in linha for linha in linhas)


def test_jogar_com_cartas_ja_usada_trata_como_invalido_sem_crashar():
    partida = Partida(
        [Rodada(tuple(perguntas_rodada_1()), premio_por_acerto=PREMIO_RODADA_1)],
        sortear_carta=lambda: "Rei",
    )
    entrada = entrada_fake(["cartas", "cartas", "A", "parar"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert any("já foi usada" in linha.lower() for linha in linhas)


def test_jogar_atravessa_rodada_1_para_rodada_2_sem_interrupcao():
    perguntas_r2 = [
        Pergunta("Pergunta R2-1", ("A", "B", "C", "D"), correta=1),
        Pergunta("Pergunta R2-2", ("A", "B", "C", "D"), correta=2),
        Pergunta("Pergunta R2-3", ("A", "B", "C", "D"), correta=3),
        Pergunta("Pergunta R2-4", ("A", "B", "C", "D"), correta=0),
        Pergunta("Pergunta R2-5", ("A", "B", "C", "D"), correta=1),
    ]
    partida = Partida(
        [
            Rodada(tuple(perguntas_rodada_1()), premio_por_acerto=PREMIO_RODADA_1),
            Rodada(tuple(perguntas_r2), premio_por_acerto=10_000),
        ]
    )
    entrada = entrada_fake(["A", "B", "C", "D", "A", "B", "C", "D", "A", "B"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 5 * 10_000  # escada da rodada 2, não soma com a rodada 1
    assert any("Pergunta R2-1" in linha for linha in linhas)  # provou que cruzou a fronteira


def test_jogar_completa_as_3_rodadas_padrao_com_premio_maximo():
    partida = Partida(rodadas_padrao())
    respostas_corretas = [
        "B", "B", "C", "C", "B",  # Rodada 1
        "B", "D", "B", "B", "C",  # Rodada 2
        "B", "C", "B", "C", "C",  # Rodada 3
    ]
    entrada = entrada_fake(respostas_corretas)
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 5 * 100_000  # escada da rodada 3 = R$500 mil


def test_jogar_acerta_pergunta_final_ganha_o_premio_do_milhao():
    pergunta_final = Pergunta("A pergunta que vale um milhão", ("A", "B", "C", "D"), correta=0)
    partida = Partida(
        [Rodada(tuple(perguntas_rodada_1()), premio_por_acerto=PREMIO_RODADA_1)],
        pergunta_final=pergunta_final,
    )
    entrada = entrada_fake(["A", "B", "C", "D", "A", "A"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 1_000_000


def test_jogar_erra_pergunta_final_zera_o_premio():
    pergunta_final = Pergunta("A pergunta que vale um milhão", ("A", "B", "C", "D"), correta=0)
    partida = Partida(
        [Rodada(tuple(perguntas_rodada_1()), premio_por_acerto=PREMIO_RODADA_1)],
        pergunta_final=pergunta_final,
    )
    entrada = entrada_fake(["A", "B", "C", "D", "A", "B"])  # erra a final (correta é A)
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 0


def test_jogar_pular_na_pergunta_final_trata_como_invalido_sem_crashar():
    pergunta_final = Pergunta("A pergunta que vale um milhão", ("A", "B", "C", "D"), correta=0)
    partida = Partida(
        [Rodada(tuple(perguntas_rodada_1()), premio_por_acerto=PREMIO_RODADA_1)],
        pergunta_final=pergunta_final,
    )
    entrada = entrada_fake(["A", "B", "C", "D", "A", "pular", "parar"])
    linhas, saida = saida_fake()

    jogar(partida, entrada=entrada, saida=saida)

    assert partida.finalizada is True
    assert partida.premio == 5_000  # preservado, veio da última rodada
    assert any("nenhuma ajuda" in linha.lower() for linha in linhas)
