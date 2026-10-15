"""Static source and sensitive-data checks; never calls Microsoft or GitHub."""
from pathlib import Path
import hashlib, json, re, sys, zipfile
import xml.etree.ElementTree as ET
import yaml

root=Path(__file__).resolve().parents[1]
errors=[]; counts={'json':0,'xml':0,'yaml':0,'links':0,'archive_members':0}
address_files=[]
patterns={
    'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github_token':r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
    'jwt':r'\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}',
    'bearer_value':r'(?i)bearer\s+[A-Za-z0-9_.-]{25,}',
    'signed_url':r'(?i)[?&](?:sig|access_token|refresh_token)=[A-Za-z0-9%_+./-]{12,}',
    'assigned_secret':r'''(?i)["']?(?:client_secret|clientSecret|access_token|refresh_token|password|api_key)["']?\s*[:=]\s*["'][^"'\s]{12,}["']''',
}
def inspect(name,data,parse=True):
    try: text=data.decode('utf-8-sig')
    except UnicodeDecodeError: return
    for label,pat in patterns.items():
        if re.search(pat,text): errors.append(f'{label}: {name}')
    if re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',text): address_files.append(name)
    if not parse: return
    try:
        if name.endswith('.json'): json.loads(text); counts['json']+=1
        elif name.endswith('.xml'): ET.fromstring(text); counts['xml']+=1
        elif name.endswith(('.yml','.yaml')) or '/botcomponents/' in '/'+name and name.endswith('/data'):
            yaml.safe_load(text); counts['yaml']+=1
    except Exception as e: errors.append(f'Parse failure {name}: {e}')
for p in root.rglob('*'):
    if not p.is_file() or any(x in {'.git','build','__pycache__'} for x in p.relative_to(root).parts): continue
    rel=p.relative_to(root).as_posix()
    if p.name.startswith('.env') or re.search(r'(?i)(tokencache|authprofile|cookies\.sqlite)',p.name): errors.append('Forbidden file: '+rel)
    if p.suffix=='.zip':
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            for n in z.namelist():
                if not n.endswith('/'): inspect(rel+'!'+n,z.read(n)); counts['archive_members']+=1
    else: inspect(rel,p.read_bytes())
    if p.suffix=='.md':
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' in link or link.startswith('#'): continue
            target=link.split('#')[0]
            if not (p.parent/target).exists(): errors.append(f'Broken link: {rel} -> {link}')
            counts['links']+=1
prov=json.loads((root/'solution/provenance.json').read_text())
for rel,expected in prov['native_files_sha256'].items():
    if hashlib.sha256((root/'solution/unpacked'/rel).read_bytes()).hexdigest()!=expected: errors.append('Native hash mismatch: '+rel)
zip_path=root/'solution'/prov['export_archive']
if hashlib.sha256(zip_path.read_bytes()).hexdigest()!=prov['archive_sha256']: errors.append('Portable archive hash mismatch')
checksum=(zip_path.parent/'SHA256SUMS.txt').read_text().strip()
if checksum!=prov['archive_sha256']+'  '+zip_path.name: errors.append('Download checksum differs')
actual={p.relative_to(root/'solution/unpacked').as_posix() for p in (root/'solution/unpacked').rglob('*') if p.is_file()}
if actual!=set(prov['native_files_sha256']): errors.append('Current provenance file inventory differs')
tool_files=list((root/'solution/unpacked/botcomponents').glob('*.action.*/data'))
if len(tool_files)!=1:
    errors.append(f'Expected one current agent tool, found {len(tool_files)}')
else:
    tool=yaml.safe_load(tool_files[0].read_text(encoding='utf-8'))
    if tool.get('modelDisplayName')!='Check and move meeting' or tool.get('action',{}).get('kind')!='InvokeFlowTaskAction':
        errors.append('Current agent tool does not match the checked scheduling flow')
print(json.dumps({'checks':counts,'errors':errors,'retained_lab_address_files':address_files},indent=2))
sys.exit(1 if errors else 0)
