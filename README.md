# Blindagem

Assistente que gera um plano de ação priorizado e verificável para pessoas expostas por vazamento de dados pessoais ou golpe de voz clonada — sem nunca pedir ou armazenar o CPF de quem usa.

> **Status: início do desenvolvimento.** Este repositório contém o esqueleto do projeto (Spring Boot, PostgreSQL, CI). A pesquisa, o desenho do domínio e o corpus de fontes oficiais estão sendo produzidos em paralelo, como parte de um projeto de extensão universitária.

## O problema

Ferramentas existentes dizem que seus dados vazaram, mas nenhuma diz o que fazer, em que ordem, e como verificar que cada passo foi concluído. E a fronteira mais nova, o golpe de voz clonada de um familiar, não tem nenhuma ferramenta de resposta — só alertas genéricos recomendando "combine uma palavra-código", sem ensinar como implantar uma na prática.

O Blindagem cobre as duas superfícies: exposição de **dados** (o que se sabe sobre você) e exposição de **voz** (o que se consegue imitar de você).

## O que este projeto não é

- Não é um verificador de vazamento — não constrói nem hospeda base de CPFs ou credenciais.
- Não é um detector de deepfake — não tenta identificar se um áudio é sintético.
- Não sintetiza, clona ou reproduz voz, em nenhuma hipótese.
- Não é um agregador de links — cada passo do plano gerado é verificável, não apenas uma sugestão de pesquisa.

## Stack

- **Java 21** + **Spring Boot 4**
- **PostgreSQL** (com pgvector planejado para a camada de busca sobre o corpus oficial)
- **Docker Compose** para o ambiente local
- **Testcontainers** para testes de integração contra banco real

## Rodando localmente

Pré-requisitos: JDK 21 e Docker.

```bash
./mvnw spring-boot:run
```

O Spring Boot sobe o `compose.yaml` automaticamente (PostgreSQL) via `spring-boot-docker-compose`. Health check em `/actuator/health`.

## Testes

```bash
./mvnw verify
```

Os testes de integração usam Testcontainers, que provisiona um PostgreSQL descartável por execução — não é preciso banco rodando à parte.

## Licença

Ainda não definida.
