# showDoMilhao

Jogo do Milhão — implementação em Python. A stack original (Java) e o diagrama de classes que
acompanhava este README foram descartados; ver [ADR-0002](docs/decisions/ADR-0002-escolha-de-plataforma.md).

## Status do projeto

Metodologia [AI-SMOS](CLAUDE.md) adotada via retrofit ([ADR-0001](docs/decisions/ADR-0001-adocao-ai-smos.md)).
Em andamento: Walking Skeleton ([ADR-0002](docs/decisions/ADR-0002-escolha-de-plataforma.md)),
alargando rodada por rodada (appetite pequeno a cada fatia, HITL antes de alargar).

- [x] Lógica de domínio (`src/showdomilhao/partida.py`) — `Rodada` (5 perguntas + valor por
  acerto) encadeadas numa `Partida` contínua; errar reduz o prêmio pela metade (não zera, mesmo
  cruzando de rodada) e encerra; parar preserva o prêmio e encerra.
- [x] Rodada 1 (R$ 1 mil/acerto) e Rodada 2 (R$ 10 mil/acerto) implementadas e encadeadas.
- [x] Testes cobrindo os desfechos, a transição entre rodadas e casos de uso indevido
  (`tests/test_partida.py`).
- [x] Interface de linha de comando (`src/showdomilhao/cli.py`) — Rodada 1 + Rodada 2 jogáveis de
  ponta a ponta pelo terminal, com testes (`tests/test_cli.py`) via injeção de entrada/saída.
- [x] Ajuda **Pulos** — até 3 por partida, pula a pergunta atual sem ganhar nem perder prêmio.
- [ ] Rodada 3 e Pergunta do Milhão.
- [ ] Ajudas **Universitários**, **Placas** e **Cartas** — adiadas: dependem de uma mecânica de
  aleatoriedade (como simular a resposta de terceiros) que o README não especifica; decisão de
  design ainda pendente (ver `docs/licoes-aprendidas.md`).

Rodar o jogo: `PYTHONPATH=src python -m showdomilhao`
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

> Confirmado por evidência primária (captura de tela do programa,
> [vídeo](https://www.youtube.com/watch?v=tPJD9Qo4EN8), 4 quadros consistentes): em cada pergunta,
> o valor de "errar" é sempre metade do valor de "parar" daquele momento (ex.: parar = R$ 2 mil →
> errar = R$ 1 mil). Confirmado pelo responsável do projeto que essa regra vale também ao cruzar
> de uma rodada pra outra (ex.: errar a 1ª pergunta da Rodada 2 com R$ 5 mil garantidos cairia pra
> R$ 2.500) — exceto na Pergunta do Milhão, cuja exceção já está descrita acima (errar zera).

### Ajudas (lifelines) disponíveis ao longo do jogo

Universitários: três estudantes dão suas respostas; o participante decide se segue ou não. 

Placas: convidados na plateia levantam placas (1–4) indicando a alternativa; conta-se o “voto” mais frequente. 

Cartas: o participante vira uma carta; Ás elimina 1 errada, 2 elimina 2, 3 elimina 3 (resta a correta), Rei não elimina nenhuma. 

Pulos: pode pular a pergunta (até 3 vezes por partida). 

Nenhuma ajuda pode ser usada na Pergunta do Milhão. Nessa hora, o participante escolhe: responder (e arriscar tudo) ou parar e levar R$ 500 mil. Erro na final zera o prêmio. 
