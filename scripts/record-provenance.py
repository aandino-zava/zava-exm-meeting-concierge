"""Record the portable package build and exact source fingerprints."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pac-version', help='Version used to pack this build; omit if unknown.')
args = parser.parse_args()
solution = Path(__file__).resolve().parents[1] / 'solution'
source = solution / 'unpacked'
manifest = ET.parse(source / 'Other/Solution.xml').getroot()
version = manifest.findtext('SolutionManifest/Version')
archive = solution / 'exports/ZavaExMMeetingConcierge.zip'

def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

record = {
    'project': 'Zava ExM Meeting Concierge',
    'build_date': datetime.now(timezone.utc).date().isoformat(),
    'source_environment': None,
    'solution_version': version,
    'package_type': 'Unmanaged',
    'pac_version': args.pac_version,
    'source': 'Repository-authored portable solution build; not a live export',
    'export_archive': archive.relative_to(solution).as_posix(),
    'archive_sha256': fingerprint(archive),
    'native_files_sha256': {
        path.relative_to(source).as_posix(): fingerprint(path)
        for path in sorted(source.rglob('*')) if path.is_file()
    },
}
(solution / 'provenance.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
(archive.parent/'SHA256SUMS.txt').write_text(fingerprint(archive)+'  '+archive.name+'\n', encoding='utf-8')
print('Recorded portable package fingerprints. This does not establish a successful tenant import.')
