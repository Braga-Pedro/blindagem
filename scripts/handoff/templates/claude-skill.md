---
name: handoff
description: >-
  Despacha o plano aprovado para o Cursor executar neste worktree e revisa o
  commit dele antes do PR. Use quando o usuário disser "/handoff", "manda pro
  Cursor", "despacha o plano", "revisa o que o Cursor fez", ou quando um plano
  acabou de ser aprovado e existe .handoff/plan.md com status ready.
---

# Handoff Claude ↔ Cursor

Fluxo de dois agentes no mesmo worktree: você planeja e revisa, o Cursor executa.
O contrato vive em `.handoff/` (`plan.md` → `exec.md` → `review.md`).

`/handoff` sozinho: se `.handoff/plan.md` está `ready` e não há `exec.md`, faça o
**dispatch**; se há `exec.md` com `status: done`, faça a **revisão**.

## Resolver o Orca CLI

Use o valor de `$ORCA_CLI_COMMAND` (o Orca exporta `orca-ide` nas sessões WSL). Nunca rode
`orca` puro no Linux — fora dos terminais do Orca isso é o leitor de tela do GNOME.
Confirme com `$ORCA_CLI_COMMAND status --json` antes da primeira chamada; se o app estiver
fora do ar, `$ORCA_CLI_COMMAND open --json`.

## Dispatch

1. Confira que `.handoff/plan.md` existe e está `status: ready`. Se não existir, o hook do
   plan mode não rodou — cheque `.handoff/.hook.log` antes de seguir.
2. Abra a aba do Cursor no worktree ativo (não crie worktree novo):

   ```
   $ORCA_CLI_COMMAND terminal create --worktree active --command "cursor-agent" --title "cursor · <slug>" --json
   ```

3. Guarde o handle retornado em `.handoff/.terminal` — a revisão vai devolver o trabalho por
   ele. Se um handle antigo estiver lá e retornar `terminal_handle_stale`, refaça com
   `terminal list --worktree active --json`.
4. `terminal wait --terminal <handle> --for tui-idle --timeout-ms 60000 --json` para não
   perder o input enquanto a TUI sobe.
5. `terminal send --terminal <handle> --text "/executar-plano" --enter --json`.
6. Marque o quadro (se houver): `worktree set --worktree active --comment "Cursor executando
   o plano" --workspace-status in-progress --json`.
7. Espere: `terminal wait --terminal <handle> --for tui-idle --timeout-ms 1200000 --json`.
   Se estourar o tempo, diga ao usuário onde está e pare — ele retoma com `/handoff review`.
8. Terminou: siga direto para a revisão.

O Cursor vai pedir aprovação de comandos (dependendo do `approvalMode` configurado). Isso é
do usuário aprovar na aba, não seu. Não passe `--force` sem ele pedir.

## Revisão

1. Leia `.handoff/plan.md` (front matter: `base_sha`) e `.handoff/exec.md` inteiro.
2. `git log --oneline <base_sha>..HEAD` e `git diff <base_sha>..HEAD`.
3. Rode a skill `code-review` sobre esse diff e valide com os comandos do bloco Ambiente do
   plano (tipicamente `./mvnw verify`).
4. **Confira aderência ao plano.** É isso que diferencia esta revisão de um code-review
   solto: passo a passo do plano, o que foi pedido × o que foi entregue. Escopo a mais conta
   como achado, tanto quanto escopo a menos.
5. Escreva `.handoff/review.md`:

   ```markdown
   ---
   status: approved | changes_requested
   reviewed_commit: <sha curto>
   ---

   ## Aderência ao plano
   Passo a passo: entregue, parcial ou fora do escopo.

   ## Achados
   1. `Arquivo.java:42` — o defeito, e o cenário concreto em que ele quebra.

   ## Validação
   `./mvnw verify`: o que rodou e o resultado.
   ```

   Achados são defeitos e desvios do plano. Preferência de estilo não é achado.
6. Se `changes_requested`: devolva ao mesmo terminal —
   `terminal send --terminal <handle> --text "Revisão pronta: leia .handoff/review.md e
   corrija os achados." --enter --json` — e espere `tui-idle` de novo. Itere até `approved`
   ou até o usuário mandar parar.
7. Se `approved`: siga para o PR.

## PR

Sem issue nem project board obrigatórios por enquanto (projeto ainda não tem esses
processos abertos no GitHub) — ajuste esta seção quando eles existirem.

1. `git push`.
2. Abra o PR com `gh pr create`, resumindo o plano executado e citando `.handoff/plan.md`
   / `.handoff/review.md` no corpo, seguindo o padrão de commit/PR já usado no repositório
   (Conventional Commits em português).
