#!/usr/bin/env python3
"""
scripts/build_blog.py
Gera as páginas estáticas do Blog da Clariô, atualiza o sitemap.xml dinamicamente
e suporta submissão ao IndexNow (Bing).

Otimizado para SEO, GEO (Generative Engine Optimization) e AGO (Answer/Agent Engine Optimization).
Suporta programação de conteúdo: posts com data futura são ignorados no build de produção
até a data estipulada no frontmatter.
"""

import os
import sys
import glob
import re
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
import markdown

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONTENT_DIR = os.path.join(ROOT_DIR, "content", "blog")
OUTPUT_DIR = os.path.join(ROOT_DIR, "public", "blog")
SITEMAP_PATH = os.path.join(ROOT_DIR, "public", "sitemap.xml")
SITE_URL = "https://clariosistemas.com.br"
INDEXNOW_KEY = "bcfc4849079645379c75ca0288a62c1e"
INDEXNOW_KEY_LOCATION = f"{SITE_URL}/{INDEXNOW_KEY}.txt"

TZ_BRT = timezone(timedelta(hours=-3))

MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}

def format_date(dt_str):
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d")
        return f"{dt.day} de {MESES[dt.month]} de {dt.year}"
    except Exception:
        return dt_str

def parse_markdown_file(filepath):
    content = open(filepath, "r", encoding="utf-8").read()
    md = markdown.Markdown(extensions=["meta", "extra"])
    html_body = md.convert(content)
    meta = {}
    for k, v in md.Meta.items():
        meta[k] = v[0] if len(v) == 1 else v
    return meta, html_body

