#!/bin/sh
# Roda os testes unitarios de tests/unit, montada em /testes/unit, com o PHPUnit do qa/composer.json, instalado na imagem.
# Roda no container qa, pelo composer test. Opcoes do PHPUnit vao depois de --: composer test -- --filter X
exec php /usr/local/qa/vendor/bin/phpunit -c /testes/unit/phpunit.xml "$@"
