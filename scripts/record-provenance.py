"""Record the current export's origin and exact file fingerprints."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pac-version', help='Version used for this export; omit if unknown.')
args = parser.parse_args()
solution = Path(__file__).resolve().parents[1] / 'solution'
source = solution / 'unpacked'
archive = solution / 'exports/ZavaExMMeetingConcierge_2_0_0_0_unmanaged.zip'
manifest = ET.parse(source / 'Other/Solution.xml').getroot()

def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

record = {
    'project': 'Zava ExM Meeting Concierge',
    'export_date': datetime.now(timezone.utc).date().isoformat(),
    'source_environment': 'Zava PP Lab Dev',
    'solution_version': manifest.findtext('SolutionManifest/Version'),
    'package_type': 'Unmanaged',
    'pac_version': args.pac_version,
    'source': 'Authenticated live PAC export after owner tool cleanup; native PAC unpack',
    'export_archive': archive.relative_to(solution).as_posix(),
    'original_export_sha256': fingerprint(archive),
    'native_files_sha256': {
        path.relative_to(source).as_posix(): fingerprint(path)
        for path in sorted(source.rglob('*')) if path.is_file()
    },
}
(solution / 'provenance.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
print('Recorded current export fingerprints. Review the source diff before committing.')
