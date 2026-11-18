#!/bin/sh
# Deixa o SonarQube local igual ao da Anatel: modo Standard, gate SEI com as mesmas 3 condicoes (confiabilidade mais rigida),
# perfis *-SEI e projeto sei-local. Gera o token do scanner em /sonar/token.local.
# Roda no container qa, pelo iniciar_ambiente_qa.bat, so na primeira vez.
L="${SONAR_LOCAL:-http://sonarqube:9000}"
A="${SONAR_ADMIN:-admin:admin}"
D="$(dirname "$0")"
c() { curl -s -u "$A" "$@"; }

echo "Aguardando o SonarQube local subir..."
until curl -s "$L/api/system/status" | grep -q '"UP"'; do sleep 5; done

echo "Modo Standard..."
c -X PATCH "$L/api/v2/clean-code-policy/mode" -H "Content-Type: application/merge-patch+json" \
  -d '{"mode":"STANDARD_EXPERIENCE"}' >/dev/null

echo "Gate SEI..."
c "$L/api/qualitygates/show?name=SEI" | grep -q '"name":"SEI"' || c -X POST "$L/api/qualitygates/create" -d "name=SEI" >/dev/null
# O Sonar cria o gate com condicoes padrao a mais. Fica so o que o servidor da Anatel tem.
c "$L/api/qualitygates/show?name=SEI" | tr '{' '\n' | grep '"metric"' | while read -r linha; do
  m=$(echo "$linha" | sed -n 's/.*"metric":"\([^"]*\)".*/\1/p')
  id=$(echo "$linha" | sed -n 's/.*"id":"\([^"]*\)".*/\1/p')
  case "$m" in
    new_blocker_violations|new_reliability_rating|new_security_rating) ;;
    *) c -X POST "$L/api/qualitygates/delete_condition" -d "id=$id" >/dev/null ;;
  esac
done
# Unica diferenca para a Anatel: confiabilidade GT 3 (la e 4), para BUG CRITICAL tambem reprovar.
for cond in new_blocker_violations:GT:0 new_reliability_rating:GT:3 new_security_rating:GT:1; do
  m=${cond%%:*}; r=${cond#*:}; o=${r%%:*}; e=${r#*:}
  id=$(c "$L/api/qualitygates/show?name=SEI" | tr '{' '\n' | grep "\"metric\":\"$m\"" | sed -n 's/.*"id":"\([^"]*\)".*/\1/p')
  if [ -n "$id" ]; then
    c -X POST "$L/api/qualitygates/update_condition" -d "id=$id&metric=$m&op=$o&error=$e" >/dev/null
  else
    c -X POST "$L/api/qualitygates/create_condition" -d "gateName=SEI&metric=$m&op=$o&error=$e" >/dev/null
  fi
done

echo "Projeto sei-local..."
c "$L/api/projects/search?projects=sei-local" | grep -q '"key":"sei-local"' || \
  c -X POST "$L/api/projects/create" -d "project=sei-local&name=SEI local&visibility=private" >/dev/null
c -X POST "$L/api/qualitygates/select" -d "gateName=SEI&projectKey=sei-local" >/dev/null
# Com "versao anterior", um bug que ja estava na analise do commit anterior deixa de ser novo e o gate passa.
c -X POST "$L/api/new_code_periods/set" -d "project=sei-local&type=NUMBER_OF_DAYS&value=30" >/dev/null

echo "Perfis *-SEI..."
for f in "$D"/perfis/*.xml; do
  lang=$(grep -o '<language>[^<]*</language>' "$f" | head -1 | sed 's/<[^>]*>//g')
  nome=$(grep -o '<name>[^<]*</name>' "$f" | head -1 | sed 's/<[^>]*>//g')
  c -X POST "$L/api/qualityprofiles/restore" -F "backup=@$f" >/dev/null
  c -X POST "$L/api/qualityprofiles/add_project" --data-urlencode "language=$lang" \
    --data-urlencode "qualityProfile=$nome" --data-urlencode "project=sei-local" >/dev/null
  echo "  $nome ($lang)"
done

echo "Token do scanner..."
if [ -s "$D/token.local" ] && printf 'user = "%s:"\n' "$(cat "$D/token.local")" | curl -s -K - "$L/api/authentication/validate" | grep -q '"valid":true'; then
  echo "  token existente continua valido"
else
  c -X POST "$L/api/user_tokens/revoke" -d "name=scanner-local" >/dev/null
  c -X POST "$L/api/user_tokens/generate" -d "name=scanner-local&type=GLOBAL_ANALYSIS_TOKEN" \
    | sed -n 's/.*"token":"\([^"]*\)".*/\1/p' > "$D/token.local"
  [ -s "$D/token.local" ] && echo "  token novo gerado" || { echo "  FALHA ao gerar o token"; rm -f "$D/token.local"; exit 1; }
fi
echo "Pronto."
