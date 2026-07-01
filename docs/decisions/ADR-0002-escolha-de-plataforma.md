# ADR-0002 — Escolha de plataforma/stack (abandono do Java + diagrama anterior)

- **Data:** 2026-07-01
- **Status:** Aceito
- **Responsável:** leotavo
- **Confiança:** Média (S-05) — MCDA com pesos definidos por mim na ausência de critérios explícitos
  do responsável; pesos e notas são candidatos a ajuste, não fato consolidado.
- **Rastreabilidade:** n/a

## Contexto
A decisão original (Java, ver diagrama de classes em `README.md`) foi descartada por instrução
direta do responsável: *"ignore a stack escolhida Java e o diagrama. se inspire nas regras"*.
Ou seja, o **domínio** (rodadas, prêmios, ajudas, pergunta do milhão — texto de `README.md`)
continua sendo a fonte da verdade; a **implementação anterior** (Java + diagrama de classes) não é
mais vinculante.

Isso reabre a decisão de arquitetura: qual plataforma/stack usar para reconstruir o jogo. Como há
2+ opções técnicas centrais, o gate S-04 exige MCDA + ADR + HITL obrigatório antes de qualquer
código — nenhuma linha de implementação foi escrita para este ADR.

## Opções consideradas
- **Opção A — CLI (Python):** jogo textual no terminal. Setup mínimo, lógica de jogo isolada e
  fácil de testar (`pytest`), mas sem fidelidade visual ao "programa de TV".
- **Opção B — Web app client-side (TypeScript/JS puro, sem backend):** lógica e UI rodando
  inteiramente no navegador, deploy estático (ex.: GitHub Pages). Visual mais fiel ao formato
  (placas, cartas, prêmio subindo), compartilhável via link, mas testes de UI têm custo maior que
  testes de lógica pura.
- **Opção C — Web app full-stack (Node/TypeScript backend + frontend):** separa lógica de jogo
  (servidor, fonte única da verdade sobre respostas corretas) da UI. Mais fiel a um "jogo real"
  (evita trapaça client-side), mas dobra a superfície de manutenção para um projeto solo.

## MCDA
Critérios ponderados (0–10 por opção), pesos refletem prioridades de um **projeto pessoal solo**
sob AI-SMOS (walking skeleton rápido, test-first, baixo overhead de manutenção):

| Critério | Peso | A — CLI Python | B — Web client-only | C — Web full-stack |
|---|---:|---:|---:|---:|
| Velocidade do Walking Skeleton | 9 | 10 (90) | 7 (63) | 5 (45) |
| Fidelidade ao formato do programa | 7 | 4 (28) | 9 (63) | 9 (63) |
| Testabilidade (test-first, S-02) | 8 | 10 (80) | 7 (56) | 8 (64) |
| Manutenção solo (baixo overhead) | 8 | 9 (72) | 7 (56) | 5 (40) |
| Compartilhável (jogar sem setup local) | 5 | 3 (15) | 9 (45) | 8 (40) |
| **Score ponderado** | | **285** | **283** | **252** |

A e B ficam praticamente empatadas (285 vs. 283) — a diferença real entre elas é uma troca
consciente: **A** prioriza velocidade de prototipagem e testabilidade pura; **B** prioriza
fidelidade visual e compartilhamento, ao custo de testes de UI mais caros. **C** perde em ambos os
eixos que mais pesam para um projeto solo (velocidade e manutenção).

## Decisão
**Opção A — CLI (Python)**, aprovada por HITL. Prova as regras (rodadas, prêmios, ajudas) ponta a
ponta com testes rápidos; UI visual fica para uma iteração futura (possível ADR-0003), sem
necessidade de reescrever as regras de domínio ao migrar de camada de apresentação.

## Consequências
- Se A: primeira fatia do walking skeleton é textual; UI visual fica para uma iteração futura
  (possível ADR-0003 se/quando migrar para B).
- Se B: primeira fatia já inclui alguma UI mínima; testes de lógica ficam em módulo isolado
  (testável sem DOM) desde o início, para não acoplar regras à interface.
- Se C: adiado — nenhuma vantagem clara para escopo solo neste momento; pode ser revisitado se
  o jogo precisar impedir trapaça (ex.: uso competitivo/multiplayer).
- Em qualquer opção: `CLAUDE.md` é atualizado com os comandos reais de lint/test/build assim que
  a stack for aprovada.

## HITL
- Aprovação necessária? **Sim** — decisão de arquitetura (S-04/S-06), sempre HITL obrigatório.
- Aprovado por: leotavo (2026-07-01, via chat)
