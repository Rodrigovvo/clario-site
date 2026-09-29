#!/usr/bin/env python3
"""
scripts/gerar_og_image.py
Gera o cartão de compartilhamento social (og:image) em 1200x630 px.
Usa as cores oficiais da Clariô no tema escuro (#2A2018), a malha de pontos,
o lockup institucional e o mostrador com o catopê como instrumento.
"""

import os
import base64
import subprocess
import tempfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PNG = os.path.join(ROOT_DIR, "public", "marca", "compartilhamento.png")

def to_base64(filepath, mime="image/svg+xml"):
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def main():
    fonts_dir = os.path.join(ROOT_DIR, "public", "fonts")
    marca_dir = os.path.join(ROOT_DIR, "public", "marca")

    font_baloo = to_base64(os.path.join(fonts_dir, "baloo2-latin.woff2"), "font/woff2")
    font_nunito = to_base64(os.path.join(fonts_dir, "nunito-latin.woff2"), "font/woff2")
    font_mono = to_base64(os.path.join(fonts_dir, "jetbrainsmono-latin.woff2"), "font/woff2")

    lockup_svg = to_base64(os.path.join(marca_dir, "lockup-dark.svg"), "image/svg+xml")
    catope_svg = to_base64(os.path.join(marca_dir, "catope.svg"), "image/svg+xml")

    html_content = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<style>
@font-face {{
  font-family: 'Baloo 2';
  font-style: normal;
  font-weight: 700 800;
  src: url('{font_baloo}') format('woff2');
}}
@font-face {{
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 400 600 700 800;
  src: url('{font_nunito}') format('woff2');
}}
@font-face {{
  font-family: 'JetBrains Mono';
  font-style: normal;
  font-weight: 500 700;
  src: url('{font_mono}') format('woff2');
}}

:root {{
  --fundo: #2A2018;
  --linha: #453729;
  --linha-forte: #584937;
  --texto: #F0E6D2;
  --suave: #C9BFA8;
  --tenue: #A2957E;
  --ouro: #E3A22B;
  --vermelho: #A93B30;
  --azul: #8FB8CE;
  --verde: #8FBBB0;
  --superficie: #342A20;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  width: 1200px;
  height: 630px;
  overflow: hidden;
  background-color: var(--fundo);
  background-image: radial-gradient(circle at 1px 1px, var(--linha-forte) 1.2px, transparent 0);
  background-size: 26px 26px;
  color: var(--texto);
  font-family: 'Nunito', system-ui, sans-serif;
  display: flex;
  position: relative;
}}

/* Borda sutil de enquadramento do cartão */
.moldura {{
  position: absolute;
  inset: 20px;
  border: 1px solid var(--linha-forte);
  border-radius: 8px;
  pointer-events: none;
  z-index: 10;
}}

.conteudo {{
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  padding: 60px 80px;
}}

/* Coluna esquerda */
.col-info {{
  max-width: 630px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}}

.lockup {{
  width: 320px;
  height: auto;
  margin-bottom: 34px;
}}

.chamada {{
  font-family: 'Baloo 2', sans-serif;
  font-size: 44px;
  font-weight: 800;
  line-height: 1.12;
  color: var(--texto);
  margin-bottom: 20px;
  letter-spacing: -0.01em;
}}

.chamada em {{
  font-style: normal;
  color: var(--ouro);
}}

.descricao {{
  font-size: 20px;
  line-height: 1.5;
  color: var(--suave);
  margin-bottom: 32px;
}}

.tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}}

.tag {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: 0.05em;
  color: var(--texto);
  background: var(--superficie);
  border: 1px solid var(--linha-forte);
  padding: 8px 16px;
  border-radius: 4px;
}}

.tag-destaque {{
  color: var(--ouro);
  border-color: rgba(227, 162, 43, 0.45);
  background: rgba(227, 162, 43, 0.08);
}}

/* Coluna direita: mostrador */
.col-mostrador {{
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}}

