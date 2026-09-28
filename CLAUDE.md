# Blindagem

Assistente que gera um plano de ação priorizado e verificável para pessoas expostas por vazamento de dados pessoais ou golpe de voz clonada — sem nunca pedir ou armazenar o CPF de quem usa.

Projeto de extensão universitária, em fase inicial de desenvolvimento (esqueleto criado, domínio e corpus de fontes oficiais em produção paralela).

## O problema que o projeto resolve

Ferramentas existentes dizem que os dados de alguém vazaram, mas nenhuma diz o que fazer, em que ordem, nem como verificar que cada passo foi concluído. O golpe de voz clonada de um familiar não tem nenhuma ferramenta de resposta — só alertas genéricos ("combine uma palavra-código") sem ensinar a implantar isso na prática.

O Blindagem cobre as duas superfícies: exposição de **dados** (o que se sabe sobre a vítima) e exposição de **voz** (o que se consegue imitar dela).

## Limites explícitos do escopo — nunca violar

- **Não** é um verificador de vazamento: não construir nem persistir base de CPFs ou credenciais.
- **Não** é um detector de deepfake: não implementar identificação de áudio sintético.
- **Não** sintetizar, clonar ou reproduzir voz, em nenhuma hipótese — nem para fins de teste/demo.
- **Não** é um agregador de links: cada passo de um plano gerado deve ser verificável, não apenas uma sugestão de pesquisa.
- **Nunca** pedir ou armazenar CPF do usuário. Se uma feature parecer exigir isso, é sinal de que o desenho está errado — parar e perguntar antes de implementar.

## Stack

- **Java 21** + **Spring Boot 4.1.1**
- **PostgreSQL**, com **pgvector** planejado para busca sobre o corpus oficial (ainda não implementado)
- **Docker Compose** para o ambiente local (subido automaticamente via `spring-boot-docker-compose`)
- **Testcontainers** para testes de integração contra banco real (sem necessidade de banco rodando à parte)
- **Maven** (wrapper `./mvnw`) como build tool

## Estrutura de pacotes

```
io.github.bragapedro.blindagem
```

`groupId` no Maven segue a mesma convenção (domínio reverso baseado no usuário GitHub, já que não há domínio próprio registrado).

## Arquitetura e convenções de código

Convenções a seguir a partir do primeiro controller/service/entidade — ainda não há código de
domínio no repositório para validar contra elas, mas ficam fixadas aqui antes desse código
aparecer para não ter que corrigir padrão depois.

- **Pacote por feature**, não por camada técnica: `plano/`, `exposicaodados/`,
  `exposicaovoz/`, `corpus/` (dentro do pacote base), cada um com seu próprio
  controller/service/repository internos.
- **Injeção de dependência por construtor**, nunca `@Autowired` em campo.
- **DTOs como `record`** (Java 21); nunca expor `@Entity` do JPA direto no controller.
- **`@Transactional` só na camada de service**, nunca em controller ou repository.
- **Bean Validation** (`spring-boot-starter-validation`) nos DTOs de entrada.
- **Busca sobre o corpus oficial (pgvector)** isolada atrás de uma interface própria
  (`*Port`/`*Gateway`) quando essa feature começar — não implementar direto no service, já
  que é a peça com mais chance de trocar de provedor/implementação.

## Fluxo de desenvolvimento (branch, PR)

- **Branch base para tudo:** `dev` — não abrir branch de trabalho a partir de `main`
  diretamente (exceção: hotfix urgente de produção, fora do fluxo padrão).
- **Nome de branch:** `<tipo>/<descricao-curta-em-kebab-case>`, reaproveitando os tipos já
  usados nos commits (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`). Ex.:
  `feat/geracao-plano-priorizado`, `fix/validacao-dto-endereco`. Com issue vinculada (ainda
  não obrigatório neste projeto): `<tipo>/<numero>-<descricao>`.
- **PR de branch de trabalho → `dev`:** título em Conventional Commits (vira a mensagem do
  squash-merge). Corpo com `## Resumo` (bullets) e `## Test plan` (checklist).
- **Merge:** squash and merge, para manter `dev`/`main` com histórico linear.
- **Promoção `dev` → `main`:** PR aberto em momento oportuno, quando o que acumulou em `dev`
  estiver validado em uso. Título descritivo do lote, não precisa seguir um único tipo
  Conventional Commit.

## Guardrails do Claude Code

- **Hook `protect-files.sh`** (`PreToolUse`, em `.claude/hooks/`) bloqueia edição de
  arquivos sensíveis (CI, segredos, certificados) — ver `.claude/settings.json`.
- **Agente `architecture-guardian`** (`.claude/agents/`) audita, sob demanda, se o código
  escrito respeita as convenções de camada/feature acima — só relatório, não bloqueia nada.

## Comandos

```bash
./mvnw spring-boot:run   # roda a aplicação local (sobe o Postgres via Docker Compose automaticamente)
./mvnw verify             # roda testes, incluindo integração via Testcontainers
./mvnw compile             # só compila
```

Health check em `/actuator/health` quando a aplicação está no ar.

## CI

GitHub Actions (`.github/workflows/ci.yml`) roda `./mvnw -B verify` em push/PR para `main` e `dev`, com JDK 21 (Temurin).

## Convenções de commit

Commits seguem Conventional Commits em português (ex: `chore: esqueleto inicial do projeto`). Prefixos usados: `chore`, `feat`, `fix`, `test`, `docs`, `refactor`.

## Handoff Claude ↔ Cursor

Fluxo de dois agentes no mesmo worktree: Claude planeja e revisa, Cursor executa. Contrato
em `.handoff/` (`plan.md` → `exec.md` → `review.md`), instalado por
`scripts/handoff/install.sh` (roda sozinho via `orca.yaml` ao criar um worktree). Skills:
`.claude/skills/handoff/SKILL.md` (Claude) e `.cursor/skills/executar-plano/SKILL.md`
(Cursor) — ambas materializadas a partir de `scripts/handoff/templates/`, não versionadas
diretamente. Use `/handoff` para despachar um plano aprovado ou revisar a execução do
Cursor.

## Estado atual do projeto

Esqueleto inicial apenas — sem controllers, services ou entidades de domínio ainda. A seção "Arquitetura e convenções de código" acima já fixa o padrão a seguir quando esse código começar a existir; não há nada em produção ainda para validar contra ela.
