# Índice de Decisões (ADRs)

| ADR | Título | Status | Data |
|---|---|---|---|
| [ADR-0001](ADR-0001-adocao-ai-smos.md) | Adoção do AI-SMOS como metodologia operacional (retrofit) | Aceito | 2026-07-01 |
| [ADR-0002](ADR-0002-escolha-de-plataforma.md) | Escolha de plataforma/stack (abandono do Java + diagrama) | Aceito | 2026-07-01 |

## Origem → S-0x (retrofit)

Mapeamento de artefatos pré-existentes no repositório (antes do AI-SMOS) para a doutrina que
passam a seguir a partir de agora:

| Origem (pré-AI-SMOS) | Mapeado para |
|---|---|
| `README.md` (regras do jogo, diagrama de classes) | Fonte de domínio — decisões de arquitetura que a implementem exigem ADR (S-04, gate "Decisão de arquitetura") |
| Histórico de commits `8fd04a6`..`af1340c` | Preservado como está; não retroagimos gates (S-04) sobre ele |
| Nenhum CLAUDE.md/AGENTS.md prévio | Criado agora (S-01, precedência de instruções) |
| Nenhum ADR prévio | Índice iniciado neste retrofit (S-04/S-05) |
