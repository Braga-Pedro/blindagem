# Catálogo de passos — rascunho

**Hipótese de trabalho**, para discussão. Cada passo tem condição de entrada, critério de verificação e fonte ([IDs em `fontes-candidatas.md`](fontes-candidatas.md)). O texto da instrução ao usuário será **escrito por nós**, sem copiar nem adaptar a Cartilha (F1).

Entradas da triagem usadas nas condições (rascunho, alimentam [`docs/ux`](../ux/) quando revisado):

- **Tipo de dado exposto:** senhas / dados bancários ou de cartão / documentos e dados de identificação / telefone ou e-mail.
- **Origem conhecida?** sim / não.
- **Houve Pix feito por golpe?** sim / não.
- **Houve prejuízo, extorsão ou uso da identidade por terceiros?** sim / não.

## Passos

| ID | Passo | Entra quando | Verificação (como saber que está feito) | Fontes |
|---|---|---|---|---|
| P1 | Trocar a senha exposta em todos os serviços onde é usada | Senhas expostas | Usuário confirma que cada serviço listado por ele tem senha nova e diferente | F1 (referência) |
| P2 | Ativar verificação em duas etapas | Senhas expostas | Usuário confirma a ativação nas contas principais (e-mail, banco, redes) | F1 (referência) |
| P3 | Acionar o banco e bloquear/substituir cartões e contestar lançamentos irregulares | Dados bancários ou de cartão | Protocolo de atendimento do banco anotado | F1 (referência) |
| P4 | Acionar o banco para devolução de Pix fraudulento (MED) **sem esperar o boletim de ocorrência** | Houve Pix por golpe | Protocolo do banco anotado; pedido feito em até 80 dias do Pix | F2 (v4.3; conferir v4.4) |
| P5 | Emitir o relatório de contas em bancos (CCS) e conferir se há bancos que você não reconhece | Documentos/dados de identificação expostos | Relatório emitido e todos os bancos reconhecidos, ou divergência registrada | F3 |
| P6 | Pedir esclarecimentos ao controlador (o que vazou, quando, medidas adotadas) | Origem conhecida | Protocolo ou e-mail de resposta guardado | F1 (referência), F4 |
| P7a | Registrar **petição de titular** na ANPD | Origem conhecida **e** o controlador não atendeu o pedido do P6 | Requerimento aberto e acompanhável no serviço gov.br; comprovação do contato prévio anexada (P6) | F5, F6 |
| P7b | Registrar **denúncia** na ANPD | Origem desconhecida, ou problema que afeta vários titulares (ex.: falta de canal, segurança inadequada) | Requerimento aberto e acompanhável no serviço gov.br | F1 (referência), F5, F6 |
| P8 | Registrar boletim de ocorrência | Prejuízo financeiro, extorsão ou uso da identidade por terceiros | Número do BO | F1 (referência) |
| P9 | Redobrar cuidado com golpes após o vazamento (não clicar em links, confirmar destinatário antes de transferir) | Sempre | Difícil de verificar; provável passo informativo. Ver questão 1 | F1 (referência) |

## Ordem sugerida de prioridade (a validar)

1. Contenção financeira imediata: **P4**, **P3** (o prazo do Pix pesa).
2. Contenção de acesso: **P1**, **P2**.
3. Investigação da exposição: **P5**, **P6**.
4. Escalada e registro: **P7a**/**P7b**, **P8**.
5. **P9** ao longo de todo o plano.

## Questões abertas

1. **P9 não é verificável de forma objetiva.** Contraria a regra "todo passo é verificável". Opções: tirá-lo do plano e deixar como aviso fixo, ou transformar em passos verificáveis (ex.: "avisar contatos de que sua conta pode ser usada em golpe").
2. **Quase todas as fontes de P1–P3, P8 e P9 são a Cartilha (F1)**, que só pode ser citada e linkada. Precisamos de fonte primária de reuso permitido para o texto desses passos, ou aceitar que o texto seja nosso com a Cartilha só como "veja também".
3. **F2 tem versão 4.4 em vigor parcial desde 01/09/2026.** Confirmar se o prazo de 80 dias e o fluxo de P4 mudaram.
4. **P5 e P7 exigem conta gov.br prata ou ouro** (F3 e F6; o P5 pede também verificação em duas etapas). Isso é obstáculo para parte do público; cabe passo prévio ("elevar o nível da conta gov.br") ou aviso.
5. **P7a depende de P6.** A petição exige comprovar o contato prévio com o controlador (F5), então o critério de verificação do P6 (protocolo/e-mail guardado) é pré-requisito do P7a. O plano deve garantir essa ordem.
6. **Prazo de resposta da ANPD: até 30 dias úteis** (F6). O plano não deve tratar a petição como ação de contenção imediata.
7. **Inconsistência a conferir em F5/F6:** F5 diz que denúncias podem ser anônimas, mas F6 exige login gov.br prata ou ouro para usar o serviço. Não sabemos se o modo anônimo existe hoje.
8. **Protocolo:** F6 fala em resultado acompanhável, mas não detalha um número de protocolo. O critério "número do requerimento" do P7 deve ser confirmado no serviço real.
9. **Falta cobrir**, por ora sem fonte lida: vazamento de dados de saúde, de menores, de documentos como CNH, e linhas de celular ativadas no CPF (Cadastro Pré-Pago, sem fonte oficial confirmada).
10. **Quem valida e revisa o catálogo** a cada mudança das fontes, e com que periodicidade.
