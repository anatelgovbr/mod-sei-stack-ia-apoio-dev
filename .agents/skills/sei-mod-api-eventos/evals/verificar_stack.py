"""Verifica contratos documentais; nao comprova eficacia de hooks em runtime."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / '.agents/skills/sei-mod-api-eventos/references/protecao-dependencias-core.md'

class StackDependenciasTest(unittest.TestCase):
    def test_acionamento_transversal(self):
        for file in ['AGENTS.md', '.agents/references/roteamento-de-skills.md', '.agents/skills/sei-guardrails-modulo/SKILL.md']:
            text = (ROOT / file).read_text(encoding='utf-8')
            self.assertIn('protecao-dependencias-core.md', text, file)
            self.assertRegex(text.lower(), r'protocolo', file)

    def test_encaminhamentos(self):
        for skill in ['sei-mod-api-eventos','sei-verificacao-banco-dados','sei-verificacao-rn','sei-gerador-crud','sei-gerador-scripts-release','sei-validacao-padrao','sei-revisao-tecnica']:
            path = ROOT / '.agents/skills' / skill / 'SKILL.md'
            self.assertIn('protecao-dependencias-core.md', path.read_text(encoding='utf-8'), skill)

    def test_template_simples(self):
        text = REF.read_text(encoding='utf-8')
        example = text.split('Exemplo de preenchimento:')[1].split('```text')[1].split('```')[0]
        self.assertIn('funcionalidade <funcionalidade>:\n\n   - <nome do tipo de documento 1>', example)
        self.assertNotIn('ID', example)
        self.assertNotIn('Utilização', example)

    def test_limites_obrigatorios(self):
        text = REF.read_text(encoding='utf-8')
        for term in ['configurarFK','antes do evento','DataProvider','concorrência','permissão','por módulo/evento','eliminação','rollback','caminho','histórico']:
            self.assertIn(term, text)

    def test_catalogo_sem_presuncao_pos_operacao(self):
        text = (REF.parent/'catalogo-eventos.md').read_text(encoding='utf-8')
        self.assertNotIn('parecem ser todos', text)
        for term in ['HipoteseLegalRN:300','VeiculoPublicacaoRN:446','DocumentoRN:1570','ProcedimentoRN:976','DocumentoAPI[]']:
            self.assertIn(term, text)

    def test_links_locais_das_skills_afetadas(self):
        skills = ['sei-mod-api-eventos','sei-guardrails-modulo','sei-verificacao-banco-dados','sei-verificacao-rn','sei-gerador-crud','sei-gerador-scripts-release','sei-validacao-padrao','sei-revisao-tecnica']
        paths = [ROOT/'.agents/skills'/s/'SKILL.md' for s in skills]+[REF,REF.parent/'catalogo-eventos.md']
        for path in paths:
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#'): continue
                target = link.split('#')[0]
                if '<' in target: continue
                self.assertTrue((path.parent/target).exists(), str(path)+': '+target)

    def test_evals_com_expectativas(self):
        data = json.loads((REF.parent.parent/'evals/evals.json').read_text(encoding='utf-8'))
        self.assertEqual(data['skill_name'], 'sei-mod-api-eventos')
        self.assertEqual(len(data['evals']), 4)
        self.assertEqual(len({c['id'] for c in data['evals']}), 4)
        for case in data['evals']:
            self.assertTrue(case['prompt'])
            self.assertGreaterEqual(len(case['expectations']), 3)


FONTES = ROOT / 'fontes/sei/src/main/php/sei/web'
SKILLS = ROOT / '.agents/skills'
CATALOGO_CLASSES = 'sei-mod-api-classes/references/catalogo-api.md'
CATALOGO_EVENTOS = 'sei-mod-api-eventos/references/catalogo-eventos.md'
CATALOGO_OPERACOES = 'sei-mod-api-operacoes/references/catalogo-operacoes.md'
# Classe que o manual 5.0 cita e o core nunca teve; o catalogo so a menciona na nota que corrige o manual.
SO_NO_MANUAL = {'RetornoInclusaoDocumentoAPI'}
# Palavras que descrevem valor ou origem dentro das listas de campos dos contratos, e nao campo.
VALORES_NOS_CONTRATOS = {'Restrito', 'Sigiloso', 'Opcional', 'Assinatura', 'Interno', 'Base64', 'IDs', 'Chamado'}


def catalogo(nome):
    return (SKILLS / nome).read_text(encoding='utf-8')


def eventos_do_core():
    return set(re.findall(r'public function (\w+)\s*\(', (FONTES / 'SeiIntegracao.php').read_text(encoding='latin-1')))


def atributos_das_classes_do_core():
    return {arquivo.stem: set(re.findall(r'private \$(\w+)', arquivo.read_text(encoding='latin-1'))) for arquivo in (FONTES / 'api').glob('*.php')}


def operacoes_do_core():
    texto = (FONTES / 'rn/SeiRN.php').read_text(encoding='latin-1')
    return {nome for nome in re.findall(r'protected function (\w+?)(?:Conectado|Controlado)\s*\(', texto) if not nome.endswith('Interno')}


def assinaturas_do_core():
    texto = (FONTES / 'SeiIntegracao.php').read_text(encoding='latin-1')
    return {f"public function {nome}({', '.join(p.strip() for p in parametros.split(',') if p.strip())})"
            for nome, parametros in re.findall(r'public function (\w+)\s*\(([^)]*)\)', texto) if nome != 'executar'}


def primeira_coluna(texto):
    return set(re.findall(r'^\|\s*([a-z]\w*)\s*\|', texto, re.M)) | set(re.findall(r'^\|\s*`(\w+)`\s*\|', texto, re.M))


@unittest.skipUnless((FONTES / 'SeiIntegracao.php').exists(), 'core do SEI fora deste checkout')
class CatalogoCoreTest(unittest.TestCase):
    """O catalogo cobre todo evento, classe API e operacao do core e so cita o que o core tem."""

    def ausentes(self, nomes, nome_catalogo):
        texto = catalogo(nome_catalogo)
        return [nome for nome in sorted(nomes) if not re.search(r'\b' + nome + r'\b', texto)]

    def test_eventos_de_sei_integracao(self):
        self.assertEqual(self.ausentes(eventos_do_core(), CATALOGO_EVENTOS), [])

    def test_classes_da_pasta_api(self):
        self.assertEqual(self.ausentes(atributos_das_classes_do_core(), CATALOGO_CLASSES), [])

    def test_operacoes_do_sei_rn(self):
        self.assertEqual(self.ausentes(operacoes_do_core(), CATALOGO_OPERACOES), [])

    def test_eventos_do_catalogo_existem_no_core(self):
        self.assertEqual(sorted(primeira_coluna(catalogo(CATALOGO_EVENTOS)) - eventos_do_core()), [])

    def test_operacoes_do_catalogo_existem_no_core(self):
        self.assertEqual(sorted(primeira_coluna(catalogo(CATALOGO_OPERACOES)) - operacoes_do_core()), [])

    def test_assinaturas_dos_eventos(self):
        texto = catalogo(CATALOGO_EVENTOS)
        secao = texto[texto.index('## Assinaturas no core'):] if '## Assinaturas no core' in texto else ''
        bloco = secao.split('```php', 1)[1].split('```', 1)[0] if '```php' in secao else ''
        no_catalogo = {linha.strip() for linha in bloco.splitlines() if linha.strip()}
        core = assinaturas_do_core()
        self.assertEqual((sorted(core - no_catalogo), sorted(no_catalogo - core)), ([], []))

    def test_catalogos_citam_so_classes_do_core(self):
        classes = set(atributos_das_classes_do_core()) | SO_NO_MANUAL
        for nome_catalogo in [CATALOGO_CLASSES, CATALOGO_EVENTOS, CATALOGO_OPERACOES]:
            with self.subTest(nome_catalogo):
                citadas = set(re.findall(r'\b[A-Z]\w*API\b', catalogo(nome_catalogo)))
                self.assertEqual(sorted(citadas - classes), [])

    def test_atributos_do_catalogo_existem_na_classe(self):
        atributos = atributos_das_classes_do_core()
        inexistentes = {}
        for classe, contrato in re.findall(r'^\|\s*`(\w+API)`\s*\|(.*)$', catalogo(CATALOGO_CLASSES), re.M):
            sobra = [nome for nome in re.findall(r'`(\w+)`:', contrato) if nome not in atributos.get(classe, set())]
            if sobra:
                inexistentes[classe] = sobra
        self.assertEqual(inexistentes, {})

    def test_campos_dos_contratos_existem_no_core(self):
        campos = set().union(*atributos_das_classes_do_core().values())
        inexistentes = {}
        for nome_catalogo in [CATALOGO_EVENTOS, CATALOGO_OPERACOES]:
            texto = catalogo(nome_catalogo)
            for lista in re.finditer(r'preenchidas? com:?([^|;.]*)', texto):
                citados = re.findall(r'\b[A-Z][A-Za-z0-9]+\b', lista.group(1))
                sobra = [nome for nome in citados if nome not in campos and nome not in VALORES_NOS_CONTRATOS and not nome.endswith('API')]
                if sobra:
                    inexistentes[f'{nome_catalogo}:{texto.count(chr(10), 0, lista.start()) + 1}'] = sobra
        self.assertEqual(inexistentes, {})

    def test_entrada_da_operacao_tem_o_tipo_do_core(self):
        texto_rn = (FONTES / 'rn/SeiRN.php').read_text(encoding='latin-1')
        tipo = {nome: classe for nome, classe in re.findall(r'protected function (\w+?)(?:Conectado|Controlado)\s*\(\s*(\w+API)\b', texto_rn)}
        divergentes = {}
        for operacao, entrada in re.findall(r'^\|\s*`(\w+)`\s*\|([^|]*)\|', catalogo(CATALOGO_OPERACOES), re.M):
            citada = re.search(r'\b(\w+API)\b', entrada)
            if operacao in tipo and (citada is None or citada.group(1).lower() != tipo[operacao].lower()):
                divergentes[operacao] = (citada.group(1) if citada else None, tipo[operacao])
        self.assertEqual(divergentes, {})

    def test_forma_da_entrada_da_operacao_segue_o_core(self):
        """Toda coluna de entrada do catalogo diz se o SeiRN recebe um objeto, uma lista ou nenhum parametro."""
        texto_rn = (FONTES / 'rn/SeiRN.php').read_text(encoding='latin-1')
        no_core = {}
        for nome, parametros in re.findall(r'protected function (\w+?)(?:Conectado|Controlado)\s*\(([^)]*)\)', texto_rn):
            parametros = parametros.strip()
            no_core[nome] = 'nenhum' if not parametros else 'lista' if parametros.startswith('$arr') else 'objeto'
        divergentes = {}
        coluna = None
        for linha in catalogo(CATALOGO_OPERACOES).splitlines():
            if not linha.startswith('|'):
                coluna = None
                continue
            colunas = [celula.strip() for celula in linha.strip().strip('|').split('|')]
            if colunas[0] in ('Nome', 'Operacao'):
                coluna = next((i for i, celula in enumerate(colunas) if celula.startswith('Entrada')), None)
                continue
            nome = colunas[0].strip('` ')
            if coluna is None or nome not in no_core:
                continue
            no_catalogo = self._forma(colunas[coluna])
            if no_catalogo != no_core[nome]:
                divergentes[nome] = (no_catalogo, no_core[nome])
        self.assertEqual(divergentes, {})

    @staticmethod
    def _forma(entrada):
        """Forma que o catalogo descreve: nenhum parametro, lista ou objeto."""
        if entrada.startswith('Sem parâmetro'):
            return 'nenhum'
        if re.search(r'Conjunto|Instâncias|ocorrências', entrada):
            return 'lista'
        if re.search(r'Instância\b', entrada) or re.match(r'`?\w+API`?', entrada):
            return 'objeto'
        return 'indefinida'


def ancora(titulo):
    """Ancora do titulo Markdown no GitHub e no VS Code."""
    return re.sub(r'\s', '-', re.sub(r'[^\w\- ]', '', titulo.strip().lower()))


class AncorasTest(unittest.TestCase):
    def test_links_com_ancora_das_skills_de_integracao(self):
        quebrados = []
        for skill in ['sei-mod-api-eventos', 'sei-mod-api-classes', 'sei-mod-api-operacoes', 'sei-direcionador-integracao']:
            for arquivo in sorted((SKILLS / skill).rglob('*.md')):
                for alvo, nome in re.findall(r'\]\(([^)#\s]*)#([^)\s]+)\)', arquivo.read_text(encoding='utf-8')):
                    destino = arquivo.parent / alvo if alvo else arquivo
                    titulos = {ancora(t) for t in re.findall(r'^#{1,6} (.+?)\s*$', destino.read_text(encoding='utf-8'), re.M)} if destino.exists() else set()
                    if nome not in titulos:
                        quebrados.append(f'{arquivo.relative_to(SKILLS)}#{nome}')
        self.assertEqual(quebrados, [])


class ResumoDosEventosTest(unittest.TestCase):
    def test_entrada_cita_os_parametros_da_assinatura(self):
        """As tabelas-resumo e a de contratos completos citam cada parametro que o core passa, conforme o bloco de assinaturas."""
        texto = catalogo(CATALOGO_EVENTOS)
        bloco = texto[texto.index('## Assinaturas no core'):].split('```php', 1)[1].split('```', 1)[0]
        parametros = {m.group(1): re.findall(r'\$(\w+)', m.group(2)) for m in re.finditer(r'public function (\w+)\((.*)\)', bloco)}
        tabelas = [  # (trecho do catalogo, coluna da entrada)
            (texto[:texto.index('## Notas sobre ambiguidades')], 2),
            (texto[texto.index('## Contratos completos dos eventos'):texto.index('## Assinaturas no core')], 1),
        ]
        divergentes = []
        for trecho, coluna_da_entrada in tabelas:
            for linha in trecho.splitlines():
                colunas = [coluna.strip() for coluna in linha.strip().strip('|').split('|')]
                nome = colunas[0].strip('` ')
                if len(colunas) <= coluna_da_entrada or nome not in parametros:
                    continue
                divergentes += [f'{nome}: {falta}' for falta in self._faltam(parametros[nome], colunas[coluna_da_entrada])]
        self.assertEqual(divergentes, [])

    @staticmethod
    def _faltam(parametros, entrada):
        """Parametros da assinatura ausentes da entrada; evento sem parametro diz `Sem parâmetro`."""
        if not parametros:
            return [] if entrada.startswith('Sem parâmetro') else ['Sem parâmetro']
        return [p for p in parametros if f'`${p}`' not in entrada and f'`{p}`' not in entrada]


class TemplatesSpecKitTest(unittest.TestCase):
    def test_plano_traz_impacto_arquitetural(self):
        texto = (ROOT / '.specify/templates/plan-template.md').read_text(encoding='utf-8')
        self.assertIn('**Impacto Arquitetural:**', texto)
        self.assertIn('Decisões Arquiteturais', texto)

    def test_toda_tarefa_traz_verify(self):
        for arquivo in ['.specify/templates/tasks-template.md', '.agents/skills/speckit-tasks/SKILL.md', '.agents/skills/speckit-converge/SKILL.md']:
            texto = (ROOT / arquivo).read_text(encoding='utf-8')
            self.assertIn('→ verify:', texto, arquivo)
            sem_verify = [linha for linha in texto.splitlines() if re.search(r'- \[ \] T\d{3}', linha) and '❌' not in linha and '→ verify:' not in linha]
            self.assertEqual(sem_verify, [], arquivo)

    def test_verify_cita_regras_do_auditor_de_pagina(self):
        regras = set(re.findall(r'^\| (P\d+) \|', (SKILLS / 'sei-verificacao-pagina/SKILL.md').read_text(encoding='utf-8'), re.M))
        citadas = set(re.findall(r'\bP\d+\b', (ROOT / '.specify/templates/tasks-template.md').read_text(encoding='utf-8')))
        self.assertTrue(citadas)
        self.assertEqual(sorted(citadas - regras), [])

    def test_skills_sem_marcador_do_instalador(self):
        """O Spec Kit ja esta instalado: nenhum instalador troca `__SPECKIT_COMMAND_*__`, e a skill cita a fase de forma generica."""
        sobras = [f'{caminho.parent.name}: {marcador}' for caminho in sorted(SKILLS.glob('speckit-*/SKILL.md'))
                  for marcador in re.findall(r'__SPECKIT_COMMAND_\w+?__', caminho.read_text(encoding='utf-8'))]
        self.assertEqual(sobras, [])

    def test_implement_marca_so_depois_do_verify(self):
        texto = (SKILLS / 'speckit-implement/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('only after its `→ verify:` check passes', texto)


class PonteirosDeSecaoTest(unittest.TestCase):
    SECAO = r'(?:seç(?:ão|ões)|secao|secoes)'
    TITULOS = r'((?:(?:"[^"]+"|`[^`]+`)(?:,\s*|\s+e\s+)?)+)'

    def test_secao_citada_existe_no_arquivo_apontado(self):
        """`arquivo.md`, seção "Título" ou `Título`, e a forma invertida, apontam para um título que existe no destino."""
        depois = re.compile(r'`([\w./-]+\.md)`,?\s+(?:na\s+)?' + self.SECAO + r'\s+' + self.TITULOS)
        antes = re.compile(self.SECAO + r'\s+' + self.TITULOS + r'\s+(?:de|do|da)\s+`([\w./-]+\.md)`')
        # No espelho publico, sem `fontes/`, o README.md da raiz e o guia da stack, e nao o README do repositorio.
        readme_da_raiz = (ROOT / 'README.md').resolve()
        espelho = not (ROOT / 'fontes').is_dir()
        quebrados = []
        for origem in self._documentos():
            texto = origem.read_text(encoding='utf-8')
            citacoes = [(m.group(1), m.group(2)) for m in depois.finditer(texto)]
            citacoes += [(m.group(2), m.group(1)) for m in antes.finditer(texto)]
            for destino, grupo in citacoes:
                caminhos = {c.resolve() for c in self._candidatos(origem, destino) if c.is_file()}
                if espelho and readme_da_raiz in caminhos:
                    continue
                titulos = set().union(*[self._titulos(c) for c in caminhos])
                for entre_aspas, entre_crases in re.findall(r'"([^"]+)"|`([^`]+)`', grupo):
                    secao = ' '.join((entre_aspas or entre_crases).split())
                    if secao not in titulos:
                        quebrados.append(f'{origem.relative_to(ROOT)}: {destino}, seção "{secao}"')
        self.assertEqual([], quebrados)

    @staticmethod
    def _documentos():
        pastas = [ROOT / '.agents', ROOT / 'docs/stack_ai', ROOT / '.specify']
        arquivos = [ROOT / 'AGENTS.md'] + [p for pasta in pastas if pasta.is_dir() for p in pasta.rglob('*.md')]
        return [p for p in arquivos if p.is_file() and not {'upstream', 'memory'} & set(p.parts)]

    @staticmethod
    def _candidatos(origem, destino):
        skill = next((p for p in origem.parents if p.parent.name == 'skills'), None)
        bases = [ROOT, origem.parent, ROOT / '.agents/references', ROOT / '.agents/skills'] + ([skill] if skill else [])
        return [base / destino for base in bases]

    @staticmethod
    def _titulos(caminho):
        """Titulos do arquivo, sem a numeracao inicial (`### 4. Titulo` vale como `Titulo`)."""
        linhas = caminho.read_text(encoding='utf-8').splitlines()
        titulos = {re.sub(r'^#+\s*', '', linha).strip() for linha in linhas if re.match(r'#{1,6}\s', linha)}
        return titulos | {re.sub(r'^\d+\.\s+', '', titulo) for titulo in titulos}

class ReusoDoCoreTest(unittest.TestCase):
    def test_acionamento_transversal(self):
        for arquivo in ['AGENTS.md', '.agents/references/roteamento-de-skills.md', '.specify/templates/plan-template.md']:
            texto = (ROOT / arquivo).read_text(encoding='utf-8')
            self.assertIn('Reuso do core', texto, arquivo)
            self.assertIn('sei-direcionador-integracao', texto, arquivo)

    def test_roteamento_aponta_o_campo_do_plano(self):
        plano = (ROOT / '.specify/templates/plan-template.md').read_text(encoding='utf-8')
        secao = plano.split('## Roteamento de Skills e Contratos', 1)[1].split('\n## ', 1)[0]
        roteamento = (ROOT / '.agents/references/roteamento-de-skills.md').read_text(encoding='utf-8')
        regra = next(linha for linha in roteamento.splitlines() if linha.startswith('14. Reuso do core'))
        self.assertIn('**Reuso do core:**', secao)
        self.assertIn('campo `Reuso do core`', regra)
        self.assertIn('Roteamento de Skills e Contratos', regra)

    def test_revisao_segue_a_conferencia_do_direcionador(self):
        direcionador = (SKILLS / 'sei-direcionador-integracao/SKILL.md').read_text(encoding='utf-8')
        revisao = (SKILLS / 'sei-revisao-tecnica/references/reutilizacao-rn-int-dto.md').read_text(encoding='utf-8')
        self.assertIn('### Conferir código já escrito', direcionador)
        self.assertIn('"Conferir código já escrito" de `sei-direcionador-integracao`', revisao)

    def test_veredito_do_direcionador(self):
        texto = (SKILLS / 'sei-direcionador-integracao/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Reuso do core:', texto)
        for capitulo in ['Classes API', 'Eventos', 'Operações']:
            self.assertIn(capitulo, texto)

    def test_evals_de_reuso(self):
        data = json.loads((SKILLS / 'sei-direcionador-integracao/evals/evals.json').read_text(encoding='utf-8'))
        self.assertEqual(data['skill_name'], 'sei-direcionador-integracao')
        self.assertEqual(len(data['evals']), 4)
        for caso in data['evals']:
            self.assertTrue(caso['prompt'])
            self.assertTrue(caso['contrato_esperado'])
            self.assertGreaterEqual(len(caso['expectations']), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