SHARED_HEAD = """
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/marca/catope.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script defer src="https://cloud.umami.is/script.js" data-website-id="7dbc2ed6-92e3-4324-8a5d-e9a11250e975" data-domains="clariosistemas.com.br,www.clariosistemas.com.br"></script>
<link rel="preload" href="/fonts/baloo2-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/nunito-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{font-family:'Baloo 2';font-style:normal;font-weight:400 800;font-display:swap;src:url('/fonts/baloo2-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Baloo 2';font-style:normal;font-weight:400 800;font-display:swap;src:url('/fonts/baloo2-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'Nunito';font-style:normal;font-weight:400 800;font-display:swap;src:url('/fonts/nunito-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Nunito';font-style:normal;font-weight:400 800;font-display:swap;src:url('/fonts/nunito-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:400 800;font-display:swap;src:url('/fonts/jetbrainsmono-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:400 800;font-display:swap;src:url('/fonts/jetbrainsmono-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
:root{
  --vermelho:#A93B30; --ouro:#E3A22B; --ouro-escuro:#C8811C;
  --rosa:#C56F7F; --azul:#3F6E8C; --verde:#5E9086;
  --tinta:#33261C; --creme:#ECDCB4; --papel:#F7F3E9;

  --texto:var(--tinta); --suave:#6E6656; --tenue:#7B7263;
  --azul-txt:#3F6E8C; --verde-txt:#517C73; --rosa-txt:#A75E6C; --ouro-txt:#A06716; --vermelho-txt:#A93B30;
  --fundo:#FCFBF7; --superficie:#fff; --faixa:var(--papel);
  --linha:#E6DFCE; --linha-forte:#D6CDB6;
  --titulo:var(--tinta); --marca:var(--vermelho); --link:var(--azul);

  --display:'Baloo 2',system-ui,sans-serif;
  --corpo:'Nunito',system-ui,-apple-system,'Segoe UI',sans-serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,monospace;
  --largura:70rem;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --texto:#F0E6D2; --suave:#C9BFA8; --tenue:#A2957E;
    --azul-txt:#8FB8CE; --verde-txt:#8FBBB0; --rosa-txt:#E0A0AC; --ouro-txt:#E3A22B; --vermelho-txt:#E58278;
    --fundo:#2A2018; --superficie:#342A20; --faixa:#241C15;
    --linha:#453729; --linha-forte:#584937;
    --titulo:#F0E6D2; --marca:var(--ouro); --link:#8FB8CE;
  }
}
:root[data-theme="dark"]{
  --texto:#F0E6D2; --suave:#C9BFA8; --tenue:#A2957E;
  --azul-txt:#8FB8CE; --verde-txt:#8FBBB0; --rosa-txt:#E0A0AC; --ouro-txt:#E3A22B; --vermelho-txt:#E58278;
  --fundo:#2A2018; --superficie:#342A20; --faixa:#241C15;
  --linha:#453729; --linha-forte:#584937;
  --titulo:#F0E6D2; --marca:var(--ouro); --link:#8FB8CE;
}

*{box-sizing:border-box}
body{margin:0; background:var(--fundo); color:var(--texto);
  font-family:var(--corpo); font-size:16.5px; line-height:1.62;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility}
h1,h2,h3{margin:0; line-height:1.18}
a{color:var(--link); text-underline-offset:.2em; text-decoration-thickness:1px}
.env{max-width:var(--largura); margin:0 auto; padding:0 2rem}
.env-artigo{max-width:46rem; margin:0 auto; padding:0 1.5rem}

.rotulo{font-family:var(--mono); font-size:.72rem; font-weight:500;
  letter-spacing:.14em; text-transform:uppercase; color:var(--tenue)}

/* Cabecalho */
header{position:sticky; top:0; z-index:20; background:var(--fundo);
  border-bottom:1px solid var(--linha)}
.barra{display:flex; align-items:center; justify-content:space-between;
  gap:1rem; padding:.75rem 0; flex-wrap:wrap}
.lockup{display:block; width:150px; height:54px;
  background:url("/marca/lockup.svg") left center/contain no-repeat}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]) .lockup{background-image:url("/marca/lockup-dark.svg")}
}
:root[data-theme="dark"] .lockup{background-image:url("/marca/lockup-dark.svg")}
nav{display:flex; gap:1.7rem}
nav a{font-family:var(--mono); font-size:.75rem; letter-spacing:.12em;
  text-transform:uppercase; color:var(--suave); text-decoration:none}
nav a:hover, nav a.ativo{color:var(--marca)}

/* Hero do Blog */
.capa-blog{padding:3.5rem 0 2.5rem; border-bottom:1px solid var(--linha);
  background:radial-gradient(circle at 1px 1px, var(--linha-forte) 1px, transparent 0) 0 0/26px 26px, var(--fundo)}
.capa-blog h1{font-family:var(--display); font-weight:700; font-size:clamp(1.9rem,3.6vw,2.5rem);
  color:var(--titulo); margin:.5rem 0 .4rem}
.capa-blog p{color:var(--suave); font-size:1.05rem; max-width:42rem; margin:0}

/* Lista de Artigos */
.secao-artigos{padding:3.2rem 0 4rem}
.grade-artigos{display:grid; gap:1.4rem; grid-template-columns:repeat(auto-fit, minmax(20rem, 1fr))}
.card-artigo{background:var(--superficie); border:1px solid var(--linha); border-radius:6px;
  padding:1.8rem; position:relative; display:flex; flex-direction:column; justify-content:space-between}
.card-artigo::before{content:""; position:absolute; left:0; top:0; width:3px; height:100%; background:var(--cor, var(--azul))}
.card-artigo .meta{display:flex; align-items:center; gap:.7rem; margin-bottom:.6rem; font-family:var(--mono); font-size:.72rem}
.card-artigo .categoria{color:var(--cor-txt, var(--azul-txt)); font-weight:600; text-transform:uppercase; letter-spacing:.08em}
.card-artigo .data{color:var(--tenue)}
.card-artigo h2{font-family:var(--corpo); font-weight:800; font-size:1.24rem; margin:0 0 .6rem; color:var(--titulo)}
.card-artigo h2 a{color:inherit; text-decoration:none}
.card-artigo h2 a:hover{color:var(--marca)}
.card-artigo p{margin:0 0 1.2rem; color:var(--suave); font-size:.95rem; line-height:1.55}
.card-artigo .ler{font-family:var(--mono); font-size:.78rem; font-weight:600; color:var(--link); text-decoration:none}

/* Ferramentas do Blog: Pesquisa e Paginacao */
.ferramentas-blog{margin-bottom:2.2rem; display:flex; flex-direction:column; gap:.8rem}
.busca-container{position:relative; width:100%}
.campo-busca{width:100%; padding:.85rem 1.1rem; padding-right:2.8rem;
  font-family:var(--corpo); font-size:1rem; color:var(--texto);
  background:var(--superficie); border:1px solid var(--linha-forte);
  border-radius:6px; outline:none; transition:border-color .15s ease, box-shadow .15s ease}
.campo-busca:focus{border-color:var(--marca); box-shadow:0 0 0 3px rgba(169, 59, 48, .12)}
.btn-limpar-busca{position:absolute; right:.75rem; top:50%; transform:translateY(-50%);
  background:none; border:none; font-size:1.3rem; color:var(--tenue); cursor:pointer;
  padding:.2rem .5rem; line-height:1; border-radius:4px}
.btn-limpar-busca:hover{color:var(--marca)}
.info-busca{display:flex; align-items:center; justify-content:space-between;
  font-family:var(--mono); font-size:.74rem; color:var(--tenue); letter-spacing:.04em}
.busca-vazia{text-align:center; padding:3.5rem 1.5rem; background:var(--superficie);
  border:1px dashed var(--linha-forte); border-radius:6px; margin:1rem 0 2rem}
.busca-vazia-titulo{font-family:var(--corpo); font-weight:800; font-size:1.2rem;
  color:var(--titulo); margin:0 0 .4rem}
.busca-vazia-sub{color:var(--suave); font-size:.95rem; margin:0}
.paginacao{display:flex; justify-content:center; align-items:center; gap:.4rem;
  margin-top:2.8rem; flex-wrap:wrap; font-family:var(--mono); font-size:.82rem}
.pag-btn{background:var(--superficie); border:1px solid var(--linha); color:var(--texto);
  padding:.5rem .95rem; border-radius:4px; cursor:pointer; font-family:var(--mono);
  font-size:.8rem; font-weight:600; text-decoration:none; transition:all .15s ease}
.pag-btn:hover:not(:disabled){border-color:var(--marca); color:var(--marca)}
.pag-btn:disabled{opacity:.35; cursor:not-allowed; border-color:var(--linha)}
.pag-numeros{display:flex; gap:.35rem; align-items:center}
.pag-num{background:var(--superficie); border:1px solid var(--linha); color:var(--texto);
  min-width:2.2rem; height:2.2rem; padding:0 .4rem; display:inline-flex; align-items:center;
  justify-content:center; border-radius:4px; cursor:pointer; font-family:var(--mono);
  font-size:.8rem; font-weight:600; text-decoration:none; transition:all .15s ease}
.pag-num:hover:not(.ativo){border-color:var(--marca); color:var(--marca)}
.pag-num.ativo{background:var(--marca); color:#fff; border-color:var(--marca); font-weight:700}
.pag-elipse{color:var(--tenue); padding:0 .2rem}

/* Cabecalho Compacto do Artigo Individual */
.artigo-cabecalho{padding:1.5rem 0 1.2rem; border-bottom:1px solid var(--linha)}
.artigo-topo{display:flex; align-items:center; gap:.55rem; font-family:var(--mono); font-size:.72rem; margin-bottom:.5rem; flex-wrap:wrap; color:var(--tenue)}
.artigo-topo .voltar-topo{color:var(--link); text-decoration:none; font-weight:600}
.artigo-topo .voltar-topo:hover{color:var(--marca)}
.artigo-topo .sep{color:var(--linha-forte)}
.artigo-topo .categoria{color:var(--marca); font-weight:600; text-transform:uppercase; letter-spacing:.08em}
.artigo-topo .data{color:var(--tenue)}
.artigo-topo .tempo{color:var(--suave)}
.artigo-cabecalho h1{font-family:var(--corpo); font-weight:800; font-size:clamp(1.55rem,2.9vw,2.05rem); color:var(--titulo); letter-spacing:-.015em; line-height:1.22; margin:0 0 .45rem}
.artigo-lead{font-size:1.02rem; color:var(--suave); line-height:1.52; margin:0}

/* Corpo do Artigo */
.artigo-corpo{padding:1.8rem 0 3.5rem; font-size:1.05rem; line-height:1.72; color:var(--texto)}
.artigo-corpo p{margin:0 0 1.35rem}
.artigo-corpo h2{font-family:var(--corpo); font-weight:800; font-size:1.32rem; color:var(--titulo); margin:2.1rem 0 .75rem; letter-spacing:-.01em}
.artigo-corpo h3{font-family:var(--corpo); font-weight:800; font-size:1.14rem; color:var(--titulo); margin:1.6rem 0 .5rem}
.artigo-corpo blockquote{margin:1.5rem 0; padding:.85rem 1.25rem; border-left:3px solid var(--marca); background:var(--faixa); border-radius:0 4px 4px 0}
.artigo-corpo blockquote p{margin:0; font-style:italic; color:var(--suave)}
.artigo-corpo ul, .artigo-corpo ol{margin:0 0 1.5rem; padding-left:1.4rem}
.artigo-corpo li{margin-bottom:.45rem}

.artigo-rodape{margin-top:2.8rem; padding-top:1.8rem; border-top:1px solid var(--linha)}
.box-autor{background:var(--superficie); border:1px solid var(--linha); border-radius:6px; padding:1.5rem 1.6rem; display:flex; flex-direction:column; gap:.7rem}
.box-autor .titulo{font-family:var(--mono); font-size:.72rem; letter-spacing:.1em; text-transform:uppercase; color:var(--tenue)}
.box-autor p{margin:0; font-size:.94rem; color:var(--suave)}
.box-autor .links{display:flex; gap:1.4rem; font-family:var(--mono); font-size:.78rem; font-weight:600; margin-top:.3rem; flex-wrap:wrap}
.voltar-blog{display:inline-block; margin-top:2rem; font-family:var(--mono); font-size:.82rem; color:var(--suave); text-decoration:none}
.voltar-blog:hover{color:var(--marca)}

/* Rodape Global */
footer{padding:2.2rem 0 3.2rem; color:var(--tenue); font-size:.82rem; font-family:var(--mono); letter-spacing:.02em; border-top:1px solid var(--linha)}
</style>
"""

