# showDoMilhao — instruções para o agente (AI-SMOS)

> Jogo do Milhão — CLI em Python (ADR-0002; ver `README.md` para as regras, fonte de domínio).
> A stack Java e o diagrama de classes anteriores foram descartados por decisão do responsável;
> só as regras do README permanecem vinculantes. AI-SMOS adotado via retrofit (ADR-0001).
> Walking Skeleton completo (DB→lógica→UI), jogável via `python -m showdomilhao` (`PYTHONPATH=src`):
> `Rodada` (5 perguntas + valor por acerto) encadeadas numa `Partida` contínua; Rodada 1 (R$1 mil),
> Rodada 2 (R$10 mil) e Rodada 3 (R$100 mil) implementadas. **Cada rodada é uma escada própria —
> não soma com a anterior** (bug corrigido: `_acertos_na_rodada` conta só acertos da rodada atual,
> zera ao cruzar de rodada; `pular()` avança a pergunta sem incrementar esse contador). Completar
> a Rodada 3 dá R$500 mil, igual ao "parar" da Pergunta do Milhão — confirma que é a mesma escada.
> Ajudas **Pulos** (até 3/partida) e **Cartas** (uso único, sorteio uniforme Ás/2/3/Rei —
> `sortear_carta`/`escolher_eliminados` injetáveis em `Partida` pra testes determinísticos)
> implementadas. **Pergunta do Milhão** implementada (`Partida(rodadas, pergunta_final=...)`,
> `partida.na_pergunta_final` público pro CLI bloquear ajudas lá): acertar dá R$1.000.000, errar
> ZERA (exceção à regra de metade), parar preserva o prêmio da última rodada. Jogo completo:
> 16 perguntas, todas as regras de valor implementadas — só faltam as ajudas Universitários/Placas
> (decisão de design pendente sobre simular opinião de terceiros). Regra de erro (metade do que já
> estava garantido, não zero, mesmo cruzando rodada) confirmada por evidência primária — ver
> README. Layout `src/showdomilhao/` (`partida.py` = domínio, `cli.py` = interação) + testes em
> `tests/`.

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

## Lições aprendidas
`docs/licoes-aprendidas.md` — observações sobre o próprio processo (não são ADRs). Ex.: o router
(S-02/S-03) define quando e como alargar uma fatia, não qual direção priorizar — isso é HITL.

## Precedência
Sandbox/permissões > hooks > regras por path > este arquivo > skill invocado > memória (S-01).
