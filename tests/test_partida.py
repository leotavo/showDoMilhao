import pytest

from showdomilhao.partida import (
    PREMIO_PERGUNTA_DO_MILHAO,
    PREMIO_RODADA_1,
    PREMIO_RODADA_2,
    PREMIO_RODADA_3,
    QUANTIDADE_MAXIMA_PULOS,
    Partida,
    Pergunta,
    Rodada,
)


def sortear_fixo(carta):
    return lambda: carta


def eliminar_primeiros(errados, quantidade):
    return errados[:quantidade]


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


def rodada_3():
    return Rodada(tuple(perguntas("R3")), premio_por_acerto=PREMIO_RODADA_3)


def pergunta_do_milhao():
    return Pergunta("A pergunta que vale um milhão", ("A", "B", "C", "D"), correta=0)


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


def test_acerto_na_rodada_2_usa_a_escada_da_rodada_2_sem_somar_a_rodada_1():
    # Confirmado pelo responsável do projeto: não é soma cumulativa entre rodadas
    # ("os prêmios não são acumulados... é como uma escada") — cada rodada tem sua
    # própria escada de degraus, que substitui (não soma) o valor da rodada anterior.
    partida = Partida([rodada_1(), rodada_2()])
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)  # completa a rodada 1, premio = 5000

    assert partida.responder(0) is True  # 1a da rodada 2, correta
    assert partida.premio == PREMIO_RODADA_2  # NÃO é 5*RODADA_1 + RODADA_2


def test_erro_logo_apos_cruzar_para_rodada_2_reduz_pela_metade_do_que_ja_tinha():
    # PARAR/ERRAR são calculados sobre o que já está garantido antes desta
    # pergunta (aqui, ainda os 5000 da rodada 1 — a escada da rodada 2 só troca
    # de valor quando uma pergunta DELA é respondida corretamente).
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

    assert partida.premio == 5 * PREMIO_RODADA_2  # escada da rodada 2, não soma da 1
    assert partida.finalizada is True


def test_parar_na_rodada_2_preserva_o_valor_da_escada_da_rodada_2():
    partida = Partida([rodada_1(), rodada_2()])
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)  # completa a rodada 1, premio = 5000
    partida.responder(0)  # 1a da rodada 2, premio = 10000 (troca, não soma)

    partida.parar()

    assert partida.premio == PREMIO_RODADA_2
    assert partida.finalizada is True


def test_partida_encadeia_3_rodadas_ate_o_fim():
    # A escada da Rodada 3 completa dá exatamente R$500 mil — o mesmo valor de
    # "parar" já documentado no README pra Pergunta do Milhão. Não é coincidência:
    # é a mesma escada continuando.
    partida = Partida([rodada_1(), rodada_2(), rodada_3()])

    for resposta in RESPOSTAS_CORRETAS * 3:
        assert partida.responder(resposta) is True

    assert partida.premio == 5 * PREMIO_RODADA_3
    assert partida.finalizada is True


def test_erro_na_rodada_3_reduz_pela_metade_do_valor_da_escada_da_rodada_2():
    partida = Partida([rodada_1(), rodada_2(), rodada_3()])
    for resposta in RESPOSTAS_CORRETAS * 2:
        partida.responder(resposta)  # completa rodadas 1 e 2, premio = 5*RODADA_2 = 50000

    assert partida.responder(1) is False  # 1a da rodada 3 é índice 0, não 1
    assert partida.premio == 25000  # metade de 50000
    assert partida.finalizada is True


# --- ajuda: Pulos -------------------------------------------------------------


def test_partida_comeca_com_o_maximo_de_pulos():
    partida = Partida([rodada_1()])

    assert partida.pulos_restantes == QUANTIDADE_MAXIMA_PULOS


def test_pular_avanca_pergunta_sem_alterar_o_premio():
    partida = Partida([rodada_1()])
    partida.responder(0)  # acerta a 1a, premio = 1000

    partida.pular()

    assert partida.premio == PREMIO_RODADA_1  # não ganhou nem perdeu
    assert partida.pergunta_atual().enunciado == "R1 3"
    assert partida.finalizada is False


