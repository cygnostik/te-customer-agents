"""Customer CLI entrypoint regressions; every value is synthetic."""
import json
from pathlib import Path
import tempfile
import unittest
import enhance as e

ORG = '11111111-1111-4111-8111-111111111111'
SITE = '22222222-2222-4222-8222-222222222222'

class CustomerProfileTests(unittest.TestCase):
    def load(self, document, name=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'synthetic.json'
            path.write_text(json.dumps(document), encoding='utf-8')
            return e.load_profile(path, name)

    def test_customer_scopes_load(self):
        for scope in ('site', 'organisation'):
            profile = self.load({'scope':scope, 'base_url':'https://example.invalid/api', 'org_id':ORG, 'website_id':SITE})
            self.assertEqual(profile.scope, scope)

    def test_admin_unknown_missing_and_nonobject_rejected(self):
        for document in ({'scope':'admin'}, {'scope':'provider'}, {}, [], None):
            with self.subTest(document=document), self.assertRaisesRegex(e.CLIError, 'Customer CLI accepts only'):
                self.load(document)

    def test_named_admin_rejected(self):
        with self.assertRaisesRegex(e.CLIError, 'Customer CLI accepts only'):
            self.load({'profiles':{'operator':{'scope':'admin'}},'default_profile':'operator'})

if __name__ == '__main__':
    unittest.main()
