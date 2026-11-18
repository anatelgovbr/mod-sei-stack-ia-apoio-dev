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

if __name__ == '__main__':
    unittest.main(verbosity=2)
