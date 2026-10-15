"""Check package dependencies and portable configuration without a tenant connection."""
import json
import os
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'solution/unpacked'

class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.settings = json.loads((ROOT/'deployment/settings.example.json').read_text(encoding='utf-8'))
        self.customizations = ET.parse(SOURCE/'Other/Customizations.xml').getroot()
        self.flows = [json.loads(p.read_text(encoding='utf-8')) for p in (SOURCE/'Workflows').glob('*.json')]

    def test_all_flow_connections_are_declared_and_mapped(self):
        declared = {r.attrib['connectionreferencelogicalname']:r.findtext('connectorid') for r in self.customizations.find('connectionreferences')}
        used = {}
        for flow in self.flows:
            for ref in flow['properties']['connectionReferences'].values():
                name = ref['connection']['connectionReferenceLogicalName']
                connector = '/providers/Microsoft.PowerApps/apis/'+ref['api']['name']
                self.assertEqual(declared.get(name), connector, name)
                used[name] = connector
        mapped = {r['LogicalName']:r['ConnectorId'] for r in self.settings['ConnectionReferences']}
        self.assertEqual(used, declared)
        self.assertEqual(mapped, declared)
        self.assertEqual(len(declared), 3)
        self.assertTrue(all(r['ConnectionId']=='' for r in self.settings['ConnectionReferences']))

    def test_required_settings_have_no_lab_defaults(self):
        definitions = {}
        for p in (SOURCE/'environmentvariabledefinitions').glob('*/environmentvariabledefinition.xml'):
            element = ET.parse(p).getroot()
            definitions[element.attrib['schemaname']] = element
            self.assertEqual(element.findtext('isrequired'), '1')
            self.assertFalse(element.findtext('defaultvalue'))
        self.assertEqual(set(definitions), {r['SchemaName'] for r in self.settings['EnvironmentVariables']})
        self.assertEqual(len(definitions), 3)
        self.assertTrue(all(r['Value']=='' for r in self.settings['EnvironmentVariables']))
        used = set()
        for flow in self.flows:
            for parameter in flow['properties']['definition']['parameters'].values():
                if 'schemaName' in parameter.get('metadata',{}):
                    used.add(parameter['metadata']['schemaName'])
                    self.assertEqual(parameter['defaultValue'], '')
        self.assertEqual(used, set(definitions))

    def test_import_starts_with_both_flows_off(self):
        for p in (SOURCE/'Workflows').glob('*.data.xml'):
            root = ET.parse(p).getroot()
            self.assertEqual(root.findtext('StateCode'), '0')
            self.assertEqual(root.findtext('StatusCode'), '1')

    def test_current_flows_have_no_lab_addresses_or_calendar_id(self):
        for flow in self.flows:
            text = json.dumps(flow).lower()
            self.assertNotIn('onmicrosoft.com', text)
            self.assertNotIn('aamkadgw', text)
        starter = next(f for f in self.flows if 'When_a_new_event_is_created_(V3)' in f['properties']['definition']['triggers'])
        trigger = next(iter(starter['properties']['definition']['triggers'].values()))
        self.assertEqual(trigger['inputs']['parameters']['table'], "@parameters('Calendar ID (cr9b0_CalendarId)')")

    def test_required_readme_sections_remain(self):
        text = (ROOT/'README.md').read_text(encoding='utf-8')
        for title in ['Overview','Design Rationale','How It Works','The Gatekeeper Pattern','Power Platform Components']:
            self.assertIn('## '+title, text)
        self.assertIn('Notify executive assistant when new protected event conflicts', text)
        self.assertNotIn('## Source and earlier work', text)

    def test_distributable_contains_current_flows_and_settings(self):
        provenance = json.loads((ROOT/'solution/provenance.json').read_text(encoding='utf-8'))
        package = Path(os.environ['CONCIERGE_PACKAGE_PATH']) if os.environ.get('CONCIERGE_PACKAGE_PATH') else ROOT/'solution'/provenance['export_archive']
        with zipfile.ZipFile(package) as archive:
            for path in (SOURCE/'Workflows').glob('*.json'):
                self.assertEqual(json.loads(archive.read('Workflows/'+path.name)), json.loads(path.read_text(encoding='utf-8')))
            customizations = ET.fromstring(archive.read('customizations.xml'))
            declared = {r.attrib['connectionreferencelogicalname'] for r in customizations.find('connectionreferences')}
            self.assertEqual(declared, {r['LogicalName'] for r in self.settings['ConnectionReferences']})
            # Environment variables are native sharded components in the solution ZIP.
            for setting in self.settings['EnvironmentVariables']:
                path = 'environmentvariabledefinitions/'+setting['SchemaName']+'/environmentvariabledefinition.xml'
                definition = ET.fromstring(archive.read(path))
                self.assertEqual(definition.attrib['schemaname'], setting['SchemaName'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
