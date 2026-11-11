#!/usr/bin/env python3
"""Exercise installed Hermes discovery, bundle fetch, scan and install locally.

Run with the Hermes runtime interpreter and its bootstrap available. Fixture
GitHub transport reads this candidate only; no remote request or active-profile
write is permitted. This is NOT a public GitHub install test.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest import mock


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hermes-source', required=True)
    parser.add_argument('--scratch', required=True)
    args = parser.parse_args()
    source = Path(args.hermes_source).resolve()
    root = Path(__file__).resolve().parents[1]
    skill = root / 'skills/enhance-site-owner'
    expected = {p.relative_to(skill).as_posix() for p in skill.rglob('*') if p.is_file()}
    assert 'scripts/assets/openapi.json' not in expected
    sys.path.insert(0, str(source))
    with tempfile.TemporaryDirectory(prefix='te-hermes-qualification-', dir=args.scratch) as temporary:
        home = Path(temporary)
        os.environ['HERMES_HOME'] = str(home)
        sys.dont_write_bytecode = True
        # Use runtime-managed dependencies, without changing its configuration.
        import hermes_bootstrap
        import httpx
        from tools import skills_hub as hub
        from tools import skills_hub_github as gh
        from tools.skills_guard import scan_skill
        from tools.skills_hub_install import quarantine_bundle, install_from_quarantine
        repo = 'example-owner/te-customer-agents'
        prefix = 'skills/enhance-site-owner/'
        revision = 'synthetic-local-revision'
        adapter = gh.GitHubSource(auth=mock.Mock())
        entries = [{'path':prefix+rel,'type':'blob','mode':'100644'} for rel in sorted(expected)]
        def read_text(repo_arg, path, **kwargs):
            assert repo_arg == repo
            return (root / path).read_text(encoding='utf-8')
        def read_bytes(repo_arg, path, **kwargs):
            assert repo_arg == repo
            assert kwargs.get('ref') == revision
            return (root / path).read_bytes()
        def get_tree(repo_arg):
            assert repo_arg == repo
            adapter._tree_revisions[repo] = revision
            return ('main', entries)
        with mock.patch.object(gh, '_cached_metas', return_value=None), mock.patch.object(gh, '_cache_metas'), mock.patch.object(adapter, '_get_skillsh_groupings', return_value=None), mock.patch.object(adapter, '_github_get', return_value=httpx.Response(200,json=[{'type':'dir','name':'enhance-site-owner'}])), mock.patch.object(adapter, '_fetch_file_content', side_effect=read_text):
            found = adapter._list_skills_in_repo(repo, 'skills/')
            assert len(found) == 1 and found[0].identifier == repo+'/skills/enhance-site-owner'
            identifier = found[0].identifier
            with mock.patch.object(adapter, '_get_repo_tree', side_effect=get_tree), mock.patch.object(adapter, '_fetch_file_bytes', side_effect=read_bytes):
                bundle = adapter.fetch(identifier)
        assert bundle is not None
        assert set(bundle.files) == expected, {'missing':sorted(expected-set(bundle.files)), 'extra':sorted(set(bundle.files)-expected)}
        assert hub._skills_dir().resolve().is_relative_to(home), 'Refuse active-profile writes'
        quarantined = quarantine_bundle(bundle)
        result = scan_skill(quarantined, source=repo)
        assert result.verdict != 'dangerous', [(f.pattern_id,f.description) for f in result.findings]
        installed = install_from_quarantine(quarantined, bundle.name, '', bundle, result)
        actual = {p.relative_to(installed).as_posix() for p in installed.rglob('*') if p.is_file()}
        assert actual == expected
        # Demonstrate that completeness assertion rejects an omitted runtime helper.
        omitted = set(actual) - {'scripts/compose_token.py'}
        assert omitted != expected
        print(json.dumps({'ok':True,'identifier_fixture':identifier,'skill_name':bundle.name,'source_files':len(expected),'bundle_files':len(bundle.files),'installed_files':len(actual),'scanner_verdict':result.verdict,'scanner_findings':[{'pattern_id':f.pattern_id,'severity':f.severity,'description':f.description} for f in result.findings],'real_hermes_discovery_fetch_quarantine_scan_install':True,'transport':'synthetic local GitHub fixtures','active_profile_modified':False,'public_install_tested':False,'full_vendor_schema_present':False}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