def test_pular_antes_de_acertar_nao_infla_o_degrau_da_escada():
    # pular() avança _indice_pergunta sem contar como acerto — a escada tem que
    # subir pela quantidade de ACERTOS na rodada, não pela posição na sequência
    # de perguntas (que pular também avança).
    partida = Partida([rodada_1()])
    partida.pular()  # pula a 1a, ainda 0 acertos

    assert partida.responder(1) is True  # acerta a 2a (correta=1)
    assert partida.premio == PREMIO_RODADA_1  # 1º acerto da rodada, não o 2º degrau


def test_pular_reduz_pulos_restantes():
    partida = Partida([rodada_1()])

    partida.pular()

    assert partida.pulos_restantes == QUANTIDADE_MAXIMA_PULOS - 1


def test_pular_sem_pulos_restantes_levanta_erro():
    partida = Partida([rodada_1()])
    for _ in range(QUANTIDADE_MAXIMA_PULOS):
        partida.pular()

    assert partida.pulos_restantes == 0
    with pytest.raises(RuntimeError):
        partida.pular()


def test_pular_atravessa_fronteira_de_rodada():
    # QUANTIDADE_MAXIMA_PULOS (3) < QUANTIDADE_PERGUNTAS_POR_RODADA (5): responde
    # certo as 2 primeiras e pula as 3 últimas (todo o orçamento de pulos) pra
    # cruzar a fronteira sem estourar o limite.
    partida = Partida([rodada_1(), rodada_2()])
    partida.responder(RESPOSTAS_CORRETAS[0])
    partida.responder(RESPOSTAS_CORRETAS[1])
    for _ in range(QUANTIDADE_MAXIMA_PULOS):
        partida.pular()

    assert partida.finalizada is False
    assert partida.pulos_restantes == 0
    assert partida.pergunta_atual().enunciado == "R2 1"


def test_pular_a_ultima_pergunta_da_ultima_rodada_finaliza_partida():
    partida = Partida([rodada_1()])
    for resposta in RESPOSTAS_CORRETAS[:4]:
        partida.responder(resposta)  # responde certo as 4 primeiras, chega na 5a

    partida.pular()  # pula a 5a e última pergunta da única rodada

    assert partida.finalizada is True


def test_pular_apos_finalizada_levanta_erro():
    partida = Partida([rodada_1()])
    partida.parar()

    with pytest.raises(RuntimeError):
        partida.pular()


# --- ajuda: Cartas --------------------------------------------------------------
# Sorteio uniforme (25% cada) aprovado via HITL. Injeção de sortear_carta/
# escolher_eliminados deixa o comportamento determinístico nos testes.


def test_usar_cartas_as_elimina_1_alternativa_errada():
    partida = Partida(
        [rodada_1()], sortear_carta=sortear_fixo("Ás"), escolher_eliminados=eliminar_primeiros
    )

    carta, eliminadas = partida.usar_cartas()

    assert carta == "Ás"
    assert len(eliminadas) == 1
    assert partida.pergunta_atual().correta not in eliminadas


def test_usar_cartas_2_elimina_2_alternativas_erradas():
    partida = Partida(
        [rodada_1()], sortear_carta=sortear_fixo("2"), escolher_eliminados=eliminar_primeiros
    )

    carta, eliminadas = partida.usar_cartas()

    assert carta == "2"
    assert len(eliminadas) == 2
    assert partida.pergunta_atual().correta not in eliminadas


def test_usar_cartas_3_elimina_3_alternativas_so_resta_a_correta():
    partida = Partida(
        [rodada_1()], sortear_carta=sortear_fixo("3"), escolher_eliminados=eliminar_primeiros
    )

    carta, eliminadas = partida.usar_cartas()

    assert carta == "3"
    assert len(eliminadas) == 3
    assert partida.pergunta_atual().correta not in eliminadas


def test_usar_cartas_rei_nao_elimina_nenhuma():
    partida = Partida([rodada_1()], sortear_carta=sortear_fixo("Rei"))

    carta, eliminadas = partida.usar_cartas()

    assert carta == "Rei"
    assert eliminadas == ()


def test_usar_cartas_nao_altera_premio_nem_avanca_pergunta():
    partida = Partida([rodada_1()], sortear_carta=sortear_fixo("2"))
    pergunta_antes = partida.pergunta_atual()

    partida.usar_cartas()

    assert partida.premio == 0
    assert partida.pergunta_atual() is pergunta_antes
    assert partida.finalizada is False


