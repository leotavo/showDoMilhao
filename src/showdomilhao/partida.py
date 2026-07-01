from dataclasses import dataclass

PREMIO_RODADA_1 = 1000
PREMIO_RODADA_2 = 10000
QUANTIDADE_PERGUNTAS_POR_RODADA = 5
QUANTIDADE_ALTERNATIVAS = 4
QUANTIDADE_MAXIMA_PULOS = 3


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


@dataclass(frozen=True)
class Rodada:
    perguntas: tuple[Pergunta, ...]
    premio_por_acerto: int

    def __post_init__(self):
        if len(self.perguntas) != QUANTIDADE_PERGUNTAS_POR_RODADA:
            raise ValueError(
                f"Rodada exige {QUANTIDADE_PERGUNTAS_POR_RODADA} perguntas, "
                f"recebeu {len(self.perguntas)}."
            )
        if self.premio_por_acerto <= 0:
            raise ValueError(
                f"premio_por_acerto deve ser positivo, recebeu {self.premio_por_acerto}."
            )


class Partida:
    """Walking skeleton: rodadas encadeadas numa única partida contínua (ADR-0002)."""

    def __init__(self, rodadas: list[Rodada]):
        if not rodadas:
            raise ValueError("Partida exige ao menos 1 rodada.")
        self._rodadas = tuple(rodadas)  # cópia defensiva: imune a mutação externa da lista original
        self._indice_rodada = 0
        self._indice_pergunta = 0
        self.premio = 0
        self.finalizada = False
        self.pulos_restantes = QUANTIDADE_MAXIMA_PULOS

    def _rodada_atual(self) -> Rodada:
        return self._rodadas[self._indice_rodada]

    def _avancar_pergunta(self) -> None:
        rodada = self._rodada_atual()
        self._indice_pergunta += 1
        if self._indice_pergunta == len(rodada.perguntas):
            self._indice_pergunta = 0
            self._indice_rodada += 1
            if self._indice_rodada == len(self._rodadas):
                self.finalizada = True

    def pergunta_atual(self) -> Pergunta:
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")
        return self._rodada_atual().perguntas[self._indice_pergunta]

    def responder(self, indice_alternativa: int) -> bool:
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")

        rodada = self._rodada_atual()
        pergunta = self.pergunta_atual()
        if not 0 <= indice_alternativa < len(pergunta.alternativas):
            raise ValueError(
                f"indice_alternativa={indice_alternativa} fora do intervalo válido "
                f"(0..{len(pergunta.alternativas) - 1})."
            )

        acertou = indice_alternativa == pergunta.correta
        if acertou:
            self.premio += rodada.premio_por_acerto
            self._avancar_pergunta()
        else:
            # Errar não zera: cai pra metade do que já estava garantido (PARAR).
            # Regra atravessa a fronteira entre rodadas (confirmado pelo responsável
            # do projeto). Confirmado por evidência primária dentro de uma rodada
            # (captura de tela do programa real, 4 pontos de dado consistentes):
            # https://www.youtube.com/watch?v=tPJD9Qo4EN8
            self.premio = self.premio // 2
            self.finalizada = True

        return acertou

    def parar(self) -> None:
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")
        self.finalizada = True

    def pular(self) -> None:
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")
        if self.pulos_restantes <= 0:
            raise RuntimeError("Sem pulos restantes.")

        self.pulos_restantes -= 1
        self._avancar_pergunta()
