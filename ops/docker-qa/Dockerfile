# Imagem de analise estatica do codigo do SEI, para uso local.
#
# Deriva da MESMA imagem do container httpd, entao o PHP tem exatamente as
# extensoes do runtime do SEI. Isso evita falso positivo em codigo protegido
# por extension_loaded().
#
# Esta variante nao depende de nada do pengovbr: a imagem e construida aqui.
# A imagem do httpd e construida pelo docker-compose.yml de ../docker-sei-localhost
# e precisa existir antes deste build.
ARG BASE_IMAGE=ops_sei-docker-httpd
FROM ${BASE_IMAGE}

# Composer da imagem oficial, baixada pelo Docker. O instalador baixado pelo PHP
# de dentro do build, em getcomposer.org, ja falhou com "certificate verify failed".
COPY --from=composer/composer:2.10.3-bin /composer /usr/local/bin/composer

# PHPStan, Psalm e PHPUnit do composer.json, nas versoes do composer.lock. Ficam
# fora de /qa porque o docker-compose.yml monta esta pasta em /qa, o que
# esconderia o vendor da imagem.
COPY composer.json composer.lock /usr/local/qa/
RUN composer install --working-dir=/usr/local/qa --no-interaction --no-progress

# A extensao zip do PHP precisa da libzip.so.5, que a imagem base guarda em
# /opt2/remi.tgz e normalmente expande em /opt. Aqui /opt recebe o codigo do SEI
# por volume e esconderia a biblioteca, entao expandimos fora de /opt.
RUN if [ -f /opt2/remi.tgz ]; then \
      mkdir -p /usr/local/remi && tar -xzf /opt2/remi.tgz -C /usr/local/remi; \
    fi
ENV LD_LIBRARY_PATH=/usr/local/remi/remi/libzip/lib64

# short_open_tag: boa parte dos arquivos do SEI abre com <?. Sem isso o Psalm
# le o arquivo como HTML e passa sem apontar nada, inclusive erro de sintaxe.
RUN printf 'short_open_tag = On\nmemory_limit = 2G\n' > /etc/php.d/qa.ini

WORKDIR /opt
