# Lições aprendidas (processo/metodologia)

Log de observações sobre como o AI-SMOS se comportou na prática neste projeto — não são ADRs
(não são decisões de arquitetura), são ajustes de expectativa sobre o próprio processo.

## 2026-07-01 — A metodologia não sugere a próxima iteração, só o processo pra alargar

**Observação:** depois de fechar a fatia da Rodada 2 e confirmar a Definition of Done (todos os
itens batendo), a pergunta natural "o que fazer agora?" esbarrou num limite do S-03/playbook
`new-feature`: o router define *quando* alargar (HITL antes de alargar, uma etapa por vez) e
*como* (appetite → test-first → DoD), mas não tem heurística nenhuma pra decidir **qual** direção
alargar quando há mais de uma aberta (Rodada 3, ajudas, Pergunta do Milhão). Os eixos de
classificação do S-02 (tipo/escopo/reversibilidade/risco) classificam uma tarefa uma vez que a
forma dela já é conhecida — não ranqueiam alternativas de escopo/produto ainda não escolhidas.

**Por quê isso importa:** sem esse registro, cada vez que uma fatia fecha, o agente (ou uma
pessoa nova lendo o histórico) pode achar que "a metodologia travou" ou que falta alguma etapa —
quando na verdade é um limite esperado: decisão de prioridade de produto é HITL por natureza,
não é algo que um router de processo deveria resolver sozinho.

**Como aplicar daqui pra frente:** ao chegar nesse ponto, nomear explicitamente que é uma decisão
de prioridade fora do escopo do router (não um processo quebrado ou incompleto), e ainda assim
propor uma recomendação por algum critério disponível (ex.: Shape Up — "alargar uma dimensão por
vez", preferir reaproveitar um padrão já provado antes de atacar algo estruturalmente diferente).
Evitar devolver a decisão em aberto sem nenhuma âncora.
