# showDoMilhao
Jogo do Milhão em Java

## Regras

### Formato e perguntas

Jogo dividido em 3 rodadas de 5 perguntas cada, seguidas de 1 pergunta final (“a do milhão”) — total de 16 perguntas.

Cada pergunta tem 4 alternativas e apenas 1 correta. 
Wikipédia

### Valores e progressão

Rodada 1: cada acerto soma R$ 1 mil (cumulativo).

Rodada 2: cada acerto soma R$ 10 mil (cumulativo).

Rodada 3: cada acerto soma R$ 100 mil (cumulativo).

Pergunta do Milhão: vale R$ 1.000.000. Há tabela de “parar” e “errar” em cada nível; na final, parar = R$ 500 mil e errar = R$ 0. 
Wikipédia

### Ajudas (lifelines) disponíveis ao longo do jogo

Universitários: três estudantes dão suas respostas; o participante decide se segue ou não. 
Wikipédia

Placas: convidados na plateia levantam placas (1–4) indicando a alternativa; conta-se o “voto” mais frequente. 
Wikipédia

Cartas: o participante vira uma carta; Ás elimina 1 errada, 2 elimina 2, 3 elimina 3 (resta a correta), Rei não elimina nenhuma. 
Wikipédia

Pulos: pode pular a pergunta (até 3 vezes por partida). 
Wikipédia

Nenhuma ajuda pode ser usada na Pergunta do Milhão. Nessa hora, o participante escolhe: responder (e arriscar tudo) ou parar e levar R$ 500 mil. Erro na final zera o prêmio. 

### Restrições importantes

## Diagrama de Classes

```mermaid
classDiagram
direction LR

class Partida {
  - estado: EstadoPartida
  - fase: Fase
  - perguntas: List~Pergunta~
  - indiceAtual: int
  - ajudas: Map~TipoAjuda,Ajuda~
  - pulosRestantes: int
  - usados: Set~UUID~
  - escada: EscadaPremios
  + iniciar(): void
  + responder(indice:int): boolean
  + usarAjuda(tipo:TipoAjuda): boolean
  + pular(): boolean
  + parar(): void
  + avancar(): void
  + saldoAtual(): BigDecimal
  + emFinal(): boolean
  + getPerguntaAtual(): Pergunta
}

class Jogador {
  - nome: String
  + getNome(): String
}

class Pergunta {
  - id: UUID
  - enunciado: String
  - alternativas: List~Alternativa~
  - fase: Fase
}

class Alternativa {
  - texto: String
  - correta: boolean
}

class EscadaPremios {
  - degraus: List~BigDecimal~
  + premioNa(indice:int): BigDecimal
  + valorPararFinal(): BigDecimal
  + valorErroFinal(): BigDecimal
}

class Ajuda {
  <<interface>>
  + tipo(): TipoAjuda
  + aplicar(p:Pergunta, visiveis:List~Alternativa~): List~Alternativa~
  + disponivel(): boolean
  + consumir(): void
}

class Universitarios
class Placas
class Cartas
class Pulo

Ajuda <|.. Universitarios
Ajuda <|.. Placas
Ajuda <|.. Cartas
Ajuda <|.. Pulo

class BancoPerguntas {
  <<interface>>
  + sortear(fase:Fase, usados:Set~UUID~): Pergunta
}

Partida "1" --> "1" Jogador
Partida "1" --> "1" EscadaPremios
Partida "1" --> "1" BancoPerguntas
Partida "1" o-- "*" Ajuda : usa
Partida "1" --> "0..*" Pergunta : selecionadas
Pergunta "1" *-- "4" Alternativa : compõe

class EstadoPartida {
  <<enumeration>>
  PRONTO
  PERGUNTANDO
  CHECANDO
  FINAL
}

class Fase {
  <<enumeration>>
  RODADA1
  RODADA2
  RODADA3
  FINAL
}

class TipoAjuda {
  <<enumeration>>
  UNIVERSITARIOS
  PLACAS
  CARTAS
  PULO
}

note for Pergunta "4 alternativas; 1 correta."
note for Partida "Sem ajuda na pergunta final."
