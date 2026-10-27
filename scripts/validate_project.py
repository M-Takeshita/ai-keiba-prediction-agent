#!/usr/bin/env python3
"""Offline structural validation; optional initial-migration check.
Requires Python 3.11+ (tomllib). Does not call web or Codex.
"""
from pathlib import Path
import sys, json, tomllib, re, hashlib

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT/'prompts/INDEX.md').read_text(encoding='utf-8')
config = tomllib.loads((ROOT/'.codex/config.toml').read_text(encoding='utf-8'))
assert config['web_search'] == 'live'
assert config['agents']['enabled'] is True
agent_names = set()
for fp in sorted((ROOT/'.codex/agents').glob('*.toml')):
    info = tomllib.loads(fp.read_text(encoding='utf-8'))
    assert fp.stem == info['name']
    assert info['name'] not in agent_names
    agent_names.add(info['name'])
    assert all(info.get(x) for x in ('name','description','developer_instructions'))
    assert f'### `{fp.stem}`' in INDEX, f'missing INDEX route for {fp.stem}'
assert agent_names, 'no subagents configured'
assert '### `main`' in INDEX

modules = [p for p in (ROOT/'prompts').rglob('*.md') if p.name not in {'INDEX.md','README.md'}]
assert modules, 'no prompt modules found'
for m in modules:
    rel=m.relative_to(ROOT).as_posix()
    assert f'`{rel}`' in INDEX, f'{rel} is not indexed'
    assert m.read_text(encoding='utf-8').strip(), f'{rel} empty'
for ref in re.findall(r'`(prompts/(?:common|research|analysis|decision|workflow|review|output)/[^`]+?\.md)`',INDEX):
    assert (ROOT/ref).exists(), f'{ref} referenced but missing'

if '--verify-initial-migration' in sys.argv:
    manifest=json.loads((ROOT/'archive/migration_manifest.json').read_text(encoding='utf-8'))
    src=(ROOT/manifest['source']).read_bytes()
    assert hashlib.sha256(src).hexdigest()==manifest['source_sha256']
    lines=src.decode('utf-8').splitlines(keepends=True)
    starts=[s['source_start_line'] for s in manifest['sections']]
    assert starts[0]==3 and len(manifest['sections'])==32
    assert ''.join(lines[:2]).startswith('# 🏇')
    for part in manifest['sections']:
        text=''.join(lines[part['source_start_line']-1:part['source_end_line']])
        assert hashlib.sha256(text.encode()).hexdigest()==part['original_section_sha256']
        dest=(ROOT/part['path']).read_text(encoding='utf-8')
        assert text in dest, f'differs from v9 original: {part["heading"]}'
    print('Migration match: all original 32 sections occur intact in their assigned modules.')
print(f'OK: {len(modules)} modules, {len(agent_names)} subagents, project config and routes.')
