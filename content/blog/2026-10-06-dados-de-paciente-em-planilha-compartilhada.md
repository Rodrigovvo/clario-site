---
title: A planilha de pacientes na pasta compartilhada é um problema de LGPD antes de ser um problema de organização
slug: dados-de-paciente-em-planilha-compartilhada
date: 2026-10-06
area: Saúde e proteção de dados
description: Dado de saúde é dado pessoal sensível na Lei 13.709. O que isso significa na prática para a recepção de uma clínica que controla agenda e prontuário em arquivos compartilhados na rede.
read_time: 6 min
---

A conversa sobre proteção de dados em clínicas costuma começar pelo lugar errado. Fala-se em termo de consentimento, em aviso de privacidade no rodapé do site, em encarregado de dados. São obrigações reais, e quase todas elas tratam do que a clínica declara. Enquanto isso, o arquivo `agenda_setembro_v3_FINAL.xlsx` continua aberto na pasta compartilhada da rede, com nome completo, telefone, convênio e motivo da consulta de mil e duzentos pacientes, acessível a qualquer pessoa que ligue qualquer computador da recepção.

A Lei 13.709 classifica dado referente à saúde como dado pessoal sensível. A consequência prática é direta: o regime de tratamento é mais estrito que o de um cadastro comercial comum, e o dever de proteger não se cumpre com documento assinado. Cumpre-se com controle de acesso.

## O que a planilha não consegue fazer

O problema técnico não é a planilha em si, que é uma ferramenta excelente para o que foi projetada. É que ela não tem, e não pode ter, três coisas que o tratamento de dado sensível exige.

Não tem identidade. O arquivo não sabe quem o abriu. Sabe, no máximo, qual usuário do Windows estava logado naquela máquina, o que em uma recepção com senha compartilhada colada no monitor equivale a não saber nada. Quando um dado vaza, a pergunta do titular e da autoridade é quem acessou. A planilha não responde.

Não tem granularidade. Ou a pessoa abre o arquivo inteiro, com todas as colunas e todas as linhas, ou não abre nada. A estagiária que precisa confirmar horários da semana recebe, no mesmo gesto, o histórico de procedimentos do ano inteiro. O princípio da necessidade, que manda limitar o tratamento ao mínimo indispensável, é estruturalmente impossível de cumprir em um arquivo monolítico.

Não tem histórico. Alguém salva por cima, a versão anterior desaparece, e não há registro de qual linha foi alterada nem quando. Isso quebra ao mesmo tempo a segurança e a operação: é a mesma falha que faz o paciente chegar para uma consulta que sumiu da agenda.

## O caminho mais curto entre o vazamento e a clínica

Vale descrever a rota concreta, porque ela costuma ser mais banal do que o imaginário de ataque hacker sugere. A recepcionista precisa trabalhar de casa em um sábado e envia o arquivo para o próprio e-mail pessoal. Meses depois ela sai da clínica. A cópia permanece em uma caixa de entrada que a clínica nunca controlou, protegida por uma senha que a clínica não conhece, em um provedor que a clínica não contratou.

Ninguém agiu de má-fé nessa história. Todos agiram de forma razoável diante de uma ferramenta que não oferecia alternativa. Culpar a equipe por isso é o mesmo que culpar o motorista pela estrada sem acostamento. A responsabilidade, inclusive a legal, é de quem escolheu a ferramenta.

## O que muda com um sistema, mesmo um pequeno

Nada do que segue exige uma plataforma hospitalar de duzentas telas. São propriedades de qualquer aplicação web bem construída, e cada uma resolve um item da lista acima:

- **Cada pessoa tem o próprio acesso.** Recepção vê agenda e contato. Profissional vê o prontuário dos próprios pacientes. A direção vê o faturamento. Ninguém vê o que não precisa para trabalhar.
- **Todo acesso deixa rastro.** Quem abriu qual ficha, em que dia, a que hora. É o que transforma a resposta a um incidente em um relatório, em vez de uma suposição.
- **O desligamento de um funcionário é um clique.** Revogar acesso encerra a exposição no mesmo instante, coisa que nenhum arquivo copiado permite.
- **O dado fica em banco relacional com cópia de segurança automática.** A corrupção do arquivo deixa de ser um evento capaz de apagar o histórico de um mês.
- **A clínica continua dona dos próprios dados.** Exportação em formato aberto, sem reféns contratuais. Isso não é cortesia: é condição para atender pedido de portabilidade do titular.

## O primeiro passo custa uma tarde

Antes de qualquer contratação, dois inventários resolvem metade do problema e não dependem de fornecedor algum. O primeiro: listar todos os lugares onde existe dado de paciente hoje, incluindo WhatsApp da recepção, e-mails, pendrives e a pasta da rede. O segundo: listar quem tem acesso a cada um deles, incluindo ex-funcionários. A maioria das clínicas descobre nesse exercício que o número de cópias é maior do que a direção imaginava, e que pelo menos uma pessoa que saiu há um ano ainda tem acesso a alguma coisa.

Feito o inventário, a decisão sobre sistema deixa de ser sobre recursos bonitos em apresentação comercial e passa a ser sobre o que de fato reduz exposição. O sistema mais seguro não é o que tem mais telas de confirmação. É o que não guarda o dado que não precisava guardar e não mostra o dado a quem não precisa vê-lo.

A Clariô constrói sistemas de agendamento e cadastro sob medida para clínicas, com controle de acesso por perfil, registro de auditoria e banco próprio da clínica. Para um diagnóstico objetivo da sua rotina, escreva para contato@clariosistemas.com.br.
