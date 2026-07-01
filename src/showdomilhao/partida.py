from dataclasses import dataclass

PREMIO_POR_ACERTO_RODADA_1 = 1000
QUANTIDADE_PERGUNTAS_RODADA_1 = 5
QUANTIDADE_ALTERNATIVAS = 4


@dataclass(frozen=True)
class Pergunta:
    enunciado: str
    alternativas: tuple[str, ...]
    correta: int

    def __post_init__(self):
        if len(self.alternativas) != QUANTIDADE_ALTERNATIVAS:
            raise ValueError(
                f"Pergunta deve ter {QUANTIDADE_ALTERNATIVAS} alternativas, "
                f"recebeu {len(self.alternativas)}."
            )
        if not 0 <= self.correta < len(self.alternativas):
            raise ValueError(
                f"correta={self.correta} fora do intervalo válido "
                f"(0..{len(self.alternativas) - 1})."
            )


class Partida:
    """Walking skeleton: cobre só a Rodada 1 (ADR-0002, appetite pequeno)."""

    def __init__(self, perguntas: list[Pergunta]):
        if len(perguntas) != QUANTIDADE_PERGUNTAS_RODADA_1:
            raise ValueError(
                f"Rodada 1 exige {QUANTIDADE_PERGUNTAS_RODADA_1} perguntas, "
                f"recebeu {len(perguntas)}."
            )
        self._perguntas = tuple(perguntas)  # cópia defensiva: imune a mutação externa da lista original
        self._indice_atual = 0
        self.premio = 0
        self.finalizada = False

    def pergunta_atual(self) -> Pergunta:
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")
        return self._perguntas[self._indice_atual]

    def responder(self, indice_alternativa: int) -> bool:
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")

        pergunta = self.pergunta_atual()
        if not 0 <= indice_alternativa < len(pergunta.alternativas):
            raise ValueError(
                f"indice_alternativa={indice_alternativa} fora do intervalo válido "
                f"(0..{len(pergunta.alternativas) - 1})."
            )

        acertou = indice_alternativa == pergunta.correta
        if acertou:
            self.premio += PREMIO_POR_ACERTO_RODADA_1
            self._indice_atual += 1
            if self._indice_atual == len(self._perguntas):
                self.finalizada = True
        else:
            # Errar não zera: cai pra metade do que já estava garantido (PARAR).
            # Confirmado por evidência primária (captura de tela do programa real,
            # 4 pontos de dado consistentes): https://www.youtube.com/watch?v=tPJD9Qo4EN8
            self.premio = self.premio // 2
            self.finalizada = True

        return acertou

    def parar(self) -> None:
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")
        self.finalizada = True
