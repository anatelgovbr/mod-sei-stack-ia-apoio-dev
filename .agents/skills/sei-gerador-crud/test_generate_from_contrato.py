"""Testes do gerador de CRUD da skill sei-gerador-crud.

Fecha o ciclo da stack: o que o gerador produz precisa passar no auditor de RN.
Por isso este arquivo tambem invoca sei-verificacao-rn/audit.py.

    python3 -m unittest test_generate_from_contrato
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / ".agents" / "skills"
AUDITORS = {
    "rn": SKILLS / "sei-verificacao-rn" / "audit.py",
}


class GeradorCrudTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        path = self.work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_auditor(self, name, target, *extra):
        process = subprocess.run(
            [sys.executable, str(AUDITORS[name]), "--input", str(target), "--format", "json", "--exit-code", *extra],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertTrue(process.stdout, process.stderr)
        return process, json.loads(process.stdout)

    @staticmethod
    def codes(payload, field="erros"):
        return {
            issue["codigo"]
            for result in payload.get("results", [])
            for issue in result.get(field, [])
        }

    def test_crud_generator_uses_listar_in_generated_rn(self):
        contract = {
            "entidade": {
                "tabela": "md_ts_item",
                "singular": "item",
                "plural": "itens",
                "artigo": "o",
                "campoPrincipal": "str_nome",
                "comentario": "Item de teste",
            },
            "colunas": [
                {"nome": "id_md_ts_item", "tipoBanco": "integer", "chavePrimaria": True, "obrigatorio": True, "comentario": "Identificador"},
                {"nome": "str_nome", "tipoBanco": "varchar", "tamanho": 50, "chavePrimaria": False, "obrigatorio": True, "comentario": "Nome"},
            ],
            "relacionamentos": [],
            "relacionamentosNn": [],
            "regrasGeracao": {"campoSinAtivo": None},
            "ui": {"campos": {"str_nome": {"rotulo": "Nome", "teclaAtalho": "N"}}, "ordemFormulario": ["str_nome"]},
        }
        contract_path = self.write("contrato.json", json.dumps(contract))
        output = self.work / "gerado"
        process = subprocess.run(
            [sys.executable, str(SKILLS / "sei-gerador-crud" / "generate_from_contrato.py"), str(contract_path), str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, process.returncode, process.stderr)
        rn = output / "rn" / "MdTsItemRN.php"
        content = rn.read_text(encoding="latin-1")
        self.assertNotIn("validarAuditarPermissao('md_ts_item_consultar'", content)
        self.assertGreaterEqual(content.count("validarAuditarPermissao('md_ts_item_listar'"), 3)
        audit, payload = self.run_auditor("rn", rn)
        self.assertNotEqual(2, audit.returncode, payload)


if __name__ == "__main__":
    unittest.main()
