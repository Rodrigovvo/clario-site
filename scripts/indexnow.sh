#!/usr/bin/env bash
#
# scripts/indexnow.sh
# Submete URLs do site Clariô para o Bing e outros motores de busca via protocolo IndexNow.
#

set -euo pipefail

HOST="clariosistemas.com.br"
KEY="bcfc4849079645379c75ca0288a62c1e"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
URL_TO_SUBMIT="${1:-https://${HOST}/}"

echo "=== IndexNow: Notificação para Bing / IndexNow ==="
echo "Host:         ${HOST}"
echo "Key:          ${KEY}"
echo "Key Location: ${KEY_LOCATION}"
echo "Submetendo:   ${URL_TO_SUBMIT}"
echo ""

PAYLOAD=$(cat <<EOF
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "${KEY_LOCATION}",
  "urlList": [
    "${URL_TO_SUBMIT}"
  ]
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
      echo "OK (${HTTP_CODE}) — URL enviada com sucesso."
      ;;
    202)
      echo "Aceito (${HTTP_CODE}) — URL recebida, validação da chave em andamento."
      ;;
    400)
      echo "Erro (${HTTP_CODE}) — Formato inválido."
      ;;
    403)
      echo "Aviso (${HTTP_CODE}) — Chave não validada (certifique-se de que ${KEY_LOCATION} já está publicado e acessível)."
      ;;
    422)
      echo "Erro (${HTTP_CODE}) — O URL não pertence ao domínio informado."
      ;;
    429)
      echo "Aviso (${HTTP_CODE}) — Muitas requisições (rate limit)."
      ;;
    *)
      echo "Resposta HTTP: ${HTTP_CODE}"
      ;;
  esac
done

echo ""
echo "Concluído!"
