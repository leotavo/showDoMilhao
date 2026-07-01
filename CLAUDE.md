# showDoMilhao — instruções para o agente (AI-SMOS)

> Jogo do Milhão — CLI em Python (ADR-0002; ver `README.md` para as regras, fonte de domínio).
> A stack Java e o diagrama de classes anteriores foram descartados por decisão do responsável;
> só as regras do README permanecem vinculantes. AI-SMOS adotado via retrofit (ADR-0001).
> Walking Skeleton completo (DB→lógica→UI), jogável via `python -m showdomilhao` (`PYTHONPATH=src`):
> `Rodada` (5 perguntas + valor por acerto) encadeadas numa `Partida` contínua; Rodada 1 (R$1 mil)
> e Rodada 2 (R$10 mil) implementadas, Rodada 3/final e ajudas ainda não. Regra de erro (metade do
> prêmio, não zero, mesmo cruzando rodada) confirmada por evidência primária — ver README. Layout
> `src/showdomilhao/` (`partida.py` = domínio, `cli.py` = interação) + testes em `tests/`.

## Como trabalhar aqui (resumo)
- **Classifique antes de agir** (S-02) e roteie (S-03). Tarefa trivial → execução expressa, sem cerimônia.
- **Evidência > prosa** (S-00): toda mudança de comportamento traz teste/aceitação.
- **Risco/HITL** (S-04/S-06): tocar `.env`/`.github`/segredos/produção → pare e peça aprovação.
- **Decisão de arquitetura** → MCDA → ADR (`docs/decisions/`) → HITL.
- **Anti-alucinação** (S-05): não afirme capacidade de ferramenta sem fonte.

## Comandos do projeto
- Lint: `python -m ruff check .`
- Teste: `python -m pytest`
- Rodar: `PYTHONPATH=src python -m showdomilhao`
- Build: n/a — ainda não há empacotamento/distribuição; revisitar quando existir.

## Playbooks (invocar por classe)
new-feature · bugfix · refactor · research · architecture-decision · code-review

## Precedência
Sandbox/permissões > hooks > regras por path > este arquivo > skill invocado > memória (S-01).
