#!/bin/sh
# Envia os arquivos alterados e os relatorios ao SonarQube local e espera o resultado do Quality Gate.
# Roda no container scanner, pelo executar_analise_codigo_alterado.bat. VERSAO traz o SHA curto do commit.
until curl -s http://sonarqube:9000/api/system/status | grep -q '"UP"'; do
  echo "Aguardando o SonarQube local subir..."; sleep 5
done
# O token vai pelo ambiente e pela entrada do curl, fora da linha de comando, que outro processo consegue ler.
export SONAR_TOKEN="$(cat /sonar/token.local)"
# A primeira analise de um projeto nao tem codigo novo e o gate passa sempre; antes dela vai uma analise vazia.
if printf 'user = "%s:"\n' "$SONAR_TOKEN" | curl -s -K - "http://sonarqube:9000/api/qualitygates/project_status?projectKey=sei-local" \
  | grep -q '"status":"NONE"'; then
  echo "Primeira analise do projeto: enviando antes a linha de base, vazia..."
  sonar-scanner -Dproject.settings=/sonar/sonar-project.properties \
    -Dsonar.sources="$(paste -sd, /relatorios/arquivos.txt)" \
    -Dsonar.exclusions='**/*' \
    -Dsonar.php.phpstan.reportPaths= -Dsonar.php.psalm.reportPaths= \
    -Dsonar.projectVersion=linha-de-base > /tmp/linha-de-base.log 2>&1 \
    || { grep -E 'ERROR' /tmp/linha-de-base.log; exit 1; }
fi
sonar-scanner -Dproject.settings=/sonar/sonar-project.properties \
  -Dsonar.sources="$(paste -sd, /relatorios/arquivos.txt)" \
  -Dsonar.projectVersion="${VERSAO:-local}" \
  -Dsonar.qualitygate.wait=true > /tmp/scanner.log 2>&1
s=$?
grep -E 'QUALITY GATE STATUS|EXECUTION|ERROR' /tmp/scanner.log
exit $s
