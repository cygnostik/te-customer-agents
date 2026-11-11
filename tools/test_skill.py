#!/usr/bin/env python3
"""Test a disposable skill copy; vendor schema never enters source tree."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scratch',required=True,help='Private writable scratch directory')
    parser.add_argument('--schema',help='Existing official schema JSON; otherwise fetch publisher YAML using setup helper')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    work=Path(tempfile.mkdtemp(prefix='te-skill-test-',dir=args.scratch))
    skill=work/'skill'
    shutil.copytree(root/'skills/enhance-site-owner',skill)
    for test in (root/'tests/enhance-site-owner').glob('test_*.py'):
        shutil.copyfile(test,skill/'scripts'/test.name)
    env=dict(os.environ,TMPDIR=str(work),PYTHONDONTWRITEBYTECODE='1')
    if args.schema:
        shutil.copyfile(args.schema,skill/'scripts/assets/openapi.json')
    else:
        setup=subprocess.run([sys.executable,str(skill/'scripts/setup_schema.py')],capture_output=True,text=True,env=env)
        (work/'schema-setup.log').write_text(setup.stdout+setup.stderr)
        if setup.returncode:
            print(setup.stdout+setup.stderr,file=sys.stderr)
            return setup.returncode
    command=[sys.executable,'-m','unittest','discover','-s',str(skill/'scripts'),'-p','test_*.py','-v']
    result=subprocess.run(command,capture_output=True,text=True,env=env)
    (work/'unittest.log').write_text(result.stdout+result.stderr)
    print(result.stdout+result.stderr)
    receipt={'exit_code':result.returncode,'python':sys.version,'workspace':str(work),'source_schema_present':(root/'skills/enhance-site-owner/scripts/assets/openapi.json').exists()}
    (work/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    return result.returncode

if __name__=='__main__':
    raise SystemExit(main())
