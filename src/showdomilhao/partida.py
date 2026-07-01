import random
from dataclasses import dataclass

PREMIO_RODADA_1 = 1000
PREMIO_RODADA_2 = 10000
PREMIO_RODADA_3 = 100000
QUANTIDADE_PERGUNTAS_POR_RODADA = 5
QUANTIDADE_ALTERNATIVAS = 4
QUANTIDADE_MAXIMA_PULOS = 3

CARTAS = ("Ás", "2", "3", "Rei")
CARTAS_QUANTIDADE_A_ELIMINAR = {"Ás": 1, "2": 2, "3": 3, "Rei": 0}


def _sortear_carta_padrao() -> str:
    return random.choice(CARTAS)


def _escolher_eliminados_padrao(indices_errados: list[int], quantidade: int) -> list[int]:
    return random.sample(indices_errados, quantidade)


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

    def __init__(
        self,
        rodadas: list[Rodada],
        sortear_carta=_sortear_carta_padrao,
        escolher_eliminados=_escolher_eliminados_padrao,
    ):
        if not rodadas:
            raise ValueError("Partida exige ao menos 1 rodada.")
        self._rodadas = tuple(rodadas)  # cópia defensiva: imune a mutação externa da lista original
        self._indice_rodada = 0
        self._indice_pergunta = 0
        self.premio = 0
        self.finalizada = False
        self.pulos_restantes = QUANTIDADE_MAXIMA_PULOS
        self.cartas_usada = False
        self._sortear_carta = sortear_carta
        self._escolher_eliminados = escolher_eliminados

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

    def usar_cartas(self) -> tuple[str, tuple[int, ...]]:
        # Uso único por partida: o README não dá uma contagem explícita pra Cartas
        # (só Pulos tem "até 3 vezes"), tratado como single-use por inferência do
        # contraste textual — decisão de design registrada em docs/licoes-aprendidas.md.
        if self.finalizada:
            raise RuntimeError("Partida já finalizada.")
        if self.cartas_usada:
            raise RuntimeError("Ajuda Cartas já foi usada nesta partida.")

        pergunta = self.pergunta_atual()
        carta = self._sortear_carta()
        quantidade_a_eliminar = CARTAS_QUANTIDADE_A_ELIMINAR[carta]

        indices_errados = [i for i in range(len(pergunta.alternativas)) if i != pergunta.correta]
        eliminadas = tuple(self._escolher_eliminados(indices_errados, quantidade_a_eliminar))

        self.cartas_usada = True
        return carta, eliminadas
