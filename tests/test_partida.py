import pytest

from showdomilhao.partida import PREMIO_POR_ACERTO_RODADA_1, Partida, Pergunta


def perguntas_rodada_1():
    return [
        Pergunta("Pergunta 1", ("A", "B", "C", "D"), correta=0),
        Pergunta("Pergunta 2", ("A", "B", "C", "D"), correta=1),
        Pergunta("Pergunta 3", ("A", "B", "C", "D"), correta=2),
        Pergunta("Pergunta 4", ("A", "B", "C", "D"), correta=3),
        Pergunta("Pergunta 5", ("A", "B", "C", "D"), correta=0),
    ]


# --- fluxo principal -------------------------------------------------------


def test_responder_correto_soma_premio_cumulativo():
    partida = Partida(perguntas_rodada_1())

    assert partida.responder(0) is True
    assert partida.premio == PREMIO_POR_ACERTO_RODADA_1

    assert partida.responder(1) is True
    assert partida.premio == 2 * PREMIO_POR_ACERTO_RODADA_1


def test_responder_errado_reduz_premio_pela_metade_e_encerra():
    # Regra confirmada por evidência primária (captura de tela do programa real,
    # 4 pontos de dado consistentes): ERRAR = PARAR / 2, não zero.
    # https://www.youtube.com/watch?v=tPJD9Qo4EN8 (3:08, 3:29, 4:04 e um quadro anterior)
    partida = Partida(perguntas_rodada_1())
    partida.responder(0)  # acerta a 1a, premio = 1000
    partida.responder(1)  # acerta a 2a, premio = 2000

    assert partida.responder(0) is False  # a 3a correta é índice 2, não 0
    assert partida.premio == 1000  # metade dos 2000 que já tinha garantido
    assert partida.finalizada is True


def test_responder_errado_na_primeira_pergunta_zera_o_premio():
    # Caso-limite do mesmo cálculo: antes da 1a pergunta o "PARAR" vale 0,
    # então ERRAR = 0 / 2 = 0 — não é uma regra separada, é a mesma fórmula.
    partida = Partida(perguntas_rodada_1())

    assert partida.responder(1) is False  # a 1a correta é índice 0, não 1
    assert partida.premio == 0
    assert partida.finalizada is True


def test_parar_preserva_premio_e_encerra():
    partida = Partida(perguntas_rodada_1())
    partida.responder(0)
    partida.responder(1)

    partida.parar()

    assert partida.premio == 2 * PREMIO_POR_ACERTO_RODADA_1
    assert partida.finalizada is True


def test_completar_rodada_1_com_5_acertos_finaliza_partida():
    partida = Partida(perguntas_rodada_1())
    respostas_corretas = [0, 1, 2, 3, 0]

    for resposta in respostas_corretas:
        assert partida.responder(resposta) is True

    assert partida.premio == 5 * PREMIO_POR_ACERTO_RODADA_1
    assert partida.finalizada is True


# --- guardas contra uso indevido pós-finalização ----------------------------
# Os três caminhos de finalização (completar a rodada, errar, parar) devem se
# comportar de forma idêntica e explícita: qualquer chamada depois disso levanta
# RuntimeError, em vez de um deles devolver uma Pergunta obsoleta e outro
# explodir com IndexError.


@pytest.mark.parametrize(
    "finalizar",
    [
        lambda p: [p.responder(r) for r in [0, 1, 2, 3, 0]],  # completa com sucesso
        lambda p: p.responder(1),  # erra a 1a (correta=0)
        lambda p: p.parar(),
    ],
    ids=["completou_rodada", "errou", "parou"],
)
def test_pergunta_atual_apos_finalizar_levanta_erro(finalizar):
    partida = Partida(perguntas_rodada_1())
    finalizar(partida)

    assert partida.finalizada is True
    with pytest.raises(RuntimeError):
        partida.pergunta_atual()


def test_responder_apos_finalizada_levanta_erro():
    partida = Partida(perguntas_rodada_1())
    partida.parar()

    with pytest.raises(RuntimeError):
        partida.responder(0)


def test_parar_apos_finalizada_levanta_erro():
    partida = Partida(perguntas_rodada_1())
    partida.parar()

    with pytest.raises(RuntimeError):
        partida.parar()


# --- robustez contra input inválido -----------------------------------------


@pytest.mark.parametrize("indice_invalido", [-1, 4, 99])
def test_responder_com_indice_fora_do_range_levanta_erro(indice_invalido):
    partida = Partida(perguntas_rodada_1())

    with pytest.raises(ValueError):
        partida.responder(indice_invalido)


def test_partida_exige_exatamente_5_perguntas():
    with pytest.raises(ValueError):
        Partida(perguntas_rodada_1()[:1])

    with pytest.raises(ValueError):
        Partida(perguntas_rodada_1() + [Pergunta("Extra", ("A", "B", "C", "D"), correta=0)])


def test_partida_faz_copia_defensiva_da_lista_de_perguntas():
    lista = perguntas_rodada_1()
    partida = Partida(lista)

    lista.clear()  # mutar a lista original não deve afetar a Partida já construída

    assert partida.pergunta_atual().enunciado == "Pergunta 1"


@pytest.mark.parametrize(
    "alternativas,correta,mensagem",
    [
        (("A", "B", "C"), 0, "menos de 4 alternativas"),
        (("A", "B", "C", "D", "E"), 0, "mais de 4 alternativas"),
        (("A", "B", "C", "D"), 4, "correta fora do range (alto)"),
        (("A", "B", "C", "D"), -1, "correta fora do range (negativo)"),
    ],
)
def test_pergunta_invalida_levanta_erro(alternativas, correta, mensagem):
    with pytest.raises(ValueError):
        Pergunta("X", alternativas, correta=correta)


def test_pergunta_e_imutavel_e_hashable():
    pergunta = Pergunta("X", ("A", "B", "C", "D"), correta=0)

    with pytest.raises(AttributeError):
        pergunta.alternativas = ("E", "F", "G", "H")

    hash(pergunta)  # não deve levantar TypeError
