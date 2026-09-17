---
name: executar-plano
description: >-
  Executa o plano que o Claude deixou em .handoff/plan.md neste worktree e
  relata o resultado em .handoff/exec.md. Use quando o usuário pedir "executar
  o plano", "/executar-plano", "seguir o handoff", ou quando existir um
  .handoff/plan.md com status ready ou um .handoff/review.md com status
  changes_requested.
---

# Executar o plano do Claude

Você é o executor de um fluxo de dois agentes: o Claude planeja e revisa, você implementa.
O contrato está em `.handoff/plan.md`.

## 1. Ler o contrato

Leia `.handoff/plan.md` inteiro antes de tocar em qualquer arquivo. Ele traz:

- o **front matter** com `issue` (se houver), `branch` e `base_sha`;
- o bloco **Ambiente**, com os comandos que funcionam neste worktree;
- o **Plano** aprovado.

Se `.handoff/review.md` existir com `status: changes_requested`, vá para a seção
"Rodada de correção" no fim deste arquivo.

## 2. Executar

Implemente o plano na ordem em que está escrito. As regras:

- **Não replaneje.** Se um passo estiver errado ou impossível, implemente todo o resto e
  registre a divergência em `.handoff/exec.md` — não invente uma solução alternativa de
  escopo maior.
- **Não amplie o escopo.** Nada de refatoração oportunista, documentação não pedida,
  changelog ou passe de formatação em arquivo que o plano não menciona.
- Siga `AGENTS.md` para convenções de código (Java 21, Spring Boot 4, pacotes sob
  `io.github.bragapedro.blindagem`, sem comentários que só repetem o que o código já diz).
- Comentários: só quando o *porquê* não estiver visível no código. O racional da mudança
  vai no PR, não no fonte.

## 3. Validar

Use **os comandos do bloco Ambiente do plano**.

Rode, nesta ordem, antes de commitar:

1. `./mvnw compile` — garante que compila.
2. `./mvnw verify` — testes, incluindo integração via Testcontainers.

Toda mudança de comportamento precisa de teste: crie um novo ou atualize um existente. Se
algum comando falhar e você não conseguir resolver dentro do escopo do plano, pare e
registre em `exec.md` — não commite vermelho.

## 4. Commitar

Um commit, mensagem no padrão Conventional Commits em português, igual ao histórico do
repositório (`feat: ...`, `fix: ...`, `chore: ...`). **Sem `git push`** — quem abre o PR é
o Claude, depois da revisão.

## 5. Relatar

Escreva `.handoff/exec.md`:

```markdown
---
status: done
commit: <sha curto>
---

## O que foi feito
Um parágrafo por passo do plano, dizendo onde encostou.

## Divergências
Passos que você não seguiu à risca e por quê. "Nenhuma" se for o caso.

## Validação
Os comandos que você rodou e o resultado de cada um.

## Dúvidas
O que precisa de decisão humana. "Nenhuma" se for o caso.
```

Seja honesto: se um teste ficou de fora ou um passo ficou incompleto, diga. O Claude vai
revisar o diff contra o plano e a divergência aparece de qualquer jeito.

## Rodada de correção

Quando `.handoff/review.md` tiver `status: changes_requested`:

1. Leia os achados numerados.
2. Corrija todos, revalidando como na etapa 3.
3. Commite por cima (novo commit, não `--amend`).
4. **Acrescente** uma seção `## Rodada N` no fim de `.handoff/exec.md` — respondendo achado
   por achado, inclusive os que você discorda e por quê — e volte o `status` do front matter
   para `done`.
