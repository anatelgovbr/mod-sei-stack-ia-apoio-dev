# Imagem de desenvolvimento do SEI: a base oficial do projeto mais as bibliotecas
# que o modulo Correios precisa para ler o PDF do AR e extrair o codigo de barras.
# Antes eram instaladas na mao, com docker exec, a cada recriacao do container.
#
# BASE_IMAGE vem do docker-compose.yml, montado com as variaveis do .env. Nao ha
# valor padrao de proposito: APP_IMAGE e ENVIRONMENT_VERSION mudam conforme o
# ambiente (sei4/sei5), e um padrao fixo aqui construiria sobre a base errada.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# PHP 8.2.35 ou superior: corrige CVE-2026-109618 e CVE-2026-109619 (php.net,
# 21/10/2026). A base do PEN nao fixa o patch do PHP; o update traz o 8.2.x mais
# novo do remi e o teste derruba o build se a versao ficar abaixo do minimo.
RUN dnf update -y 'php*' \
 && dnf clean all && rm -rf /var/cache/dnf \
 && php -r 'exit(version_compare(PHP_VERSION, "8.2.35", ">=") ? 0 : 1);'

# ImageMagick rasteriza a pagina do PDF e o zbar le o codigo de barras. Ver
# MdCorRetornoArRN. O php-pecl-imagick do remi traz a extensao, o ImageMagick 7
# e o 40-imagick.ini.
RUN dnf install -y php-pecl-imagick zbar \
 && dnf clean all \
 && rm -rf /var/cache/dnf

# Defensivo: hoje o policy.xml nao bloqueia PDF e este sed nao altera nada, mas
# uma atualizacao do ImageMagick pode voltar a bloquear o coder.
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-7/policy.xml

# Silencia o aviso de ServerName do Apache na inicializacao.
RUN echo 'ServerName localhost' >> /etc/httpd/conf/httpd.conf

# O Xdebug descobre o IDE so pelo endereco de origem da requisicao. O cabecalho X-Forwarded-For,
# que o padrao tambem le, deixaria a requisicao desviar a sessao de depuracao para outro endereco.
RUN echo 'xdebug.client_discovery_header=REMOTE_ADDR' > /etc/php.d/99-xdebug-descoberta.ini
