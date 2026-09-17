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

## Comandos

```bash
./mvnw spring-boot:run   # roda a aplicação local (sobe o Postgres via Docker Compose automaticamente)
./mvnw verify             # roda testes, incluindo integração via Testcontainers
./mvnw compile             # só compila
```

Health check em `/actuator/health` quando a aplicação está no ar.

## CI

GitHub Actions (`.github/workflows/ci.yml`) roda `./mvnw -B verify` em push/PR para `main`, com JDK 21 (Temurin).

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

Esqueleto inicial apenas — sem controllers, services ou entidades de domínio ainda. Ao propor código novo, não assumir camadas ou padrões arquiteturais que ainda não existem no repositório; perguntar antes de introduzir uma convenção nova (ex: separação por camada vs. por feature).
