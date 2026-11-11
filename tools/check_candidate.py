#!/usr/bin/env python3
"""Local source checks, not a credential scanner or security certification."""
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/enhance-site-owner'

def check(root=ROOT):
    errors = []
    files = sorted(p for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts)
    for p in files:
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            errors.append(rel + ': symlink forbidden')
        if any(part in ('__pycache__', 'private', 'profiles', 'credentials', 'evidence') for part in p.relative_to(root).parts) or p.name == 'openapi.json' or p.suffix in ('.token','.pem','.key','.pyc','.log','.zip') or p.name.startswith('.env'):
            errors.append(rel + ': runtime/private file forbidden')
        if p.suffix in ('.md','.py','.json','.html','.svg') or p.name == '.gitignore':
            text = p.read_text(encoding='utf-8')
            # Construct patterns so this checker does not trip over its own literals.
            for marker in ('/'+'Users/', '/'+'home/', 'Pro'+'Dyn'):
                if marker in text:
                    errors.append(rel + ': private path or wrong identity marker')
            if p.suffix == '.py':
                ast.parse(text, filename=rel)
            if p.suffix == '.json':
                json.loads(text)
            if p.suffix == '.svg':
                ET.fromstring(text)
            if p.suffix == '.md':
                # Explicit inline Markdown links; not arbitrary prose, references, or fenced code.
                prose = re.sub(r'```.*?```', '', text, flags=re.S)
                for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', prose):
                    if urlsplit(target).scheme or target.startswith('#'):
                        continue
                    linked = (p.parent / unquote(target.split('#')[0])).resolve()
                    if not linked.is_relative_to(root.resolve()) or not linked.exists():
                        errors.append(rel + ': missing/escaping link ' + target)
    skills = sorted(root.glob('skills/*/SKILL.md'))
    if len(skills) != 1:
        errors.append('expected exactly one skill')
    for path in skills:
        text = path.read_text(encoding='utf-8')
        if not text.startswith('---\n') or '\n---\n' not in text[4:]:
            errors.append('invalid frontmatter delimiters')
            continue
        front, body = text[4:].split('\n---\n', 1)
        # Format-specific dependency-free checks; real Hermes parser is exercised separately.
        for key in ('name','description','version','author','license','platforms','metadata'):
            if not re.search(r'^'+key+r':', front, re.M):
                errors.append('missing frontmatter '+key)
        match = re.search(r'^description: (.+)$', front, re.M)
        if match:
            desc = match[1].strip('\"\'')
            if len(desc)>60 or not desc.endswith('.'):
                errors.append('description length/punctuation')
        if not body.strip():
            errors.append('empty skill body')
        if path.parent.name != re.search(r'^name: (.+)$', front, re.M)[1]:
            errors.append('skill directory/name mismatch')
        for required in ('scripts/enhance.py','scripts/setup_schema.py','scripts/compose_token.py','scripts/assets/freshness.json','templates/site-profile.json','templates/organisation-profile.json','NOTICE.md'):
            if not (path.parent / required).is_file():
                errors.append('missing support file '+required)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(json.dumps({'ok':True,'source_files':len(files),'skills':len(skills),'full_vendor_schema_present':False,'scope':'syntax, explicit inline Markdown links, required files and bounded hygiene markers'}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(check())
