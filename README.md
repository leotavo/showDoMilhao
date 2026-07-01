# showDoMilhao

Jogo do Milhão — implementação em Python. A stack original (Java) e o diagrama de classes que
acompanhava este README foram descartados; ver [ADR-0002](docs/decisions/ADR-0002-escolha-de-plataforma.md).

## Status do projeto

Metodologia [AI-SMOS](CLAUDE.md) adotada via retrofit ([ADR-0001](docs/decisions/ADR-0001-adocao-ai-smos.md)).
Em andamento: Walking Skeleton da Rodada 1 ([ADR-0002](docs/decisions/ADR-0002-escolha-de-plataforma.md), appetite pequeno).

- [x] Lógica de domínio da Rodada 1 (`src/showdomilhao/partida.py`) — 5 perguntas, prêmio
  cumulativo de R$ 1 mil por acerto, encerramento por erro ou por parar.
- [x] Testes cobrindo os três desfechos e casos de uso indevido (`tests/test_partida.py`).
- [ ] Interface de linha de comando (a lógica ainda não é jogável — só testada).
- [ ] Rodada 2, Rodada 3 e Pergunta do Milhão.
- [ ] As 4 ajudas (Universitários, Placas, Cartas, Pulos).
- [ ] Tabela de segurança (valores de "parar"/"errar" por nível intermediário — o texto abaixo só
  especifica o valor final; os intermediários são uma lacuna de regra ainda não esclarecida).

Rodar os testes: `python -m pytest`
Rodar o lint: `python -m ruff check .`

## Regras

### Formato e perguntas

Jogo dividido em 3 rodadas de 5 perguntas cada, seguidas de 1 pergunta final (“a do milhão”) — total de 16 perguntas.

Cada pergunta tem 4 alternativas e apenas 1 correta. 

### Valores e progressão

Rodada 1: cada acerto soma R$ 1 mil (cumulativo).

Rodada 2: cada acerto soma R$ 10 mil (cumulativo).

Rodada 3: cada acerto soma R$ 100 mil (cumulativo).

Pergunta do Milhão: vale R$ 1.000.000. Há tabela de “parar” e “errar” em cada nível; na final, parar = R$ 500 mil e errar = R$ 0. 

### Ajudas (lifelines) disponíveis ao longo do jogo

Universitários: três estudantes dão suas respostas; o participante decide se segue ou não. 

Placas: convidados na plateia levantam placas (1–4) indicando a alternativa; conta-se o “voto” mais frequente. 

Cartas: o participante vira uma carta; Ás elimina 1 errada, 2 elimina 2, 3 elimina 3 (resta a correta), Rei não elimina nenhuma. 

Pulos: pode pular a pergunta (até 3 vezes por partida). 

Nenhuma ajuda pode ser usada na Pergunta do Milhão. Nessa hora, o participante escolhe: responder (e arriscar tudo) ou parar e levar R$ 500 mil. Erro na final zera o prêmio. 