HEADER_HTML = """
<header>
  <div class="env barra">
    <a href="/" aria-label="Clariô Sistemas Inteligentes">
      <span class="lockup" role="img" aria-label="Clariô Sistemas Inteligentes"></span>
    </a>
    <nav>
      <a href="/#produtos">Produtos</a>
      <a href="/blog/" class="ativo">Blog</a>
      <a href="/#empresa">Empresa</a>
      <a href="/#contato">Contato</a>
    </nav>
  </div>
</header>
"""

FOOTER_HTML = """
<footer>
  <div class="env">
    © <span id="ano">2026</span> CLARIO · Análise, Desenvolvimento de Software e Consultoria em TI LTDA · CNPJ 68.569.828/0001-07
  </div>
</footer>
<script>document.getElementById('ano').textContent = new Date().getFullYear();</script>
"""

CORES_CATEGORIA = [
    ("var(--azul)", "var(--azul-txt)"),
    ("var(--verde)", "var(--verde-txt)"),
    ("var(--ouro-escuro)", "var(--ouro-txt)"),
    ("var(--vermelho)", "var(--vermelho-txt)"),
    ("var(--rosa)", "var(--rosa-txt)")
]

def render_article_page(post, meta, html_body):
    title = meta.get("title", "Artigo")
    slug = meta.get("slug")
    date_str = meta.get("date", "")
    area = meta.get("area", "Tecnologia")
    description = meta.get("description", "")
    read_time = meta.get("read_time", "3 min")
    formatted_date = format_date(date_str)
    canonical_url = f"{SITE_URL}/blog/{slug}/"

    # Extracao de texto puro para o articleBody do schema (essencial para GEO e AGO)
    plain_text = re.sub(r'<[^>]+>', ' ', html_body)
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()

    custom_keywords = meta.get("keywords", "")
    if isinstance(custom_keywords, str) and custom_keywords:
        extra_kws = [k.strip() for k in custom_keywords.split(",") if k.strip()]
    elif isinstance(custom_keywords, list):
        extra_kws = [str(k).strip() for k in custom_keywords]
    else:
        extra_kws = []

    keywords_list = [
        area,
        "Clariô Sistemas Inteligentes",
        "inteligência artificial",
        "Montes Claros",
        "Norte de Minas",
        "desenvolvimento de software",
        "software sob medida",
        "IA industrial e empresarial",
        "engenharia de software",
        "tecnologia com proposito"
    ] + extra_kws
    keywords_list = list(dict.fromkeys(keywords_list))

    artigo_schema = {
        "@type": "TechArticle",
        "@id": f"{canonical_url}#artigo",
        "headline": title,
        "description": description,
        "articleBody": plain_text[:5000],
        "inLanguage": "pt-BR",
        "keywords": keywords_list,
        "about": [
            {"@type": "Thing", "name": "Inteligência Artificial"},
            {"@type": "Place", "name": "Montes Claros"}
        ],
        "datePublished": date_str,
        "dateModified": date_str,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        },
        "author": {
            "@type": "Organization",
            "name": "Clariô Sistemas Inteligentes",
            "url": SITE_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": "Clariô Sistemas Inteligentes",
            "url": SITE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/marca/catope.svg"
            },
            "email": "contato@clariosistemas.com.br",
            "telephone": "+5538920000181",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Curitiba",
                "addressRegion": "PR",
                "addressCountry": "BR"
            }
        }
    }

    trilha_schema = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": canonical_url}
        ]
    }

    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [artigo_schema, trilha_schema]
    }, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<title>{title} | Blog Clariô</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:type" content="article">
