"""Check exported target components after import; never enables flows or calls services."""
import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

SOURCE = Path(__file__).resolve().parents[1] / 'solution/unpacked'

def verify(folder):
    expected_manifest = ET.parse(SOURCE/'Other/Solution.xml').getroot()
    actual_manifest = ET.parse(folder/'Other/Solution.xml').getroot()
    for field in ['UniqueName', 'Version']:
        if actual_manifest.findtext('SolutionManifest/'+field) != expected_manifest.findtext('SolutionManifest/'+field):
            raise ValueError('Imported solution identity or internal revision differs.')
    for name in ['Checknewmeeting-F5621481-00BD-F111-AAAD-6045BD06703E', 'Checkandmovemeeting-80614549-FDBC-F111-AAAD-6045BD067E6D']:
        path = folder/'Workflows'/(name+'.json')
        definition = json.loads(path.read_text(encoding='utf-8-sig'))['properties']['definition']
        metadata = ET.parse(path.with_name(path.name+'.data.xml')).getroot()
        if metadata.findtext('StateCode') != '0':
            raise ValueError('An imported flow is enabled. Pause processing and review the installation.')
        if not definition.get('actions'):
            raise ValueError('An imported flow is missing its actions.')
    refs = ET.parse(folder/'Other/Customizations.xml').getroot().find('connectionreferences')
    declared = {r.attrib['connectionreferencelogicalname'] for r in refs} if refs is not None else set()
    for path in (folder/'Workflows').glob('*.json'):
        flow = json.loads(path.read_text(encoding='utf-8-sig'))
        for ref in flow['properties']['connectionReferences'].values():
            if ref['connection']['connectionReferenceLogicalName'] not in declared:
                raise ValueError('An imported flow connection reference is missing from the solution.')
    for expected in (SOURCE/'environmentvariabledefinitions').glob('*/environmentvariabledefinition.xml'):
        actual = folder/expected.relative_to(SOURCE)
        if ET.parse(actual).getroot().attrib.get('schemaname') != expected.parent.name:
            raise ValueError('An imported configuration definition is missing or incorrect.')
    if not (folder/'Entities/cr9b0_CalendarGovernanceRule/Entity.xml').is_file():
        raise ValueError('The governance rule table is missing.')
    if not (folder/'bots/cr9b0_ZavaCalendarGovernanceAgent/bot.xml').is_file():
        raise ValueError('The agent is missing.')
    tools = list((folder/'botcomponents').glob('*.action.*/data'))
    if len(tools) != 1:
        raise ValueError('Expected exactly one agent tool.')
    content = tools[0].read_text(encoding='utf-8-sig')
    if 'kind: InvokeFlowTaskAction' not in content or not re.search(r'flowId:\s*80614549-fdbc-f111-aaad-6045bd067e6d\b', content, re.I):
        raise ValueError('The agent tool does not point to the Gatekeeper flow.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', required=True, type=Path)
    args = parser.parse_args()
    verify(args.folder)
    print('Imported solution, agent tool, flows, table, and configuration definitions passed structural checks. Flows are off. Runtime permissions and calendar behavior still require acceptance testing.')
