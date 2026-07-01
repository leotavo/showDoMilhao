# showDoMilhao — instruções para o agente (AI-SMOS)

> Jogo do Milhão — CLI em Python (ADR-0002; ver `README.md` para as regras, fonte de domínio).
> A stack Java e o diagrama de classes anteriores foram descartados por decisão do responsável;
> só as regras do README permanecem vinculantes. AI-SMOS adotado via retrofit (ADR-0001).
> Nenhum código ainda existe — comandos de lint/test/build ficam `TODO` até o Walking Skeleton
> (new-feature playbook) escolher e instalar o ferramental real, para não afirmar capacidade
> inexistente (S-05).

## Como trabalhar aqui (resumo)
- **Classifique antes de agir** (S-02) e roteie (S-03). Tarefa trivial → execução expressa, sem cerimônia.
- **Evidência > prosa** (S-00): toda mudança de comportamento traz teste/aceitação.
- **Risco/HITL** (S-04/S-06): tocar `.env`/`.github`/segredos/produção → pare e peça aprovação.
- **Decisão de arquitetura** → MCDA → ADR (`docs/decisions/`) → HITL.
- **Anti-alucinação** (S-05): não afirme capacidade de ferramenta sem fonte.

## Comandos do projeto
- Lint: `TODO — definir ao escolher stack`
- Teste: `TODO — definir ao escolher stack`
- Build: `TODO — definir ao escolher stack`

## Playbooks (invocar por classe)
new-feature · bugfix · refactor · research · architecture-decision · code-review

## Precedência
Sandbox/permissões > hooks > regras por path > este arquivo > skill invocado > memória (S-01).
