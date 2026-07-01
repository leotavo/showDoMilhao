import sys

from showdomilhao.partida import PREMIO_RODADA_1, PREMIO_RODADA_2, Partida, Pergunta, Rodada


def formatar_pergunta(pergunta: Pergunta) -> str:
    linhas = [pergunta.enunciado]
    for indice, alternativa in enumerate(pergunta.alternativas):
        letra = chr(ord("A") + indice)
        linhas.append(f"{letra}) {alternativa}")
    return "\n".join(linhas)


def formatar_resultado(acertou: bool, premio: int) -> str:
    if acertou:
        return f"Certa resposta! Prêmio atual: R$ {premio}"
    return f"Resposta errada. Prêmio caiu para R$ {premio}"


def interpretar_entrada(texto: str, quantidade_alternativas: int) -> int | str | None:
    normalizado = texto.strip().lower()

    if normalizado in ("parar", "p"):
        return "parar"

    if normalizado in ("pular", "pu"):
        return "pular"

    if len(normalizado) == 1 and normalizado.isalpha():
        indice = ord(normalizado) - ord("a")
        return indice if 0 <= indice < quantidade_alternativas else None

    if normalizado.isdecimal():  # isdigit() aceita '²' etc., que int() não converte
        indice = int(normalizado) - 1
        return indice if 0 <= indice < quantidade_alternativas else None

    return None


def jogar(partida: Partida, entrada=input, saida=print) -> None:
    while not partida.finalizada:
        pergunta = partida.pergunta_atual()
        saida(formatar_pergunta(pergunta))

        try:
            texto = entrada(
                f"Responda (A-D), 'parar' ou 'pular' ({partida.pulos_restantes} restantes): "
            )
        except EOFError:
            saida("Entrada encerrada. Encerrando o jogo.")
            partida.parar()
            break

        comando = interpretar_entrada(texto, len(pergunta.alternativas))

        if comando is None:
            saida("Entrada inválida, tente novamente.")
            continue

        if comando == "parar":
            partida.parar()
            break

        if comando == "pular":
            if partida.pulos_restantes <= 0:
                saida("Sem pulos restantes, responda ou digite 'parar'.")
                continue
            partida.pular()
            saida(f"Pulou! Pulos restantes: {partida.pulos_restantes}")
            continue

        acertou = partida.responder(comando)
        saida(formatar_resultado(acertou, partida.premio))

    saida(f"Fim de jogo. Prêmio final: R$ {partida.premio}")


def perguntas_padrao_rodada_1() -> tuple[Pergunta, ...]:
    return (
        Pergunta(
            "Qual é a capital do Brasil?",
            ("Rio de Janeiro", "Brasília", "São Paulo", "Salvador"),
            correta=1,
        ),
        Pergunta("Quanto é 7 x 8?", ("54", "56", "58", "64"), correta=1),
        Pergunta(
            "Quem pintou a Mona Lisa?",
            ("Michelangelo", "Rafael", "Da Vinci", "Picasso"),
            correta=2,
        ),
        Pergunta(
            "Qual o maior planeta do Sistema Solar?",
            ("Terra", "Saturno", "Júpiter", "Netuno"),
            correta=2,
        ),
        Pergunta(
            "Em que ano o homem pisou na Lua pela primeira vez?",
            ("1965", "1969", "1972", "1959"),
            correta=1,
        ),
    )


def perguntas_padrao_rodada_2() -> tuple[Pergunta, ...]:
    return (
        Pergunta(
            "Quem escreveu 'Dom Casmurro'?",
            ("José de Alencar", "Machado de Assis", "Graciliano Ramos", "Clarice Lispector"),
            correta=1,
        ),
        Pergunta(
            "Qual é o maior oceano do mundo?",
            ("Atlântico", "Índico", "Ártico", "Pacífico"),
            correta=3,
        ),
        Pergunta(
            "Em que continente fica o Egito?",
            ("Ásia", "África", "Europa", "Oceania"),
            correta=1,
        ),
        Pergunta(
            "Quantos lados tem um hexágono?",
            ("5", "6", "7", "8"),
            correta=1,
        ),
        Pergunta(
            "Quem foi o primeiro presidente do Brasil?",
            ("Getúlio Vargas", "Dom Pedro II", "Deodoro da Fonseca", "Juscelino Kubitschek"),
            correta=2,
        ),
    )


def rodadas_padrao() -> list[Rodada]:
    return [
        Rodada(perguntas_padrao_rodada_1(), premio_por_acerto=PREMIO_RODADA_1),
        Rodada(perguntas_padrao_rodada_2(), premio_por_acerto=PREMIO_RODADA_2),
    ]


def main() -> None:
    # Windows costuma abrir stdout/stdin num codepage que não é UTF-8 (ex.: cp1252),
    # o que quebra os acentos do português; forçar UTF-8 evita mojibake no terminal.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    jogar(Partida(rodadas_padrao()))
