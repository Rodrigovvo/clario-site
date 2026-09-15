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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700&family=Nunito:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
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

    keywords_list = [
        area,
        "Clariô Sistemas Inteligentes",
        "desenvolvimento de software",
        "software sob medida",
        "engenharia de software",
        "tecnologia com proposito"
    ]

    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "articleBody": plain_text[:5000],
        "inLanguage": "pt-BR",
        "keywords": keywords_list,
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
            }
        }
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
        <article class="card-artigo" style="--cor:{cor}; --cor-txt:{cor_txt}">
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
{SHARED_HEAD}
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
      <div class="grade-artigos">
        {cards_str}
      </div>
    </div>
  </section>
</main>

{FOOTER_HTML}
</body>
</html>
"""

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

    # Atualizar sitemap
    active_urls = generate_sitemap(published_posts, today_str)

    # Submissao IndexNow se solicitado
    if do_indexnow:
        submit_indexnow(active_urls)

    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main()
