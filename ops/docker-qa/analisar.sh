#!/bin/sh
# Roda PHPStan e Psalm nos arquivos alterados, a partir da copia do codigo no disco Linux (/src), e deixa
# nos relatorios so os achados em linhas alteradas. Roda no container qa, pelo executar_analise_codigo_alterado.bat.
# Sai com 3 quando nao ha arquivo alterado.
R=/qa/relatorios
mkdir -p "$R" && rm -f "$R"/*.json "$R"/*.txt

if [ ! -d /src/sei ]; then
  echo "  Primeira vez: copiando o codigo para o disco Linux do container, leva de 3 a 6 minutos..."
  cp -a /opt/. /src/
fi

# Arquivos alterados que ainda existem, copiados de novo para /src.
php /qa/codigo-novo.php --lista | while read -r a; do
  [ -f "/opt/$a" ] || continue
  mkdir -p "/src/$(dirname "$a")" && cp -p "/opt/$a" "/src/$a" && echo "$a"
done > "$R/arquivos.txt"
if [ ! -s "$R/arquivos.txt" ]; then
  echo "  Nenhum arquivo alterado."
  exit 3
fi
echo "  $(wc -l < "$R/arquivos.txt") arquivos alterados."

# PHPStan e Psalm olham o que o pipeline analisa: modulos e scripts, sem bibliotecas de terceiros.
grep -E '^(sei/web/modulos|sei/scripts|sip/scripts)/.*\.php$' "$R/arquivos.txt" | grep -v '/vendor/' | sed 's#^#/src/#' > "$R/php.txt"
cd /src
if [ -s "$R/php.txt" ]; then
  echo "  PHPStan em $(wc -l < "$R/php.txt") arquivos PHP..."
  php /usr/local/qa/vendor/bin/phpstan analyse -c /qa/phpstan.neon --error-format=json --no-progress --no-interaction \
    --memory-limit=2G $(cat "$R/php.txt") > "$R/phpstan-bruto.json" 2>/dev/null
  php /qa/codigo-novo.php --phpstan-json "$R/phpstan-bruto.json" "$R/phpstan.json" || exit 1
  echo "  Psalm..."
  php /usr/local/qa/vendor/bin/psalm --config=/qa/psalm.xml --no-progress --threads=1 --scan-threads=1 --ignore-baseline \
    --report="$R/psalm-bruto.sonarqube.json" $(cat "$R/php.txt") > /dev/null 2>&1
  php /qa/codigo-novo.php --psalm-json "$R/psalm-bruto.sonarqube.json" "$R/psalm.json" || exit 1
else
  echo "  Nenhum arquivo PHP alterado em modulos ou scripts. PHPStan e Psalm nao rodaram."
  printf '%s' '{"totals":{"errors":0,"file_errors":0},"files":{},"errors":[]}' > "$R/phpstan.json"
  printf '%s' '{"issues":[]}' > "$R/psalm.json"
fi
