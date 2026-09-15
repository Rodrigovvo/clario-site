#!/usr/bin/env bash
#
# scripts/publicar.sh
# Script automatizado de publicacao em producao da Clario.
# Executa verificacoes de conformidade, build do blog, commit, push,
# notificacao via IndexNow e validacao pos-deploy.
#
# Uso:
#   ./scripts/publicar.sh "Mensagem descritiva da alteracao"
#   ./scripts/publicar.sh --check-only
#   ./scripts/publicar.sh --no-indexnow "Mensagem"
#

set -euo pipefail

# Garante execucao a partir da raiz do projeto
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

CHECK_ONLY=false
SKIP_INDEXNOW=false
COMMIT_MSG=""

# Processamento de argumentos
for arg in "$@"; do
  case "$arg" in
    --check-only)
      CHECK_ONLY=true
      shift || true
      ;;
    --no-indexnow)
      SKIP_INDEXNOW=true
      shift || true
      ;;
    -h|--help)
      echo "Uso: $0 [OPCOES] [\"Mensagem de commit\"]"
      echo ""
      echo "Opcoes:"
      echo "  --check-only     Executa apenas as validacoes sem commitar ou publicar"
      echo "  --no-indexnow    Nao envia notificacoes para os indexadores"
      echo "  -h, --help       Exibe esta ajuda"
      exit 0
      ;;
    *)
      if [ -z "${COMMIT_MSG}" ]; then
        COMMIT_MSG="$arg"
      fi
      ;;
  esac
done

echo "=================================================="
echo "   Publicacao em Producao: Clario Sistemas"
echo "=================================================="
echo "Diretorio raiz: ${ROOT_DIR}"
echo ""

# --------------------------------------------------
# Passo 1: Construcao do Blog e Sitemap
# --------------------------------------------------
echo "[1/5] Construindo paginas do blog e gerando sitemap..."
python3 scripts/build_blog.py
echo "      Blog e sitemap atualizados com sucesso."
echo ""

# --------------------------------------------------
# Passo 2: Auditoria de Conformidade e Voz
# --------------------------------------------------
echo "[2/5] Executando auditoria de conformidade..."

python3 - << 'PY_AUDIT'
import os
import sys

errors = []

# 1. Verificacao de travessoes e emojis
def check_text_rules(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, 1):
            if "—" in line or "–" in line:
                errors.append(f"[TRAVESSAO] {path}:{idx}: {line.strip()}")
            for ch in line:
                cp = ord(ch)
                if (0x1F300 <= cp <= 0x1F9FF) or (0x2600 <= cp <= 0x27BF) or (0x1F600 <= cp <= 0x1F64F) or (0x1F680 <= cp <= 0x1F6FF) or (0x1FA70 <= cp <= 0x1FAFF):
                    errors.append(f"[EMOJI] {path}:{idx}: caractere U+{cp:04X}")
                    break

for folder in ["public", "content"]:
    if not os.path.exists(folder):
        continue
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith((".html", ".md", ".css", ".js", ".txt")):
                check_text_rules(os.path.join(root, file))

# 2. Verificacao de tracking do Umami
umami_files = ["public/index.html", "public/blog/index.html"]
if os.path.exists("public/blog"):
    for sub in os.listdir("public/blog"):
        article_html = os.path.join("public/blog", sub, "index.html")
        if os.path.isfile(article_html):
            umami_files.append(article_html)

for uf in umami_files:
    if os.path.isfile(uf):
        with open(uf, "r", encoding="utf-8") as f:
            html = f.read()
        if "cloud.umami.is/script.js" not in html or "7dbc2ed6-92e3-4324-8a5d-e9a11250e975" not in html:
            errors.append(f"[UMAMI] Script de tracking ausente em {uf}")

# 3. Verificacao de arquivos estruturais essenciais
required_files = [
    "public/sitemap.xml",
    "public/robots.txt",
    "public/favicon.ico",
    "public/apple-touch-icon.png",
    "public/bcfc4849079645379c75ca0288a62c1e.txt"
]
for rf in required_files:
    if not os.path.isfile(rf):
        errors.append(f"[ARQUIVO] Arquivo estrutural ausente: {rf}")

if errors:
    print("ERROS DE CONFORMIDADE ENCONTRADOS:")
    for err in errors:
        print("  *", err)
    sys.exit(1)
else:
    print("      Auditoria concluida: zero travessoes, zero emojis, tracking ativo e arquivos estruturais OK.")
PY_AUDIT

echo ""

if [ "${CHECK_ONLY}" = true ]; then
  echo "Modo --check-only finalizado com sucesso. Nenhuma publicacao realizada."
  exit 0
fi

# --------------------------------------------------
# Passo 3: Git Stage e Commit
# --------------------------------------------------
echo "[3/5] Preparando arquivos no controle de versao (Git)..."

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "${BRANCH}" != "main" ]; then
  echo "AVISO: Voce esta no ramo '${BRANCH}'. O deploy em producao ocorre a partir do ramo 'main'."
fi

# Adiciona arquivos modificados ou novos
git add .

# Verifica se ha diferencas para commit
if git diff --cached --quiet; then
  echo "      Nenhuma alteracao pendente para commit."
else
  if [ -z "${COMMIT_MSG}" ]; then
    if [ -t 0 ]; then
      echo -n "Digite a mensagem de commit: "
      read -r COMMIT_MSG
    fi
  fi

  if [ -z "${COMMIT_MSG}" ]; then
    COMMIT_MSG="Atualiza conteudo e publicacoes do site"
  fi

  # Valida se a propria mensagem de commit contem travessoes ou emojis
  if echo "${COMMIT_MSG}" | grep -qE "[—–]"; then
    echo "ERRO: A mensagem de commit contem travessao. Substitua por virgula, dois-pontos ou hifen simples."
    exit 1
  fi

  git commit -m "${COMMIT_MSG}"
  echo "      Commit realizado: ${COMMIT_MSG}"
fi
echo ""

# --------------------------------------------------
# Passo 4: Git Push para Producao
# --------------------------------------------------
echo "[4/5] Enviando alteracoes para os servidores remotos (push)..."
git push origin "${BRANCH}"
echo "      Push concluido com sucesso."
echo ""

# --------------------------------------------------
# Passo 5: IndexNow e Validacao em Producao
# --------------------------------------------------
echo "[5/5] Notificando motores de busca e validando producao..."

if [ "${SKIP_INDEXNOW}" = false ]; then
  if [ -f "scripts/indexnow.sh" ]; then
    bash scripts/indexnow.sh
  fi
else
  echo "      IndexNow ignorado (--no-indexnow)."
fi

echo ""
echo "Aguardando propagacao da borda Cloudflare (5 segundos)..."
sleep 5

PROD_URL="https://clariosistemas.com.br"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${PROD_URL}/" || true)

if [ "${HTTP_STATUS}" = "200" ]; then
  echo "      Status HTTP em producao: 200 OK (${PROD_URL})"
else
  echo "      Aviso: Codigo HTTP retornado por ${PROD_URL}: ${HTTP_STATUS}"
fi

echo ""
echo "=================================================="
echo "   Publicacao concluida com exito!"
echo "=================================================="