<meta property="article:published_time" content="{date_str}">
<meta property="article:section" content="{area}">
<meta property="og:site_name" content="Clariô Sistemas Inteligentes">
<meta property="og:locale" content="pt_BR">
<meta property="og:image" content="{SITE_URL}/apple-touch-icon.png">
<meta name="author" content="Clariô Sistemas Inteligentes">
<link rel="alternate" type="application/rss+xml" title="Blog da Clariô" href="{SITE_URL}/blog/feed.xml">
{SHARED_HEAD}
<script type="application/ld+json">
{schema_json}
</script>
</head>
<body>
{HEADER_HTML}

<main>
  <article>
    <header class="artigo-cabecalho">
      <div class="env-artigo">
        <div class="artigo-topo">
          <a href="/blog/" class="voltar-topo">&larr; Blog</a>
          <span class="sep">/</span>
          <span class="categoria">{area}</span>
          <span class="sep">&middot;</span>
          <span class="data">{formatted_date}</span>
          <span class="sep">&middot;</span>
          <span class="tempo">{read_time}</span>
        </div>
        <h1>{title}</h1>
        <p class="artigo-lead">{description}</p>
      </div>
    </header>

    <div class="env-artigo artigo-corpo">
      {html_body}

      <div class="artigo-rodape">
        <div class="box-autor">
          <span class="titulo">Sobre a Clariô</span>
          <p>
            Construímos produtos próprios e sistemas sob medida com rigor de engenharia
            e propósito prático. Curitiba/PR e Montes Claros/MG.
          </p>
          <div class="links">
            <a href="/#produtos">Conhecer produtos&nbsp;&rarr;</a>
            <a href="/#contato">Falar sobre um projeto&nbsp;&rarr;</a>
          </div>
        </div>

        <a class="voltar-blog" href="/blog/">&larr; Voltar para a lista de artigos</a>
      </div>
    </div>
  </article>
