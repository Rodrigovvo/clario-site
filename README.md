# Site institucional: Clariô

Página única, sem build e sem dependência externa: um `index.html` que funciona
em qualquer hospedagem estática.

```
content/blog/                               artigos em Markdown (.md)
public/index.html                           a página principal
public/blog/                                páginas geradas do blog
public/blog/feed.xml                        feed RSS gerado a partir dos artigos publicados
public/sitemap.xml                          mapa do site para indexação (SEO)
public/robots.txt                           diretivas para rastreadores e ponteiro do sitemap
public/bcfc4849079645379c75ca0288a62c1e.txt chave de verificação do IndexNow (Bing)
public/marca/                               ativos da identidade visual
scripts/build_blog.py                       gerador do blog, agendamento e sitemap
scripts/indexnow.sh                         script para submissão ao IndexNow
scripts/publicar.sh                         script de validação, commit, push e deploy
wrangler.jsonc                              configuração do deploy na Cloudflare
.AGENTS/                                    plano de marketing, guia de voz e material de execução
```

O diretório `.AGENTS/` reúne a estratégia e o material operacional: o
[plano de marketing](.AGENTS/PLANO_DE_MARKETING.md), o
[guia de voz](.AGENTS/GUIA_DE_VOZ.md), o
[guia de prospecção](.AGENTS/PROSPECCAO_SOFTWARE_SOB_ENCOMENDA.md), o
[calendário editorial](.AGENTS/CALENDARIO_EDITORIAL.md) com a fila de artigos
programados e as [publicações de LinkedIn](.AGENTS/LINKEDIN_PUBLICACOES.md)
prontas para cada artigo.

## Identidade visual

Vem do sistema de marca da Clariô, em `~/Documentos/Clariô`:

- **Paleta** das cores da Festa de Agosto: vermelho `#A93B30` (Divino),
  ouro `#E3A22B` (sol), rosa `#C56F7F` (São Benedito), azul `#3F6E8C`
  (N. S. do Rosário), verde `#5E9086` (pena de pavão)
- **Tipografia**: Baloo 2 nos títulos, Nunito no texto, JetBrains Mono nos
  dados (CNPJ, telefone), todas SIL Open Font License
- **Emblema do catopê** como marca d'água da capa

O tema escuro não foi inventado: as cores saem do próprio `lockup-dark.svg`,
inclusive o fundo `#2A2018`, que é a cor da placa do lockup (assim ela
desaparece no cabeçalho).

### Linguagem: técnica sobre tradição

A ideia é instrumento de precisão, não material didático:

- **Mostrador**: o catopê no centro de um mostrador com anéis concêntricos,
  24 marcas de escala e 12 raios, desenhados por script. A geometria radial do
  emblema lida como instrumento.
- **Monoespaçada nos rótulos**: navegação, rótulos de seção, área dos produtos
  e todos os dados cadastrais. É a voz técnica do sistema.
- **Baloo 2 só no H1.** As demais chamadas usam Nunito 800 (a arredondada em
  toda parte puxava o visual para o didático).
- **Malha de pontos** na capa, cantos vivos, réguas de 1px, cartões numerados.

### Acessibilidade

Contraste conferido par a par. As cores vivas da marca não atingem 4.5:1 em
fundo claro quando usadas em texto pequeno, então há variantes escurecidas
(`--verde-txt`, `--rosa-txt`, `--ouro-txt`) só para texto: a cor viva
permanece na régua lateral dos cartões, onde é elemento gráfico e não texto.

Existe por um motivo concreto: a verificação de negócio da Meta (spec
[`F0-T01`](../amparo/specs/00-fase0/F0-T01-conta-meta-e-numero.md) do Amparo)
exige site institucional e e-mail no domínio da empresa.

## Antes de publicar

Os dados do cartão CNPJ já estão preenchidos. Conferir antes de qualquer
alteração: divergência entre o site e os documentos é a causa mais comum de
reprovação na verificação de negócio da Meta.

## Publicar na Cloudflare

O deploy usa **Workers Static Assets**: o caminho atual da Cloudflare para site
estático, que substituiu o Pages clássico em projetos novos.

