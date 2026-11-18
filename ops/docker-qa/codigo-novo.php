<?php
// Lista os arquivos alterados em relacao a base e deixa nos relatorios do PHPStan e do Psalm so os
// achados em linhas alteradas.
// Uso: php /qa/codigo-novo.php --lista   (arquivos alterados, relativos a fontes/sei/src/main/php)
//      php /qa/codigo-novo.php --phpstan-json|--psalm-json <relatorio> <saida>
$diff = '/qa/cache/alteracoes.diff';
$novos = '/qa/cache/novos.txt';
$prefixo = 'fontes/sei/src/main/php/';
if (!is_file($diff) || !is_file($novos)) {
    echo "Faltam as linhas alteradas. Rode pelo executar_analise_codigo_alterado.bat.\n";
    exit(2);
}

function lerDiff(string $caminho): array
{
    $linhas = [];
    $arquivo = null;
    foreach (file($caminho, FILE_IGNORE_NEW_LINES) as $l) {
        $l = rtrim($l, "\r");
        if (str_starts_with($l, '+++ ')) {
            $arquivo = $l === '+++ /dev/null' ? null : substr($l, 6);
        } elseif ($arquivo !== null && preg_match('/^@@ -\S+ \+(\d+)(?:,(\d+))? @@/', $l, $m)) {
            $fim = (int)$m[1] + (isset($m[2]) ? (int)$m[2] : 1);
            for ($n = (int)$m[1]; $n < $fim; $n++) {
                $linhas[$arquivo][$n] = true;
            }
        }
    }
    return $linhas;
}

$linhas = lerDiff($diff);
// Fica so o que tambem difere da base de hoje: mudanca que ja chegou la por outro commit nao conta.
$contraBase = '/qa/cache/alteracoes-base.diff';
if (is_file($contraBase)) {
    $base = lerDiff($contraBase);
    foreach ($linhas as $a => $numeros) {
        $linhas[$a] = array_intersect_key($numeros, $base[$a] ?? []);
        if (!$linhas[$a]) {
            unset($linhas[$a]);
        }
    }
}
$inteiros = [];
foreach (file($novos, FILE_IGNORE_NEW_LINES) as $l) {
    if (($l = rtrim($l, "\r")) !== '') {
        $inteiros[$l] = true;
    }
}

if (($argv[1] ?? '') === '--lista') {
    foreach (array_keys($linhas + $inteiros) as $a) {
        if (str_starts_with($a, $prefixo)) {
            echo substr($a, strlen($prefixo)), "\n";
        }
    }
    exit(0);
}

$ehNovo = function (string $caminho, int $n) use ($linhas, $inteiros): bool {
    $a = preg_replace('#^/src/#', 'fontes/sei/src/main/php/', $caminho);
    return isset($inteiros[$a]) || isset($linhas[$a][$n]);
};
$j = json_decode((string)@file_get_contents($argv[2] ?? ''), true);
if (!is_array($j)) {
    echo "Relatorio invalido ou ausente: " . ($argv[2] ?? '') . "\n";
    exit(1);
}
if (($argv[1] ?? '') === '--phpstan-json') {
    $total = 0;
    $fica = 0;
    foreach ($j['files'] ?? [] as $arq => $d) {
        $total += count($d['messages']);
        $d['messages'] = array_values(array_filter($d['messages'], fn($m) => $ehNovo($arq, (int)($m['line'] ?? 0))));
        $d['errors'] = count($d['messages']);
        $fica += $d['errors'];
        if ($d['messages']) {
            $j['files'][$arq] = $d;
        } else {
            unset($j['files'][$arq]);
        }
    }
    $j['files'] = $j['files'] ?: new stdClass();
    $j['totals']['file_errors'] = $fica;
    echo "    $fica achados em linhas alteradas, de $total nos arquivos alterados.\n";
} else {
    // Formato sonarqube do Psalm, com caminhos relativos a /src.
    $total = count($j['issues'] ?? []);
    $j['issues'] = array_values(array_filter($j['issues'] ?? [], fn($i) => $ehNovo('/src/' . $i['primaryLocation']['filePath'], (int)$i['primaryLocation']['textRange']['startLine'])));
    echo "    " . count($j['issues']) . " achados em linhas alteradas, de $total nos arquivos alterados.\n";
}
file_put_contents($argv[3], json_encode($j, JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE));
