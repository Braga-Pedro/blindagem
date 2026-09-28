#!/usr/bin/env bash
# Descreve como rodar comandos neste checkout, em markdown, para o bloco
# "Ambiente" do .handoff/plan.md.
#
# Projeto simples (um único checkout, sem infra por worktree): os comandos
# valem como estão. Se o blindagem ganhar infra paralela por worktree (como
# o giroapp tem para o Postgres), adapte este script para descrevê-la.

set -euo pipefail

cat <<'EOF'
Checkout comum, sem infra paralela por worktree. `./mvnw` funciona direto:

    ./mvnw compile
    ./mvnw verify
    ./mvnw spring-boot:run

`spring-boot-docker-compose` sobe o Postgres automaticamente ao rodar a
aplicação ou os testes de integração (Testcontainers cuida dos testes à
parte, sem precisar de banco no ar).
EOF
