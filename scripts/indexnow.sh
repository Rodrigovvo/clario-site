#!/usr/bin/env bash
#
# scripts/indexnow.sh
# Submete URLs do site Clariô para o Bing e outros motores de busca via protocolo IndexNow.
# Lê automaticamente todas as URLs ativas do public/sitemap.xml por padrão.
#

set -euo pipefail

HOST="clariosistemas.com.br"
KEY="bcfc4849079645379c75ca0288a62c1e"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
SITEMAP_FILE="public/sitemap.xml"

echo "=== IndexNow: Notificação para Bing e IndexNow ==="
echo "Host:         ${HOST}"
echo "Key:          ${KEY}"
echo "Key Location: ${KEY_LOCATION}"

if [ -n "${1:-}" ]; then
  URL_ARRAY="[\"$1\"]"
  echo "Submetendo URL única: $1"
else
  if [ -f "${SITEMAP_FILE}" ]; then
    URL_LIST=$(grep -o '<loc>[^<]*</loc>' "${SITEMAP_FILE}" | sed 's/<loc>/"/;s/<\/loc>/"/' | paste -sd, -)
    URL_ARRAY="[${URL_LIST}]"
    echo "Submetendo todas as URLs do sitemap (${SITEMAP_FILE}):"
    grep -o '<loc>[^<]*</loc>' "${SITEMAP_FILE}" | sed 's/<\/\?loc>//g' | sed 's/^/  * /'
  else
    URL_ARRAY="[\"https://${HOST}/\"]"
    echo "Submetendo: https://${HOST}/"
  fi
fi
echo ""

PAYLOAD=$(cat <<EOF
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "${KEY_LOCATION}",
  "urlList": ${URL_ARRAY}
}
EOF
)

for ENDPOINT in "https://api.indexnow.org/indexnow" "https://www.bing.com/indexnow"; do
  echo -n "Enviando para ${ENDPOINT}... "
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d "${PAYLOAD}")

  case "${HTTP_CODE}" in
    200)
      echo "OK (${HTTP_CODE}): URLs enviadas com sucesso."
      ;;
    202)
      echo "Aceito (${HTTP_CODE}): URLs recebidas, validação da chave em andamento."
      ;;
    400)
      echo "Erro (${HTTP_CODE}): Formato inválido."
      ;;
    403)
      echo "Aviso (${HTTP_CODE}): Chave não validada (certifique-se de que ${KEY_LOCATION} já está publicado e acessível)."
      ;;
    422)
      echo "Erro (${HTTP_CODE}): Uma ou mais URLs não pertencem ao domínio informado."
      ;;
    429)
      echo "Aviso (${HTTP_CODE}): Muitas requisições (rate limit)."
      ;;
    *)
      echo "Resposta HTTP: ${HTTP_CODE}"
      ;;
  esac
done

echo ""
echo "Concluído com sucesso!"