</main>

{FOOTER_HTML}
</body>
</html>
"""

def render_blog_index(published_posts):
    canonical_url = f"{SITE_URL}/blog/"
    cards_html = []
    
    def limpa_attr(s):
        return str(s).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

    for idx, p in enumerate(published_posts):
        m = p["meta"]
        title = m.get("title", "Sem título")
        slug = m.get("slug")
        date_str = m.get("date", "")
        formatted_date = format_date(date_str)
        area = m.get("area", "Geral")
        desc = m.get("description", "")
        cor, cor_txt = CORES_CATEGORIA[idx % len(CORES_CATEGORIA)]
        
        card = f"""
        <article class="card-artigo" style="--cor:{cor}; --cor-txt:{cor_txt}" data-titulo="{limpa_attr(title)}" data-categoria="{limpa_attr(area)}" data-descricao="{limpa_attr(desc)}">
          <div>
            <div class="meta">
              <span class="categoria">{area}</span>
              <span class="data">{formatted_date}</span>
            </div>
            <h2><a href="/blog/{slug}/">{title}</a></h2>
            <p>{desc}</p>
          </div>
          <div>
            <a class="ler" href="/blog/{slug}/">Ler artigo&nbsp;&rarr;</a>
          </div>
        </article>
        """
        cards_html.append(card)

    cards_str = "\n".join(cards_html)

    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": f"{canonical_url}#blog",
                "name": "Blog da Clariô Sistemas Inteligentes",
                "description": "Artigos sobre engenharia de software, arquitetura web, gestão pública e a rotina real de colocar sistemas em produção.",
                "url": canonical_url,
                "inLanguage": "pt-BR",
                "publisher": {
                    "@type": "Organization",
                    "name": "Clariô Sistemas Inteligentes",
                    "url": SITE_URL
                },
                "blogPost": [
                    {
                        "@type": "TechArticle",
                        "headline": p["meta"].get("title", ""),
                        "description": p["meta"].get("description", ""),
                        "datePublished": p["meta"].get("date", ""),
                        "url": f"{SITE_URL}/blog/{p['meta'].get('slug')}/"
                    } for p in published_posts
                ]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": canonical_url}
                ]
            }
        ]
    }, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<title>Blog | Clariô Sistemas Inteligentes</title>
<meta name="description" content="Artigos sobre engenharia de software, arquitetura web, produtos digitais e as lições práticas de colocar sistemas em produção.">
<link rel="canonical" href="{canonical_url}">
<meta property="og:title" content="Blog | Clariô Sistemas Inteligentes">
<meta property="og:description" content="Artigos sobre engenharia de software, arquitetura web e tecnologia com propósito.">
<meta property="og:url" content="{canonical_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Clariô Sistemas Inteligentes">
<meta property="og:locale" content="pt_BR">
<meta property="og:image" content="{SITE_URL}/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Blog da Clariô" href="{SITE_URL}/blog/feed.xml">
{SHARED_HEAD}
<script type="application/ld+json">
{schema_json}
</script>
</head>
<body>
{HEADER_HTML}

<main>
  <div class="capa-blog">
    <div class="env">
      <div class="rotulo">Publicações &middot; Engenharia e Prática</div>
      <h1>Tecnologia, produto e software com raiz.</h1>
      <p>
        Reflexões técnicas, decisões de arquitetura e a rotina real de quem projeta e coloca software em produção.
      </p>
    </div>
  </div>

  <section class="secao-artigos">
    <div class="env">
      <div class="ferramentas-blog">
        <div class="busca-container">
          <input type="text" id="campo-busca" class="campo-busca" placeholder="Buscar artigos por título, tema ou tecnologia..." autocomplete="off" spellcheck="false" aria-label="Buscar artigos no blog">
          <button type="button" id="btn-limpar-busca" class="btn-limpar-busca" aria-label="Limpar busca" style="display:none">&times;</button>
        </div>
        <div class="info-busca">
          <span id="contador-busca">Carregando artigos...</span>
          <span class="dica-busca">Filtro instantâneo</span>
        </div>
      </div>

      <div id="busca-vazia" class="busca-vazia" style="display:none">
        <p class="busca-vazia-titulo">Nenhum artigo encontrado</p>
        <p class="busca-vazia-sub">Tente outros termos ou limpe a busca para ver todas as publicações.</p>
      </div>

      <div class="grade-artigos" id="grade-artigos">
        {cards_str}
      </div>

      <nav class="paginacao" id="paginacao" aria-label="Paginação de artigos" style="display:none">
        <button type="button" class="pag-btn" id="pag-ant" aria-label="Página anterior">&larr; Anterior</button>
        <div class="pag-numeros" id="pag-numeros"></div>
        <button type="button" class="pag-btn" id="pag-prox" aria-label="Próxima página">Próxima &rarr;</button>
      </nav>
    </div>
  </section>
</main>

{FOOTER_HTML}

<script>
(function() {{
  var ITENS_POR_PAGINA = 6;
  var campoBusca = document.getElementById('campo-busca');
  var btnLimpar = document.getElementById('btn-limpar-busca');
  var contador = document.getElementById('contador-busca');
  var buscaVazia = document.getElementById('busca-vazia');
  var grade = document.getElementById('grade-artigos');
  var paginacao = document.getElementById('paginacao');
  var pagAnt = document.getElementById('pag-ant');
  var pagProx = document.getElementById('pag-prox');
  var pagNumeros = document.getElementById('pag-numeros');

  if (!grade) return;
  var cards = Array.prototype.slice.call(grade.querySelectorAll('.card-artigo'));
  if (!cards.length) return;

  function normalizar(s) {{
    return (s || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
  }}

  var dadosCards = cards.map(function(card) {{
    var t = normalizar(card.getAttribute('data-titulo') || '');
    var c = normalizar(card.getAttribute('data-categoria') || '');
    var d = normalizar(card.getAttribute('data-descricao') || '');
    return {{
      el: card,
      textoBusca: t + ' ' + c + ' ' + d
    }};
  }});

  var cardsFiltrados = dadosCards.slice();
  var paginaAtual = 1;

  function obterParams() {{
    var p = new URLSearchParams(window.location.search);
    return {{
      q: p.get('q') || '',
      p: parseInt(p.get('p'), 10) || 1
    }};
  }}

  function atualizarURL(q, pag) {{
    var p = new URLSearchParams();
    if (q) p.set('q', q);
    if (pag > 1) p.set('p', pag);
    var qs = p.toString();
    var novaUrl = window.location.pathname + (qs ? '?' + qs : '');
    window.history.replaceState(null, '', novaUrl);
  }}

  function renderizar() {{
    var totalItens = cardsFiltrados.length;
    var totalPaginas = Math.ceil(totalItens / ITENS_POR_PAGINA) || 1;
    if (paginaAtual > totalPaginas) paginaAtual = totalPaginas;
    if (paginaAtual < 1) paginaAtual = 1;

    var termo = campoBusca.value.trim();
    if (termo) {{
      contador.textContent = totalItens === 1 ? '1 artigo encontrado' : totalItens + ' artigos encontrados';
      btnLimpar.style.display = 'block';
    }} else {{
      contador.textContent = totalItens + ' artigos publicados';
      btnLimpar.style.display = 'none';
    }}

    if (totalItens === 0) {{
      buscaVazia.style.display = 'block';
      grade.style.display = 'none';
      paginacao.style.display = 'none';
      atualizarURL(termo, 1);
      return;
    }}

    buscaVazia.style.display = 'none';
    grade.style.display = 'grid';

    var inicio = (paginaAtual - 1) * ITENS_POR_PAGINA;
    var fim = inicio + ITENS_POR_PAGINA;

    dadosCards.forEach(function(item) {{
      item.el.style.display = 'none';
    }});

    cardsFiltrados.slice(inicio, fim).forEach(function(item) {{
      item.el.style.display = 'flex';
    }});

    if (totalPaginas <= 1) {{
      paginacao.style.display = 'none';
    }} else {{
      paginacao.style.display = 'flex';
      pagAnt.disabled = (paginaAtual === 1);
      pagProx.disabled = (paginaAtual === totalPaginas);

      pagNumeros.innerHTML = '';
      for (var i = 1; i <= totalPaginas; i++) {{
        (function(num) {{
          var btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'pag-num' + (num === paginaAtual ? ' ativo' : '');
          btn.textContent = num;
          btn.setAttribute('aria-label', 'Ir para a página ' + num);
          btn.addEventListener('click', function() {{
            irParaPagina(num);
          }});
          pagNumeros.appendChild(btn);
        }})(i);
      }}
    }}

    atualizarURL(termo, paginaAtual);
  }}

  function irParaPagina(pag) {{
    paginaAtual = pag;
    renderizar();
    var secao = document.querySelector('.secao-artigos');
    if (secao) {{
      secao.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
  }}

  function filtrar(termo) {{
    var normal = normalizar(termo);
    var tokens = normal.split(/\\s+/).filter(Boolean);
    if (!tokens.length) {{
      cardsFiltrados = dadosCards.slice();
    }} else {{
      cardsFiltrados = dadosCards.filter(function(item) {{
        return tokens.every(function(t) {{
          return item.textoBusca.indexOf(t) !== -1;
        }});
      }});
    }}
    paginaAtual = 1;
    renderizar();
  }}

  var debounceTimer = null;
  campoBusca.addEventListener('input', function() {{
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function() {{
      filtrar(campoBusca.value);
    }}, 100);
  }});

  campoBusca.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') {{
      campoBusca.value = '';
      filtrar('');
    }}
  }});

  btnLimpar.addEventListener('click', function() {{
    campoBusca.value = '';
    campoBusca.focus();
    filtrar('');
  }});

  pagAnt.addEventListener('click', function() {{
    if (paginaAtual > 1) irParaPagina(paginaAtual - 1);
  }});

  pagProx.addEventListener('click', function() {{
    var totalPaginas = Math.ceil(cardsFiltrados.length / ITENS_POR_PAGINA);
    if (paginaAtual < totalPaginas) irParaPagina(paginaAtual + 1);
  }});

  var inicial = obterParams();
  if (inicial.q) {{
    campoBusca.value = inicial.q;
    filtrar(inicial.q);
  }}
  if (inicial.p && inicial.p > 1) {{
    paginaAtual = inicial.p;
  }}
  renderizar();
}})();
</script>
</body>
</html>
"""

