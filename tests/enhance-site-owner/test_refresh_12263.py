"""Regression checks for the 12.26.3 schema; synthetic loopback only."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import enhance as e
import test_enhance as fixtures


class RefreshTests(unittest.TestCase):
    def test_callback_protocols_refuse_before_binding_or_transport(self):
        c = e.Catalog()
        p = e.Profile({'base_url': 'https://example.invalid/api', 'scope': 'admin'})
        with mock.patch.object(e, 'transport', side_effect=AssertionError('network forbidden')):
            for name in ('manifestCallback', 'installComplete', 'githubWebhook'):
                with self.subTest(operation=name):
                    self.assertTrue(e.auth_support(c.operation(name)).startswith('unsupported'))
                    with self.assertRaises(e.CLIError) as caught:
                        e.prepare(c, p, name, {'code': 'synthetic-secret'})
                    self.assertEqual(caught.exception.code, 'unsupported')
                    self.assertNotIn('synthetic-secret', str(caught.exception))

    def test_member_session_requires_apply_and_private_output(self):
        c = e.Catalog()
        token = 'SYNTHETIC-SESSION-SECRET'
        with tempfile.TemporaryDirectory(dir=e.ROOT) as tmp, fixtures.local_server([(201, {'Content-Type': 'application/json'}, json.dumps(token).encode())]) as (p, server):
            request = e.prepare(c, p, 'createMemberSession', {'member_id': fixtures.OTHER})
            self.assertTrue(request.guidance['requires_output'])
            self.assertTrue(e.execute(request, p)['dry_run'])
            with self.assertRaises(e.CLIError):
                e.execute(request, p, apply=True)
            self.assertEqual(server.records, [])
            output = Path(tmp) / 'session.json'
            result = e.execute(request, p, apply=True, output=output)
            self.assertTrue(result['output_written'])
            self.assertNotIn(token, json.dumps(result))
            self.assertEqual(json.loads(output.read_text()), token)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.assertEqual(len(server.records), 1)

    def test_github_metadata_is_private_and_not_batchable(self):
        c = e.Catalog()
        p = e.Profile({'base_url': 'https://example.invalid/api', 'scope': 'admin'})
        import build_inventory
        for name in ('getOrgGithubAppInfo', 'getOrgGithubRepoRefs', 'getWebsiteGitInfo', 'getWebsiteGitDeploys', 'getWebsiteGitDeploymentLog'):
            with self.subTest(operation=name):
                op = c.operation(name)
                params = {v['name']: build_inventory.sample(c, v['schema']) for v in op['parameters'] if v.get('required')}
                req = e.prepare(c, p, name, params)
                self.assertTrue(req.guidance['requires_apply'])
                self.assertTrue(req.guidance['requires_output'])
                with mock.patch.object(e, 'transport', side_effect=AssertionError('network forbidden')):
                    with self.assertRaises(e.CLIError):
                        e.batch(c, p, [{'operationId': name, 'params': params}])
