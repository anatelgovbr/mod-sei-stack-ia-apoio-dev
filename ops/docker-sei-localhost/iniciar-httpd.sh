#!/usr/bin/env bash
set -euo pipefail

probe=''
trap 'if [[ -n "$probe" ]]; then rm -f -- "$probe"; fi' EXIT

# O bind mount do Windows pode atribuir ao arquivo um UID diferente do criador.
uid_upload=''
for dir in /opt/sei/temp /opt/sip/temp; do
    mkdir -p -- "$dir"
    chmod 0777 "$dir"
    probe=$(runuser -u apache -- mktemp "$dir/.ops-upload-XXXXXX")
    uid_arquivo=$(stat -c '%u' "$probe")
    rm -- "$probe"
    probe=''

    if [[ -n "$uid_upload" && "$uid_upload" != "$uid_arquivo" ]]; then
        echo "Erro: as pastas temp do SEI e SIP atribuem UIDs diferentes aos uploads." >&2
        exit 1
    fi
    uid_upload="$uid_arquivo"
done

if [[ "$uid_upload" != "$(id -u apache)" ]]; then
    if [[ "$uid_upload" == 0 ]]; then
        echo "Erro: o bind mount atribui UID 0 aos uploads. Use o Podman rootful conforme ops/README.md." >&2
        exit 1
    fi
    usermod -u "$uid_upload" apache
    echo "Upload: UID do apache ajustado para $uid_upload, conforme os arquivos no bind mount."
fi

for dir in /opt/sei/temp /opt/sip/temp; do
    probe=$(runuser -u apache -- mktemp "$dir/.ops-upload-XXXXXX")
    runuser -u apache -- chmod 0660 "$probe"
    rm -- "$probe"
    probe=''
done

exec /command.sh
