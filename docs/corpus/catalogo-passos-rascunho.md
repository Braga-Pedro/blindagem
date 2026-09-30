# Catálogo de passos — rascunho

**Hipótese de trabalho**, para discussão. Cada passo tem condição de entrada, critério de verificação e fonte ([IDs em `fontes-candidatas.md`](fontes-candidatas.md)). O texto da instrução ao usuário será **escrito por nós**, sem copiar nem adaptar a Cartilha (F1), que entra só como "veja também" com link. Decisão **provisória** (ver decisão 2).

Entradas da triagem usadas nas condições (rascunho, alimentam [`docs/ux`](../ux/) quando revisado):

- **Tipo de dado exposto:** senhas / dados bancários ou de cartão / documentos e dados de identificação / telefone ou e-mail.
- **Origem conhecida?** sim / não.
- **Houve Pix feito por golpe?** sim / não.
- **Houve prejuízo, extorsão ou uso da identidade por terceiros?** sim / não.

## Passos

| ID | Passo | Entra quando | Verificação (como saber que está feito) | Fontes |
|---|---|---|---|---|
| P1 | Trocar a senha exposta em todos os serviços onde é usada | Senhas expostas | Usuário confirma que cada serviço listado por ele tem senha nova e diferente | F1 (veja também) |
| P2 | Ativar verificação em duas etapas | Senhas expostas | Usuário confirma a ativação nas contas principais (e-mail, banco, redes) | F1 (veja também) |
| P3 | Acionar o banco e bloquear/substituir cartões e contestar lançamentos irregulares | Dados bancários ou de cartão | Protocolo de atendimento do banco anotado | F1 (veja também) |
| P4 | Acionar o banco para devolução de Pix fraudulento (MED) **sem esperar o boletim de ocorrência** | Houve Pix por golpe | Protocolo do banco anotado; pedido feito em até 80 dias do Pix | F2 (v4.3; conferir v4.4), F10 |
| P5 | Emitir o relatório de contas em bancos (CCS) e conferir se há bancos que você não reconhece. **Aviso:** exige conta gov.br prata ou ouro ([como elevar o nível](https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br/niveis-da-conta-govbr), F11) | Documentos/dados de identificação expostos | Relatório emitido e todos os bancos reconhecidos, ou divergência registrada | F3, F11 |
| P6 | Pedir esclarecimentos ao controlador (o que vazou, quando, medidas adotadas) | Origem conhecida | Protocolo ou e-mail de resposta guardado | F4, F1 (veja também) |
| P7a | Registrar **petição de titular** na ANPD. **Aviso:** exige conta gov.br prata ou ouro (F11) | Origem conhecida **e** o controlador não atendeu o pedido do P6 | Requerimento aberto e acompanhável no serviço gov.br; comprovação do contato prévio anexada (P6) | F5, F6, F11 |
| P7b | Registrar **denúncia** na ANPD, pelo serviço gov.br (acompanhável; exige conta prata ou ouro, F11). Alternativa anônima: Plataforma Fala.BR, **sem acompanhamento** do andamento | Origem desconhecida, ou problema que afeta vários titulares (ex.: falta de canal, segurança inadequada) | Via gov.br: requerimento aberto e acompanhável. Via Fala.BR: só a confirmação de envio (não há acompanhamento) | F5, F6, F11, F12 |
| P8 | Registrar boletim de ocorrência | Prejuízo financeiro, extorsão ou uso da identidade por terceiros | Número do BO | F1 (veja também) |

## Aviso fixo (fora do catálogo de passos)

**Redobrar cuidado com golpes após o vazamento** (não clicar em links, confirmar destinatário antes de transferir). Não é passo porque não é verificável de forma objetiva. Aparece sempre no plano, como aviso, sem checklist. Fonte: F1 (veja também).

## Ordem sugerida de prioridade (a validar)

1. Contenção financeira imediata: **P4**, **P3** (o prazo do Pix pesa).
2. Contenção de acesso: **P1**, **P2**.
3. Investigação da exposição: **P5**, **P6**.
4. Escalada e registro: **P7a**/**P7b**, **P8**. A ANPD responde em até 30 dias úteis (F6): não é ação de contenção imediata.
5. Aviso fixo de cuidado com golpes, ao longo de todo o plano.

Restrição de ordem: **P6 vem antes de P7a**, porque a petição exige comprovar o contato prévio com o controlador (F5).

## Decisões tomadas

1. **P9 vira aviso fixo**, fora do catálogo (ver seção acima).
2. **Texto dos passos é nosso**, com a Cartilha (F1) só como "veja também". Aceito **momentaneamente**: segue valendo a busca por fonte primária de reuso permitido para P1–P3 e P8.
3. **Prazo de 80 dias do Pix confirmado** pela página do BCB sobre segurança do Pix (F10, informada pelo autor). Ainda pendente: conferir se a v4.4 do guia (F2) mudou o fluxo de P4.
4. **P5 e P7 exigem conta gov.br prata ou ouro** (F3 e F6; o P5 pede também verificação em duas etapas). Tratado com **aviso** e link governamental de como elevar o nível (F11), sem passo prévio.
5. **P7a depende de P6**, e o plano deve garantir essa ordem.
6. **Prazo de resposta da ANPD (até 30 dias úteis)** entra como expectativa no plano, não como contenção imediata.
7. **Denúncia anônima:** o serviço gov.br exige conta prata ou ouro e não permite anonimato. O canal anônimo é a Plataforma Fala.BR (F12).
8. **Acompanhamento:** denúncia pelo gov.br é acompanhável; pela Fala.BR anônima, não. O critério de verificação de P7b reflete isso.
9. **Fora do escopo por ora**, por falta de fonte: vazamento de dados de saúde, de menores, de documentos como CNH, e linhas de celular ativadas no CPF (Cadastro Pré-Pago). Não incluir alternativas sem fonte.
10. **Revisão do catálogo:** feita pelo autor do projeto, **mensalmente**, e a cada mudança de versão das fontes conhecida.

## Pendências que restam

- **Número de protocolo do requerimento (gov.br):** F6 fala em resultado acompanhável, mas não detalha um número. Confirmar no serviço real o que o usuário recebe e ajustar o critério de verificação de P7a/P7b.
- **F2 v4.4:** ler e conferir P4 (vigência parcial desde 01/09/2026, nova etapa em 26/10/2026).
- **F10 e F12:** o acesso automático não devolve conteúdo (páginas que dependem de JavaScript). Ler no navegador: na F10, o prazo de 80 dias; na F12, se há manifestação anônima e acompanhamento.
- **F11:** lida. Confirma os métodos de subir para prata e ouro. Licença CC BY-ND 3.0: só citar e linkar, o que já fazemos.
