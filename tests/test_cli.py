from showdomilhao.cli import formatar_pergunta, formatar_resultado, interpretar_entrada, jogar
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
    assert partida.premio == 5_000 + 5 * 10_000
    assert any("Pergunta R2-1" in linha for linha in linhas)  # provou que cruzou a fronteira
