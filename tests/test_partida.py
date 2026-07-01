import pytest

from showdomilhao.partida import PREMIO_RODADA_1, PREMIO_RODADA_2, Partida, Pergunta, Rodada


def perguntas(prefixo="Pergunta"):
    return [
        Pergunta(f"{prefixo} 1", ("A", "B", "C", "D"), correta=0),
        Pergunta(f"{prefixo} 2", ("A", "B", "C", "D"), correta=1),
        Pergunta(f"{prefixo} 3", ("A", "B", "C", "D"), correta=2),
        Pergunta(f"{prefixo} 4", ("A", "B", "C", "D"), correta=3),
        Pergunta(f"{prefixo} 5", ("A", "B", "C", "D"), correta=0),
    ]


def rodada_1():
    return Rodada(tuple(perguntas("R1")), premio_por_acerto=PREMIO_RODADA_1)


def rodada_2():
    return Rodada(tuple(perguntas("R2")), premio_por_acerto=PREMIO_RODADA_2)


RESPOSTAS_CORRETAS = [0, 1, 2, 3, 0]


# --- fluxo principal (1 rodada) ----------------------------------------------


def test_responder_correto_soma_premio_cumulativo():
    partida = Partida([rodada_1()])

    assert partida.responder(0) is True
    assert partida.premio == PREMIO_RODADA_1

    assert partida.responder(1) is True
    assert partida.premio == 2 * PREMIO_RODADA_1


def test_responder_errado_reduz_premio_pela_metade_e_encerra():
    # Regra confirmada por evidência primária (captura de tela do programa real,
    # 4 pontos de dado consistentes): ERRAR = PARAR / 2, não zero.
    # https://www.youtube.com/watch?v=tPJD9Qo4EN8 (3:08, 3:29, 4:04 e um quadro anterior)
    partida = Partida([rodada_1()])
    partida.responder(0)  # acerta a 1a, premio = 1000
    partida.responder(1)  # acerta a 2a, premio = 2000

    assert partida.responder(0) is False  # a 3a correta é índice 2, não 0
    assert partida.premio == 1000  # metade dos 2000 que já tinha garantido
    assert partida.finalizada is True


def test_responder_errado_na_primeira_pergunta_zera_o_premio():
    # Caso-limite do mesmo cálculo: antes da 1a pergunta o "PARAR" vale 0,
    # então ERRAR = 0 / 2 = 0 — não é uma regra separada, é a mesma fórmula.
    partida = Partida([rodada_1()])

    assert partida.responder(1) is False  # a 1a correta é índice 0, não 1
    assert partida.premio == 0
    assert partida.finalizada is True


def test_parar_preserva_premio_e_encerra():
    partida = Partida([rodada_1()])
    partida.responder(0)
    partida.responder(1)

    partida.parar()

    assert partida.premio == 2 * PREMIO_RODADA_1
    assert partida.finalizada is True


def test_completar_unica_rodada_finaliza_partida():
    partida = Partida([rodada_1()])

    for resposta in RESPOSTAS_CORRETAS:
        assert partida.responder(resposta) is True

    assert partida.premio == 5 * PREMIO_RODADA_1
    assert partida.finalizada is True


# --- transição entre rodadas --------------------------------------------------


def test_completar_rodada_1_avanca_para_rodada_2_sem_finalizar():
    partida = Partida([rodada_1(), rodada_2()])

    for resposta in RESPOSTAS_CORRETAS:
        assert partida.responder(resposta) is True

    assert partida.premio == 5 * PREMIO_RODADA_1
    assert partida.finalizada is False
    assert partida.pergunta_atual().enunciado == "R2 1"


def test_acerto_na_rodada_2_usa_o_incremento_da_rodada_2():
    partida = Partida([rodada_1(), rodada_2()])
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)  # completa a rodada 1, premio = 5000

    assert partida.responder(0) is True  # 1a da rodada 2, correta
    assert partida.premio == 5 * PREMIO_RODADA_1 + PREMIO_RODADA_2


