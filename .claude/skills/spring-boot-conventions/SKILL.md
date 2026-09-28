---
name: spring-boot-conventions
description: >-
  Convenções de código Spring Boot do Blindagem (injeção por construtor, DTO vs. entidade,
  onde colocar @Transactional). Use sempre que for escrever ou revisar um controller,
  service, repository, entidade ou DTO neste projeto.
---

# Convenções Spring Boot do Blindagem

Reforça o que está em `CLAUDE.md` → "Arquitetura e convenções de código", com exemplos
curtos. Se este arquivo e o `CLAUDE.md` divergirem no futuro, o `CLAUDE.md` é a fonte de
verdade — atualize este arquivo para bater com ele.

## Injeção de dependência: sempre por construtor

```java
// Ruim — injeção por campo
@Service
public class PlanoService {
    @Autowired
    private CorpusRepository corpusRepository;
}

// Bom — injeção por construtor (permite final, testável sem Spring)
@Service
public class PlanoService {
    private final CorpusRepository corpusRepository;

    public PlanoService(CorpusRepository corpusRepository) {
        this.corpusRepository = corpusRepository;
    }
}
```

## DTO vs. entidade: nunca expor `@Entity` no controller

```java
// Ruim — vaza a entidade JPA pela API
@GetMapping("/planos/{id}")
public Plano buscar(@PathVariable UUID id) { ... }

// Bom — DTO como record, mapeado explicitamente
public record PlanoResponse(UUID id, String status, List<PassoResponse> passos) {}

@GetMapping("/planos/{id}")
public PlanoResponse buscar(@PathVariable UUID id) { ... }
```

## `@Transactional` só na service

```java
// Ruim — no controller ou no repository
@RestController
class PlanoController {
    @Transactional // não faz isso aqui
    @PostMapping("/planos")
    ResponseEntity<PlanoResponse> criar(...) { ... }
}

// Bom — na service, na fronteira da operação de negócio
@Service
class PlanoService {
    @Transactional
    public Plano criar(NovoPlanoRequest request) { ... }
}
```

## Validação de entrada

DTOs de request usam Bean Validation (`spring-boot-starter-validation`, já no `pom.xml`):

```java
public record NovoPlanoRequest(
    @NotBlank String tipoExposicao,
    @NotEmpty List<@Valid FonteRequest> fontes
) {}
```
