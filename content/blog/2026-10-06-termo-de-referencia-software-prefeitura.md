---
title: O que uma prefeitura deve exigir num termo de referência de software
slug: termo-de-referencia-software-prefeitura
date: 2026-10-06
area: Gestão pública e contratações
description: Propriedade dos dados, exportação em formatos abertos e entregas por módulo em produção. Como evitar contratos de licença que aprisionam a administração municipal.
read_time: 6 min
---

Contratar software no setor público costuma seguir um roteiro conhecido: um termo de referência longo, copiado de outro município, repleto de exigências genéricas de conformidade e itens de catálogo que nenhuma equipe técnica da prefeitura vai fiscalizar. O resultado, homologado após meses de licitação, costuma ser um sistema pesado, desenhado para satisfazer o edital em vez de atender a rotina dos servidores na ponta.

Dois anos depois, quando o contrato se aproxima do fim ou a administração muda, descobre-se a armadilha clássica: os dados dos munícipes, os atendimentos de saúde e os registros de arrecadação estão trancados em um banco proprietário que a empresa vencedora se recusa a entregar sem cobrar uma taxa extraordinária de migração.

A soberania sobre a informação pública começa na redação do Termo de Referência (TR). Três cláusulas técnicas simples separam um contrato vantajoso para o interesse público de um aprisionamento tecnológico de longo prazo.

## 1. Propriedade incondicional dos dados e formatos abertos

A prefeitura não deve apenas declarar que é proprietária dos dados cadastrados: deve estabelecer os meios técnicos e a periodicidade em que esses dados retornam aos seus servidores.

No TR, inclua obrigatoriamente:

* **Exportação periódica automatizada:** o fornecedor deve disponibilizar rotina semanal ou mensal que gere uma cópia integral do banco de dados em formato aberto e relacional (como SQL, PostgreSQL dump ou arquivos CSV padronizados com codificação UTF-8).
* **Vedação a formatos proprietários:** proibir expressamente que backups sejam entregues em formatos criptografados por chave exclusiva do fornecedor ou que exijam software comercial pago de terceiros para leitura.
* **Acesso contínuo a APIs de consulta:** a administração municipal deve ter direito de ler seus próprios dados via interfaces abertas de programação (APIs REST documentadas), permitindo auditorias dos órgãos de controle interno e externo sem intermediação onerosa.

Se a empresa contratada exigir o pagamento de consultoria adicional apenas para entregar a lista de pacientes cadastrados no município, o TR falhou na premissa mais básica do direito administrativo.

## 2. Prazos de entrega escalonados por módulo em produção

O modelo tradicional de contratação em bloco único, no qual o município espera seis a doze meses para ver o sistema rodando pela primeira vez, quase sempre resulta em termos aditivos de prazo e frustração operacional.

A exigência correta é a homologação em produção por marcos mensais ou quinzenais:

* **Primeiro marco:** o módulo central que resolve a dor imediata entra em operação assistida com dados reais (por exemplo, a lista de visitas domiciliares na atenção primária ou o protocolo geral da secretaria).
* **Critério de pagamento condicionado ao uso real:** o desembolso das parcelas do contrato deve estar vinculado a atestados de recebimento definitivo de cada módulo funcionalmente testado pelos servidores públicos da ponta, não a relatórios abstratos de horas trabalhadas.

Essa abordagem garante que, se um fornecedor falhar na execução inicial, o município interrompe os pagamentos antes de comprometer o orçamento do exercício financeiro.

## 3. Compatibilidade com o parque de máquinas real do município

É comum fornecedores apresentarem softwares corporativos que exigem computadores com processadores modernos e conexões de fibra dedicada. Quando o sistema chega à Unidade Básica de Saúde da zona rural ou ao balcão de atendimento do prédio histórico, a tela sequer carrega.

O TR precisa amarrar a realidade física:

* **Execução pura em navegadores padrão:** o sistema deve rodar integralmente no navegador (HTML5, CSS e JavaScript padrão), sem exigir instalação de clientes pesados, emuladores ou componentes proprietários no Windows.
* **Tolerância a conexões instáveis:** a interface deve ter peso reduzido de transferência (poucos kilobytes por requisição), viabilizando o preenchimento de cadastros mesmo em conexões móveis lentas de 3G ou 4G.
* **Clareza de papéis e conformidade com a LGPD:** controle estrito de acessos por matrícula funcional, com trilha de auditoria completa que registre data, hora e servidor que visualizou cada prontuário ou documento protegido.

## A experiência da Clariô no setor público

Com essa visão de engenharia enxuta e respeito aos recursos municipais, desenvolvemos produtos como o Amparo, projetado especificamente para ordenar visitas domiciliares de idosos na atenção básica sem exigir licenças astronômicas nem travar no computador do posto de saúde.

Para estruturar termos de referência tecnicamente seguros ou avaliar demandas específicas de software no setor público municipal, converse com nossa equipe: contato@clariosistemas.com.br ou pelo telefone institucional (38) 9 2000-0181.
