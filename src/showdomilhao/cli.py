import sys

from showdomilhao.partida import Partida, Pergunta


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
            texto = entrada("Responda (A-D) ou digite 'parar': ")
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

        acertou = partida.responder(comando)
        saida(formatar_resultado(acertou, partida.premio))

    saida(f"Fim de jogo. Prêmio final: R$ {partida.premio}")


def perguntas_padrao_rodada_1() -> list[Pergunta]:
    return [
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
    ]


def main() -> None:
    # Windows costuma abrir stdout/stdin num codepage que não é UTF-8 (ex.: cp1252),
    # o que quebra os acentos do português; forçar UTF-8 evita mojibake no terminal.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    jogar(Partida(perguntas_padrao_rodada_1()))