.mostrador {{
  position: relative;
  width: 370px;
  height: 370px;
}}

.mostrador svg {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}}

.mostrador img {{
  position: absolute;
  inset: 29%;
  width: 42%;
  height: 42%;
}}

/* Rodapé técnico sutil na base */
.rodape-base {{
  position: absolute;
  bottom: 36px;
  left: 80px;
  display: flex;
  align-items: center;
  gap: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--tenue);
  letter-spacing: 0.04em;
}}

.ponto {{
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--linha-forte);
}}
</style>
</head>
<body>
<div class="moldura"></div>
<div class="conteudo">
  <div class="col-info">
    <img src="{lockup_svg}" alt="Clariô Sistemas Inteligentes" class="lockup">
    <h1 class="chamada">Tecnologia com <em>raiz</em>,<br>software com propósito.</h1>
    <p class="descricao">
      Sistemas sob medida e inteligência artificial aplicada desenhados para a rotina real de quem opera na ponta.
    </p>
    <div class="tags">
      <span class="tag tag-destaque">clariosistemas.com.br</span>
      <span class="tag">Software sob Medida</span>
      <span class="tag">Inteligência Artificial</span>
    </div>
  </div>

  <div class="col-mostrador">
    <div class="mostrador">
      <svg viewBox="0 0 400 400" fill="none">
        <g stroke="var(--linha-forte)" stroke-width="1.2">
          <circle cx="200" cy="200" r="196"/>
          <circle cx="200" cy="200" r="164"/>
          <circle cx="200" cy="200" r="118" stroke-dasharray="3 7"/>
          <circle cx="200" cy="200" r="92"/>
        </g>
        <g stroke="var(--ouro)" stroke-width="1.8" opacity=".85" id="ticks"></g>
        <g stroke="var(--vermelho)" stroke-width="1.2" opacity=".55" id="raios"></g>
      </svg>
      <img src="{catope_svg}" alt="">
    </div>
  </div>
</div>

<div class="rodape-base">
  <span>Montes Claros • MG</span>
  <span class="ponto"></span>
  <span>CNPJ 68.569.828/0001-07</span>
</div>

<script>
const svgns = 'http://www.w3.org/2000/svg';
const pol = (r, a) => [200 + r * Math.cos(a), 200 + r * Math.sin(a)];
const ticks = document.getElementById('ticks');
const raios = document.getElementById('raios');
if (ticks) {{
  for (let i = 0; i < 24; i++) {{
    const a = (i / 24) * Math.PI * 2 - Math.PI / 2;
    const longo = i % 6 === 0;
    const [x1, y1] = pol(longo ? 144 : 155, a);
    const [x2, y2] = pol(164, a);
    const l = document.createElementNS(svgns, 'line');
    l.setAttribute('x1', x1); l.setAttribute('y1', y1);
    l.setAttribute('x2', x2); l.setAttribute('y2', y2);
    ticks.appendChild(l);
  }}
  for (let i = 0; i < 12; i++) {{
    const a = (i / 12) * Math.PI * 2 - Math.PI / 2 + Math.PI / 12;
    const [x1, y1] = pol(94, a);
    const [x2, y2] = pol(196, a);
    const l = document.createElementNS(svgns, 'line');
    l.setAttribute('x1', x1); l.setAttribute('y1', y1);
    l.setAttribute('x2', x2); l.setAttribute('y2', y2);
    raios.appendChild(l);
  }}
}}
</script>
</body>
</html>
"""

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html_content)
        tmp_path = tmp.name

    try:
        cmd = [
            "google-chrome-stable",
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1200,630",
            f"--screenshot={OUTPUT_PNG}",
            f"file://{tmp_path}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Erro ao renderizar screenshot com Chrome: {res.stderr}")
            return False
        print(f"Cartão de compartilhamento gerado com sucesso: {OUTPUT_PNG}")
        return True
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    main()