Em `dash.cloudflare.com` → **Workers & Pages** → **Create** → conectar este
repositório, com:

| Campo | Valor |
|---|---|
| Project name | `clario-site` |
| Build command | *(vazio: não há build)* |
| Deploy command | `npx wrangler deploy` |

O `npx wrangler deploy` lê o `wrangler.jsonc`, que aponta para `public/`. Cada
push na `main` publica sozinho.

Depois, em **Custom domains**, adicionar `clariosistemas.com.br` e `www`.

### Script automatizado de publicação

Para verificar o código, atualizar o blog, auditar conformidade, commitar, enviar para produção e acionar o IndexNow em um único comando:

```bash
./scripts/publicar.sh "Descrição concisa da alteração"
```

Opções disponíveis:
- `./scripts/publicar.sh --check-only`: executa as validações e auditorias sem commitar ou enviar ao repositório remoto.
- `./scripts/publicar.sh --no-indexnow "Mensagem"`: publica em produção sem enviar ping ao IndexNow.

### Publicar diretamente via Wrangler (se configurado)

```bash
npx wrangler deploy
```

## IndexNow (Bing e outros buscadores)

O protocolo [IndexNow](https://www.indexnow.org) avisa imediatamente motores de busca (Bing, Yandex, Seznam, Naver) sobre atualizações nas URLs do site sem esperar a próxima varredura.

1. **Chave de API**: O arquivo `public/bcfc4849079645379c75ca0288a62c1e.txt` é servido na raiz do domínio (`https://clariosistemas.com.br/bcfc4849079645379c75ca0288a62c1e.txt`) para validar a titularidade.
2. **Submissão manual**: Após publicar as alterações, execute:
   ```bash
   ./scripts/indexnow.sh
   ```
   Ou envie uma URL específica:
   ```bash
   ./scripts/indexnow.sh https://clariosistemas.com.br/
   ```
3. **Automação no Cloudflare (opcional)**: No painel da Cloudflare (`dash.cloudflare.com` → domínio `clariosistemas.com.br` → **Speed** ou **Crawlers / SEO**), é possível habilitar a opção nativa de **IndexNow** para que a própria Cloudflare notifique os indexadores automaticamente ao purgar cache.

## Blog e Programação de Conteúdo

Os artigos do blog são escritos em Markdown na pasta `content/blog/` com metadados no cabeçalho (frontmatter).

### Como criar ou programar um artigo

Crie um arquivo `.md` em `content/blog/` com o padrão:

```yaml
---
title: Título do Artigo
slug: titulo-do-artigo
date: 2026-09-15
area: Engenharia de software
description: Descrição concisa para busca e meta tags.
read_time: 4 min
---

Conteúdo do artigo em Markdown...
```

* **Programação de publicação**: o campo `date` controla a liberação. Se a data for posterior ao dia atual, o artigo fica em estado programado (não é gerado para produção nem entra no sitemap até a data estipulada).
* **Construção estática e sitemap**: execute `python3 scripts/build_blog.py`. O script gera os arquivos HTML em `public/blog/`, cria a listagem em `public/blog/index.html` e regenera dinamicamente o `public/sitemap.xml` com todas as URLs ativas.
* **Feed RSS**: o mesmo comando gera `public/blog/feed.xml` com os artigos já publicados. A data de construção do feed acompanha o artigo mais recente, e não o instante do build, para não gerar diferença no Git a cada execução.
* **Submissão com IndexNow**: use `python3 scripts/build_blog.py --indexnow` ou execute `./scripts/indexnow.sh` para notificar Bing e IndexNow sobre os novos links.

## Alternativa: GitHub Pages

**Settings** → **Pages** → branch `main`, pasta `/public`. Também gratuito, com
HTTPS. Não usa o `wrangler.jsonc`.

## DNS no registro.br

Depois de registrar `clariosistemas.com.br`, aponte os servidores DNS para os
da Cloudflare (o painel deles informa quais). A partir daí, site e e-mail são
configurados pela Cloudflare, não pelo registro.br.

## E-mail: Zoho Mail (plano gratuito)

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
