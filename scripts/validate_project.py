#!/usr/bin/env python3
"""Offline verify: Codex TOML syntax, Skill metadata, path references, v9 migration fidelity.
Python 3.11+. No internet or Codex login needed.
"""
from pathlib import Path
import sys, json, tomllib, re, hashlib
ROOT = Path(__file__).resolve().parents[1]
config = tomllib.loads((ROOT/'.codex/config.toml').read_text(encoding='utf-8'))
assert config['web_search']=='live'
assert config['agents']['enabled'] is True

names=set()
for path in sorted((ROOT/'.codex/agents').glob('*.toml')):
    data=tomllib.loads(path.read_text(encoding='utf-8'))
    assert all(data.get(k) for k in ('name','description','developer_instructions')), path
    assert data['name']==path.stem and data['name'] not in names, path
    names.add(data['name'])
assert names == {'race_researcher','form_analyst','track_pace_analyst','odds_analyst','bet_strategy_analyst'}

skills = {}
for path in sorted((ROOT/'.agents/skills').glob('*/SKILL.md')):
    raw=path.read_text(encoding='utf-8')
    assert raw.startswith('---\n'), path
    match=re.match(r'^---\n(.*?)\n---\n',raw,re.S)
    assert match, path
    front=match.group(1)
    m=re.search(r'^name:\s*(\S+)$', front, re.M)
    assert m and m.group(1)==path.parent.name, path
    assert re.search(r'^description:\s*\S',front,re.M), path
    name=m.group(1)
    skills[name]=raw
    cat='local' if name.startswith('local-') else 'central'
    assert f'{cat}/prompts/INDEX.md' in raw
    assert f'{"central" if cat=="local" else "local"}/prompts/INDEX.md' not in raw, name
    for ref in re.findall(r'`((?:local|central)/prompts/[^`]+?\.md)`',raw):
        assert (ROOT/ref).is_file(), (name,ref)
assert set(skills)=={
    'local-race-info','local-full-prediction','local-odds-check',
    'central-race-info','central-full-prediction','central-odds-check'
}
for cat in ['local','central']:
    index=(ROOT/cat/'prompts/INDEX.md').read_text(encoding='utf-8')
    assert '### `main`' in index
    for name in names:
        assert f'### `{name}`' in index, (cat,name)
    modules=list((ROOT/cat/'prompts').rglob('*.md'))
    for module in modules:
        if module.name in ('INDEX.md','README.md'): continue
        rel=module.relative_to(ROOT).as_posix()
        assert module.read_text(encoding='utf-8').strip()
        assert f'`{rel}`' in index, (cat,rel)
    for ref in re.findall(r'`((?:local|central)/prompts/[^`]+?\.md)`',index):
        assert (ROOT/ref).is_file(), (cat,ref)
    # No references crossing domain paths in indexes
    other='central' if cat=='local' else 'local'
    assert re.search(r'`'+other+r'/prompts/(?:common|analysis|decision|research)/',index) is None

# Verify local migration against original immutable v9 source on demand.
if '--verify-local-v9' in sys.argv:
    manifest=json.loads((ROOT/'local/archive/migration_manifest.json').read_text(encoding='utf-8'))
    src=(ROOT/manifest['source']).read_bytes()
    assert hashlib.sha256(src).hexdigest()==manifest['source_sha256']
    lines=src.decode('utf-8').splitlines(keepends=True)
    assert len(manifest['sections'])==32
    # Check all 32 exact original sections still appear in module files.
    for item in manifest['sections']:
        frag=''.join(lines[item['source_start_line']-1:item['source_end_line']])
        assert hashlib.sha256(frag.encode()).hexdigest()==item['original_section_sha256'],item['heading']
        destination=(ROOT/item['path']).read_text(encoding='utf-8')
        assert frag in destination, item['heading']
    print('v9 migration: 32 original sections found intact in local modules.')
print(f'OK: {len(skills)} Skills, {len(names)} Agents, 2 prompt domains, TOML and references valid.')
