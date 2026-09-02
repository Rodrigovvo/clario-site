# Site institucional — Clariô

Página única, sem build e sem dependência externa: um `index.html` que funciona
em qualquer hospedagem estática.

Existe por um motivo concreto: a verificação de negócio da Meta (spec
[`F0-T01`](../amparo/specs/00-fase0/F0-T01-conta-meta-e-numero.md) do Amparo)
exige site institucional e e-mail no domínio da empresa.

## Antes de publicar

1. Preencher no `index.html` os três campos destacados em amarelo — CNPJ,
   endereço e telefone — com os dados **exatos** do cartão CNPJ. Divergência
   entre site e documento é a causa mais comum de reprovação.
2. Remover o bloco `<div class="aviso">` da seção "Dados da empresa".
3. Conferir se a razão social bate com o cartão CNPJ.

## Publicar no Cloudflare Pages

Gratuito, HTTPS automático, e o DNS do domínio fica no mesmo lugar — o que
facilita a etapa do e-mail.

1. Criar repositório git com este diretório e enviar para o GitHub.
2. Em `dash.cloudflare.com` → **Workers & Pages** → **Create** → **Pages** →
   conectar o repositório.
3. Build: **nenhum**. Diretório de saída: `/` (raiz).
4. Em **Custom domains**, adicionar `clariosistemas.com.br` e `www`.

## Alternativa: GitHub Pages

Repositório → **Settings** → **Pages** → branch `main`, pasta `/root`. Domínio
personalizado no mesmo lugar. Também gratuito, com HTTPS.

## DNS no registro.br

Depois de registrar `clariosistemas.com.br`, aponte os servidores DNS para os
da Cloudflare (o painel deles informa quais). A partir daí, site e e-mail são
configurados pela Cloudflare, não pelo registro.br.

## E-mail — Zoho Mail (plano gratuito)

O e-mail no domínio é o que a Meta usa para confirmar a titularidade.

1. Criar conta em `zoho.com/mail`, plano **Forever Free**, e informar o domínio.
2. Provar a posse do domínio com o registro TXT que o Zoho fornece.
3. Criar a caixa `contato@clariosistemas.com.br`.
4. Configurar no DNS os registros que o Zoho indicar: **MX**, **SPF** (TXT) e
   **DKIM** (TXT). Sem SPF e DKIM, a mensagem enviada cai em spam.
5. Testar envio e recebimento antes de submeter qualquer coisa à Meta.

Propagação de DNS costuma levar de minutos a algumas horas.

## Ordem sugerida

```
registrar domínio → apontar DNS → publicar site → configurar e-mail
     → testar → só então submeter a verificação de negócio da Meta
```

Submeter antes de o site estar no ar e o e-mail funcionando é o que causa
reprovação e obriga a esperar o ciclo de análise de novo.
