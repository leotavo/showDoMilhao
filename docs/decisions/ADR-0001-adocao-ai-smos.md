# ADR-0001 — Adoção do AI-SMOS como metodologia operacional

- **Data:** 2026-07-01
- **Status:** Aceito
- **Responsável:** leotavo
- **Confiança:** Alta (S-05) — decisão de processo, não de domínio; ancorada na doutrina do próprio plugin.
- **Rastreabilidade:** n/a

## Contexto
`showDoMilhao` é um repositório **existente** (Jogo do Milhão em Java) com histórico prévio
(`README.md` com regras e diagrama de classes, `.gitignore`), mas sem código-fonte, sem
instruções de agente e sem registro de decisões. Este ADR é um **retrofit**: adota o AI-SMOS
(S-00..S-06) como framework operacional a partir de agora, sem reescrever o histórico existente.

> Nota de correção: uma primeira tentativa de bootstrap tratou este diretório como projeto novo
> (a cópia local ainda não tinha sido sincronizada com o remoto) e criou um histórico local
> desconectado. Corrigido ao sincronizar com `origin/main` antes de qualquer push — nenhum dado
> do repositório real foi perdido ou sobrescrito.

## Opções consideradas
- **Opção A — Adotar AI-SMOS:** doutrina pronta (task routing, risk gates, ADRs, evidence policy),
  plugin já instalado e ativo no ambiente. Overhead mínimo para um projeto novo.
- **Opção B — Sem metodologia formal:** decisões e riscos tratados ad-hoc. Menor cerimônia inicial,
  mas sem rastreabilidade nem gate de risco para ações sensíveis (segredos, CI, produção).

## MCDA
Não aplicável — apenas uma opção viável no momento (uso do plugin já instalado), sem necessidade de
tabela ponderada.

## Decisão
Adotar o AI-SMOS (Opção A). O projeto usa `CLAUDE.md` para instruções de agente,
`docs/decisions/` para ADRs, e o risk-gate do plugin (`PreToolUse` em Write/Edit/MultiEdit/Bash)
para bloquear ações sensíveis sem aprovação humana. O breaker de cota/circuit-breaker já é
fornecido pelo plugin H1-A, também instalado neste ambiente — não duplicado aqui.

## Consequências
- Toda decisão de arquitetura futura (build tool, camadas, persistência) passa por ADR — inclusive
  a escolha entre Maven/Gradle para o projeto Java, ainda pendente.
- Tarefas triviais seguem execução expressa (S-02/S-03); apenas decisões de risco elevado exigem HITL.
- Lint/test/build em `CLAUDE.md` ficam como `TODO` até a stack de build ser escolhida — não
  fabricados aqui (README já define regras de domínio, mas não ferramental).
- O histórico de commits anterior a este ADR (`8fd04a6`..`af1340c`) permanece intacto e não é
  retroativamente sujeito aos gates do AI-SMOS.

## HITL
- Aprovação necessária? Não — decisão de processo, sem impacto em segredos/produção/CI.
