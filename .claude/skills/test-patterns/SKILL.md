---
name: test-patterns
description: >-
  Convenção de teste do Blindagem — quando escrever unit test simples vs. teste de
  integração com Testcontainers, e como rodar. Use ao escrever, cobrir ou revisar testes
  neste projeto.
---

# Padrões de teste do Blindagem

## Quando usar cada tipo

- **Unit test** (`src/test/java`, sem `@SpringBootTest`): regra de negócio isolada — lógica
  de priorização do plano, validação, mapeamento DTO ↔ entidade. Rápido, sem contexto Spring.
- **Teste de integração** (`@SpringBootTest` + Testcontainers, via
  `spring-boot-testcontainers` e `testcontainers-postgresql`, já no `pom.xml`): qualquer
  coisa que toque repository/JPA/query real — Testcontainers sobe um Postgres descartável
  por execução, não precisa de banco rodando à parte.

Regra prática: se o teste não instancia nenhum bean gerenciado pelo Spring, não use
`@SpringBootTest` — só encarece a suíte sem ganhar cobertura real.

## Como rodar

```bash
./mvnw verify   # roda tudo, unit + integração (documentado em CLAUDE.md)
```

Para rodar só um teste específico durante o desenvolvimento:

```bash
./mvnw test -Dtest=NomeDaClasseTest
```

## Toda mudança de comportamento precisa de teste

Ao implementar ou alterar uma regra de negócio, crie ou atualize o teste correspondente
antes de considerar a tarefa concluída — não deixe cobertura para depois.
