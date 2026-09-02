# Site institucional — Clariô

Página única, sem build e sem dependência externa: um `index.html` que funciona
em qualquer hospedagem estática.

```
public/index.html     a página
public/marca/         ativos da identidade visual
wrangler.jsonc        configuração do deploy na Cloudflare
```

## Identidade visual

Vem do sistema de marca da Clariô, em `~/Documentos/Clariô`:

- **Paleta** das cores da Festa de Agosto — vermelho `#A93B30` (Divino),
  ouro `#E3A22B` (sol), rosa `#C56F7F` (São Benedito), azul `#3F6E8C`
  (N. S. do Rosário), verde `#5E9086` (pena de pavão)
- **Tipografia**: Baloo 2 nos títulos, Nunito no texto, JetBrains Mono nos
  dados (CNPJ, telefone) — todas SIL Open Font License
- **Emblema do catopê** como marca d'água da capa

O tema escuro não foi inventado: as cores saem do próprio `lockup-dark.svg`,
inclusive o fundo `#2A2018`, que é a cor da placa do lockup — assim ela
desaparece no cabeçalho.

Contraste verificado: AAA no tema escuro, AA no claro.

Existe por um motivo concreto: a verificação de negócio da Meta (spec
[`F0-T01`](../amparo/specs/00-fase0/F0-T01-conta-meta-e-numero.md) do Amparo)
exige site institucional e e-mail no domínio da empresa.

## Antes de publicar

Os dados do cartão CNPJ já estão preenchidos. Conferir antes de qualquer
alteração: divergência entre o site e os documentos é a causa mais comum de
reprovação na verificação de negócio da Meta.

## Publicar na Cloudflare

O deploy usa **Workers Static Assets** — o caminho atual da Cloudflare para site
estático, que substituiu o Pages clássico em projetos novos.

Em `dash.cloudflare.com` → **Workers & Pages** → **Create** → conectar este
repositório, com:

| Campo | Valor |
|---|---|
| Project name | `clario-site` |
| Build command | *(vazio — não há build)* |
| Deploy command | `npx wrangler deploy` |

O `npx wrangler deploy` lê o `wrangler.jsonc`, que aponta para `public/`. Cada
push na `main` publica sozinho.

Depois, em **Custom domains**, adicionar `clariosistemas.com.br` e `www`.

### Publicar da linha de comando, se preferir

```bash
npx wrangler deploy
```

## Alternativa: GitHub Pages

**Settings** → **Pages** → branch `main`, pasta `/public`. Também gratuito, com
HTTPS. Não usa o `wrangler.jsonc`.

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