def test_usar_cartas_so_pode_ser_usada_uma_vez():
    # Ajuda de uso único por partida — o README não dá uma contagem explícita
    # pra Cartas (só Pulos tem "até 3 vezes"), então trato como single-use por
    # inferência do contraste textual; ver docs/licoes-aprendidas.md.
    partida = Partida([rodada_1()], sortear_carta=sortear_fixo("Rei"))
    partida.usar_cartas()

    with pytest.raises(RuntimeError):
        partida.usar_cartas()


def test_usar_cartas_apos_finalizada_levanta_erro():
    partida = Partida([rodada_1()])
    partida.parar()

    with pytest.raises(RuntimeError):
        partida.usar_cartas()


def test_usar_cartas_distribuicao_padrao_cobre_as_4_cartas():
    # Smoke test estatístico contra a implementação real (sem RNG injetado) —
    # só prova que o sorteio não está hardcoded numa carta só. Janela bem larga
    # (25 a 175 em 400 sorteios, esperado ~100) pra não ser flaky.
    from collections import Counter

    contagem = Counter()
    for _ in range(400):
        partida = Partida([rodada_1()])
        carta, _ = partida.usar_cartas()
        contagem[carta] += 1

    assert set(contagem) == {"Ás", "2", "3", "Rei"}
    for quantidade in contagem.values():
        assert 25 < quantidade < 175


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


# --- Pergunta do Milhão ------------------------------------------------------
# Regras já 100% confirmadas no README: R$1.000.000 se acertar, R$0 se errar
# (não metade — exceção explícita à regra normal), R$500 mil se parar (mesmo
# valor de completar a Rodada 3), nenhuma ajuda pode ser usada.


def test_completar_ultima_rodada_com_pergunta_final_nao_finaliza_a_partida():
    partida = Partida([rodada_1()], pergunta_final=pergunta_do_milhao())

    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)

    assert partida.finalizada is False
    assert partida.premio == 5 * PREMIO_RODADA_1
    assert partida.pergunta_atual().enunciado == "A pergunta que vale um milhão"


def test_acertar_pergunta_final_da_premio_do_milhao():
    partida = Partida([rodada_1()], pergunta_final=pergunta_do_milhao())
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)

    assert partida.responder(0) is True  # correta=0

    assert partida.premio == PREMIO_PERGUNTA_DO_MILHAO
    assert partida.finalizada is True


def test_errar_pergunta_final_zera_o_premio_em_vez_de_reduzir_pela_metade():
    # Exceção explícita à regra normal (README): "Erro na final zera o prêmio."
    partida = Partida([rodada_1()], pergunta_final=pergunta_do_milhao())
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)  # premio = 5000

    assert partida.responder(1) is False  # errada

    assert partida.premio == 0  # não 2500 (metade), como seria numa rodada normal
    assert partida.finalizada is True


def test_parar_na_pergunta_final_preserva_o_premio_da_ultima_rodada():
    partida = Partida([rodada_1()], pergunta_final=pergunta_do_milhao())
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)  # premio = 5000

    partida.parar()

    assert partida.premio == 5 * PREMIO_RODADA_1
    assert partida.finalizada is True


def test_pular_na_pergunta_final_levanta_erro():
    partida = Partida([rodada_1()], pergunta_final=pergunta_do_milhao())
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)

    with pytest.raises(RuntimeError):
        partida.pular()


def test_usar_cartas_na_pergunta_final_levanta_erro():
    partida = Partida([rodada_1()], pergunta_final=pergunta_do_milhao())
    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)

    with pytest.raises(RuntimeError):
        partida.usar_cartas()


def test_partida_sem_pergunta_final_finaliza_normalmente_apos_ultima_rodada():
    # Compatibilidade: pergunta_final é opcional (default None), comportamento
    # anterior preservado pra quem não passar esse parâmetro.
    partida = Partida([rodada_1()])

    for resposta in RESPOSTAS_CORRETAS:
        partida.responder(resposta)

    assert partida.finalizada is True
    assert partida.premio == 5 * PREMIO_RODADA_1