def test_erro_logo_apos_cruzar_para_rodada_2_reduz_pela_metade_do_acumulado():
    # Confirmado pelo responsável do projeto: a regra "metade" atravessa a
    # fronteira entre rodadas, não reseta.
    partida = Partida([rodada_1(), rodada_2()])
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)  # completa a rodada 1, premio = 5000

    assert partida.responder(1) is False  # 1a da rodada 2 é índice 0, não 1
    assert partida.premio == 2500  # metade de 5000
    assert partida.finalizada is True


def test_completar_todas_as_rodadas_finaliza_partida():
    partida = Partida([rodada_1(), rodada_2()])

    for resposta in RESPOSTAS_CORRETAS * 2:
        assert partida.responder(resposta) is True

    assert partida.premio == 5 * PREMIO_RODADA_1 + 5 * PREMIO_RODADA_2
    assert partida.finalizada is True


def test_parar_na_rodada_2_preserva_o_acumulado_das_duas_rodadas():
    partida = Partida([rodada_1(), rodada_2()])
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)  # completa a rodada 1, premio = 5000
    partida.responder(0)  # 1a da rodada 2, premio = 15000

    partida.parar()

    assert partida.premio == 5 * PREMIO_RODADA_1 + PREMIO_RODADA_2
    assert partida.finalizada is True


# --- guardas contra uso indevido pós-finalização ----------------------------
# Os três caminhos de finalização (completar todas as rodadas, errar, parar) devem
# se comportar de forma idêntica e explícita: qualquer chamada depois disso levanta
# RuntimeError, em vez de um deles devolver uma Pergunta obsoleta e outro
# explodir com IndexError.


@pytest.mark.parametrize(
    "finalizar",
    [
        lambda p: [p.responder(r) for r in RESPOSTAS_CORRETAS],  # completa com sucesso
        lambda p: p.responder(1),  # erra a 1a (correta=0)
        lambda p: p.parar(),
    ],
    ids=["completou_rodada", "errou", "parou"],
)
def test_pergunta_atual_apos_finalizar_levanta_erro(finalizar):
    partida = Partida([rodada_1()])
    finalizar(partida)

    assert partida.finalizada is True
    with pytest.raises(RuntimeError):
        partida.pergunta_atual()


def test_responder_apos_finalizada_levanta_erro():
    partida = Partida([rodada_1()])
    partida.parar()

    with pytest.raises(RuntimeError):
        partida.responder(0)


def test_parar_apos_finalizada_levanta_erro():
    partida = Partida([rodada_1()])
    partida.parar()

    with pytest.raises(RuntimeError):
        partida.parar()


# --- robustez contra input inválido -----------------------------------------


@pytest.mark.parametrize("indice_invalido", [-1, 4, 99])
def test_responder_com_indice_fora_do_range_levanta_erro(indice_invalido):
    partida = Partida([rodada_1()])

    with pytest.raises(ValueError):
        partida.responder(indice_invalido)


def test_partida_exige_ao_menos_1_rodada():
    with pytest.raises(ValueError):
        Partida([])


def test_rodada_exige_exatamente_5_perguntas():
    with pytest.raises(ValueError):
        Rodada(tuple(perguntas()[:1]), premio_por_acerto=PREMIO_RODADA_1)

    with pytest.raises(ValueError):
        Rodada(
            tuple(perguntas() + [Pergunta("Extra", ("A", "B", "C", "D"), correta=0)]),
            premio_por_acerto=PREMIO_RODADA_1,
        )


def test_rodada_exige_premio_por_acerto_positivo():
    with pytest.raises(ValueError):
        Rodada(tuple(perguntas()), premio_por_acerto=0)

    with pytest.raises(ValueError):
        Rodada(tuple(perguntas()), premio_por_acerto=-1000)


def test_partida_faz_copia_defensiva_da_lista_de_rodadas():
    lista = [rodada_1()]
    partida = Partida(lista)

    lista.clear()  # mutar a lista original não deve afetar a Partida já construída

    assert partida.pergunta_atual().enunciado == "R1 1"


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
