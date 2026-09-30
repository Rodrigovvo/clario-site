---
title: De quem é o código-fonte: a cláusula de propriedade intelectual que toda empresa deve exigir
slug: propriedade-intelectual-codigo-fonte-software-sob-medida
date: 2026-11-03
area: Engenharia e contratos
description: O que a Lei 9.609/98 determina sobre desenvolvimento encomendado, o risco de pagar para construir e continuar refém de aluguel, e como garantir soberania tecnológica no contrato.
read_time: 5 min
keywords: propriedade intelectual software sob medida, codigo fonte de quem e, contrato desenvolvimento software clausulas, lei do software 9609, cessao de direitos autorais software, titularidade de software corporativo
---

Existe uma situação desconfortável que se repete com frequência nos departamentos jurídicos de médias e grandes empresas brasileiras: a diretoria investe duzentos mil reais para encomendar um sistema próprio de gestão, acompanha o desenvolvimento ao longo de meses e, quando solicita a entrega do código-fonte e dos scripts de instalação para realizar uma auditoria ou migrar de provedor de hospedagem, recebe uma negativa do desenvolvedor. A empresa descobre, com espanto, que pagou o desenvolvimento inteiro, mas o contrato redigido pelo fornecedor concedeu apenas uma licença precária de uso. O código-fonte, segundo a cláusula esquecida em letras miúdas, pertence exclusivamente à fábrica de software.

Essa armadilha transforma um ativo estratégico da empresa em uma fonte eterna de dependência forçada. Para adicionar um novo campo no cadastro de fornecedores, a empresa precisa pagar o valor que o desenvolvedor original estipular. Se a relação comercial se deteriorar, a empresa perde o investimento realizado e fica impossibilitada de transferir a sustentação para outra equipe técnica.

Essa insegurança não decorre de nenhuma fatalidade técnica; decorre puramente de redação contratual frouxa e da falta de conhecimento sobre o que diz a legislação brasileira sobre software.

## O que a legislação brasileira diz sobre o software sob encomenda

No Brasil, a proteção jurídica aos programas de computador é regida pela Lei nº 9.609/1998 (conhecida como a Lei do Software) e, de forma subsidiária, pela Lei de Direitos Autorais (Lei nº 9.610/1998). O código-fonte é considerado legalmente uma criação intelectual equiparada à obra literária.

O artigo 4º da Lei nº 9.609/1998 estabelece uma regra basilar: quando o software é desenvolvido sob encomenda expressa ou mediante vínculo de prestação de serviços contratada para esse fim específico, os direitos relativos ao programa pertencem à empresa contratante, salvo expressa disposição em contrário.

A armadilha reside precisamente na expressão "salvo estipulação em contrário". Muitos fornecedores de TI inserem minutas contratuais padrão onde invertem discretamente essa regra legal: definem que a empresa contratante adquire apenas a "cessão de direito de uso", mantendo a titularidade dos direitos autorais patrimoniais com a desenvolvedora. Ao assinar esse documento sem ressalvas, o cliente abre mão da proteção que a própria lei lhe confere.

## As cláusulas indispensáveis para a soberania técnica da empresa

Para assegurar que o software sob encomenda seja um patrimônio real e inalienável da sua organização, o contrato de prestação de serviços deve conter disposições explícitas e inegociáveis:

1. **Cessão total e irrevogável dos direitos patrimoniais de autor:** o contrato deve consignar que a totalidade dos direitos autorais de natureza patrimonial sobre o código-fonte, arquitetura, scripts, telas, consultas a banco de dados e documentação gerada é transmitida em caráter definitivo e exclusivo à contratante, sem limitação de tempo, território ou modalidade de uso.
2. **Acesso imediato e contínuo ao repositório de código:** o desenvolvimento não deve ocorrer em uma caixa-preta isolada. A contratante deve ser a proprietária da conta do repositório Git, ou ao menos ter permissão de leitura integral e espelhamento diário de todas as alterações realizadas. A cada novo commit, o ativo já está sob custódia da empresa.
3. **Entrega de instruções de montagem e deploy independente:** código-fonte sem o manual de compilação e sem as receitas de infraestrutura é apenas um amontoado inútil de texto. O fornecedor deve ser obrigado a entregar os arquivos de configuração de ambiente e as instruções passo a passo para que qualquer outro engenheiro de software qualificado consiga subir o sistema do zero em um servidor independente em poucas horas.
4. **Propriedade e livre exportação da base de dados:** os dados operacionais da empresa, tabelas, diagramas de relacionamento e dicionários de termos pertencem integralmente à contratante. O contrato deve fixar penalidades severas caso o fornecedor crie qualquer entrave técnico ou financeiro para a extração integral da base de dados em formatos abertos e universais.

## Por que fornecedores confiáveis não retêm o código do cliente

Existe um receio infundado entre algumas empresas de que exigir a posse do código-fonte tornará a contratação mais cara ou causará atritos com os desenvolvedores. Pelo contrário: a postura do fornecedor diante dessa exigência funciona como o mais confiável teste de maturidade ética e técnica.

Empresas de desenvolvimento de software que possuem rigor de engenharia e prestam serviços de alto nível não têm nenhum interesse em aprisionar clientes por meio de artimanhas contratuais. Elas sabem que a retenção legítima de um parceiro corporativo se constrói pela entrega de código estável, pela rapidez no atendimento e pelo suporte proativo à infraestrutura.

Quem tenta trancar o código-fonte a sete chaves costuma ser o fornecedor inseguro, que teme que outro profissional inspecione a qualidade do código entregue ou que precisa do artifício do aprisionamento para continuar cobrando mensalidades por um serviço medíocre.

Na Clariô, a soberania do cliente é premissa de engenharia. Cada linha de código que escrevemos para sistemas sob encomenda nasce no repositório da sua organização, acompanhada de documentação enxuta e pronta para ser mantida pela sua própria equipe ou por quem você preferir. Para conversar sobre o desenvolvimento do seu projeto sob termos claros e transparentes, escreva para contato@clariosistemas.com.br ou ligue para (38) 9 2000-0181.
