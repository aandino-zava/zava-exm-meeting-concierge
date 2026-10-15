from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
p=root/'solution';source=p/'unpacked';archive=p/'exports/ZavaExMMeetingConcierge_2_0_0_0_unmanaged.zip'
manifest=ET.parse(source/'Other/Solution.xml').getroot()
hashfile=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
value={'project':'Zava ExM Meeting Concierge','export_date':'2026-10-15','source_environment':'Zava PP Lab Dev','solution_version':manifest.findtext('SolutionManifest/Version'),'package_type':'Unmanaged','pac_version':'2.13.1+g251dee1','source':'Authenticated live PAC export after Dev implementation; native PAC unpack','export_archive':archive.relative_to(p).as_posix(),'original_export_sha256':hashfile(archive),'native_files_sha256':{f.relative_to(source).as_posix():hashfile(f) for f in sorted(source.rglob('*')) if f.is_file()}}
(p/'provenance.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print('Updated current export fingerprints. Review before committing.')