def generate_rss(published_posts):
    """Gera o feed RSS 2.0 do blog em public/blog/feed.xml."""
    def esc(txt):
        return (str(txt).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    # Usa a data do artigo mais recente, e nao o instante do build:
    # mantem o feed estavel entre builds sem alteracao de conteudo.
    if published_posts:
        mais_recente = max(p["post_date"] for p in published_posts)
        agora = datetime.combine(mais_recente, datetime.min.time(), TZ_BRT).strftime("%a, %d %b %Y %H:%M:%S %z")
    else:
        agora = datetime.now(TZ_BRT).strftime("%a, %d %b %Y %H:%M:%S %z")
    itens = []
    for p in published_posts:
        m = p["meta"]
        slug = m.get("slug")
        url = f"{SITE_URL}/blog/{slug}/"
        try:
            pub = datetime.strptime(m.get("date", ""), "%Y-%m-%d").replace(tzinfo=TZ_BRT)
            pub_str = pub.strftime("%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            pub_str = agora
        itens.append(f"""    <item>
      <title>{esc(m.get("title", ""))}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <description>{esc(m.get("description", ""))}</description>
      <category>{esc(m.get("area", "Tecnologia"))}</category>
      <pubDate>{pub_str}</pubDate>
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Blog da Clariô Sistemas Inteligentes</title>
    <link>{SITE_URL}/blog/</link>
    <atom:link href="{SITE_URL}/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Engenharia de software, arquitetura web e a rotina real de colocar sistemas em produção.</description>
    <language>pt-BR</language>
    <lastBuildDate>{agora}</lastBuildDate>
{chr(10).join(itens)}
  </channel>
</rss>
"""
    feed_path = os.path.join(OUTPUT_DIR, "feed.xml")
    with open(feed_path, "w", encoding="utf-8") as f:
        f.write(feed)
    print(f"  Gerado: public/blog/feed.xml ({len(itens)} itens)")


def generate_sitemap(published_posts, today_str):
    urls = [
        {"loc": f"{SITE_URL}/", "lastmod": today_str, "changefreq": "monthly", "priority": "1.0"},
        {"loc": f"{SITE_URL}/blog/", "lastmod": today_str, "changefreq": "weekly", "priority": "0.8"},
    ]

    for p in published_posts:
        m = p["meta"]
        slug = m.get("slug")
        date_str = m.get("date", today_str)
        urls.append({
            "loc": f"{SITE_URL}/blog/{slug}/",
            "lastmod": date_str,
            "changefreq": "monthly",
            "priority": "0.7"
        })

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for u in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{u['loc']}</loc>")
        xml_lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{u['priority']}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>\n")

    content = "\n".join(xml_lines)
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[Sitemap] Atualizado com {len(urls)} URLs em {SITEMAP_PATH}")
    return [u["loc"] for u in urls]

def submit_indexnow(urls):
    print(f"\n[IndexNow] Submetendo {len(urls)} URLs...")
    payload = json.dumps({
        "host": "clariosistemas.com.br",
        "key": INDEXNOW_KEY,
        "keyLocation": INDEXNOW_KEY_LOCATION,
        "urlList": urls
    }).encode("utf-8")

    endpoints = [
        "https://api.indexnow.org/indexnow",
        "https://www.bing.com/indexnow"
    ]

    for ep in endpoints:
        try:
            req = urllib.request.Request(
                ep,
                data=payload,
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                code = resp.getcode()
                print(f"  {ep}: HTTP {code} (Sucesso)")
        except urllib.error.HTTPError as e:
            print(f"  {ep}: HTTP {e.code} ({e.reason})")
        except Exception as e:
            print(f"  {ep}: Erro de conexao ({e})")

def main():
    include_future = "--future" in sys.argv or "--all" in sys.argv
    do_indexnow = "--indexnow" in sys.argv

    today = datetime.now(TZ_BRT).date()
    today_str = today.strftime("%Y-%m-%d")

    print(f"=== Construtor do Blog Clariô ===")
    print(f"Data de referência: {today_str} (Horário de Brasília)")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    md_files = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.md")))
    if not md_files:
        print(f"Nenhum arquivo encontrado em {CONTENT_DIR}")
        return

    published_posts = []
    scheduled_posts = []

    for f in md_files:
        meta, body = parse_markdown_file(f)
        date_str = meta.get("date", "9999-99-99")
        try:
            post_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            post_date = today

        post_data = {
            "file": f,
            "meta": meta,
            "body": body,
            "post_date": post_date
        }

        if post_date > today and not include_future:
            scheduled_posts.append(post_data)
            print(f"  [PROGRAMADO] {meta.get('title', f)} -> Publicação em {date_str}")
        else:
            published_posts.append(post_data)
            print(f"  [PUBLICADO]  {meta.get('title', f)} -> Data: {date_str}")

    # Ordenar publicados por data decrescente
    published_posts.sort(key=lambda x: x["post_date"], reverse=True)

    # Gerar pagina individual de cada post publicado
    for p in published_posts:
        slug = p["meta"].get("slug")
        if not slug:
            continue
        post_dir = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(post_dir, exist_ok=True)
        html = render_article_page(p, p["meta"], p["body"])
        out_file = os.path.join(post_dir, "index.html")
        with open(out_file, "w", encoding="utf-8") as out:
            out.write(html)
        print(f"  Gerado: public/blog/{slug}/index.html")

    # Gerar a pagina index do blog
    index_html = render_blog_index(published_posts)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as out:
        out.write(index_html)
    print("  Gerado: public/blog/index.html")

    # Gerar feed RSS
    generate_rss(published_posts)

    # Atualizar sitemap
    active_urls = generate_sitemap(published_posts, today_str)

    # Submissao IndexNow se solicitado
    if do_indexnow:
        submit_indexnow(active_urls)

    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main()
