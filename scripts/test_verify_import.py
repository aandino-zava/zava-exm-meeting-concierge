"""Exercise post-import checks against isolated exported-source fixtures."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_import', Path(__file__).with_name('verify-import.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ImportVerificationTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'build').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='verify-', dir=ROOT/'build')
        self.folder = Path(self.temp.name).resolve()
        self.assertTrue(self.folder.is_relative_to((ROOT/'build').resolve()))
        shutil.copytree(ROOT/'solution/unpacked', self.folder, dirs_exist_ok=True)

    def tearDown(self):
        self.temp.cleanup()

    def change(self, path, old, new):
        file = self.folder/path
        file.write_text(file.read_text(encoding='utf-8-sig').replace(old,new), encoding='utf-8')

    def test_complete_export_passes(self):
        module.verify(self.folder)

    def test_enabled_flow_is_rejected(self):
        file = next((self.folder/'Workflows').glob('*.data.xml'))
        self.change(file.relative_to(self.folder), '<StateCode>0</StateCode>', '<StateCode>1</StateCode>')
        with self.assertRaisesRegex(ValueError, 'enabled'): module.verify(self.folder)

    def test_missing_connection_is_rejected(self):
        self.change('Other/Customizations.xml', 'connectionreferencelogicalname="cr9b0_sharedoffice365_2e7d8"', 'connectionreferencelogicalname="missing"')
        with self.assertRaisesRegex(ValueError, 'connection reference'): module.verify(self.folder)

    def test_different_tool_binding_is_rejected(self):
        file = next((self.folder/'botcomponents').glob('*.action.*/data'))
        self.change(file.relative_to(self.folder), '80614549-fdbc-f111-aaad-6045bd067e6d', '00000000-0000-0000-0000-000000000000')
        with self.assertRaisesRegex(ValueError, 'Gatekeeper'): module.verify(self.folder)

    def test_wrong_internal_revision_is_rejected(self):
        self.change('Other/Solution.xml', '<Version>2.1.0.0</Version>', '<Version>0.0.0.0</Version>')
        with self.assertRaisesRegex(ValueError, 'revision'): module.verify(self.folder)

    def test_missing_configuration_is_rejected(self):
        self.change('environmentvariabledefinitions/cr9b0_CalendarMailbox/environmentvariabledefinition.xml', 'schemaname="cr9b0_CalendarMailbox"', 'schemaname="missing"')
        with self.assertRaisesRegex(ValueError, 'configuration'): module.verify(self.folder)

if __name__ == '__main__':
    unittest.main(verbosity=2)
