import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / 'hooks/scripts/session-start-context.py'
spec = importlib.util.spec_from_file_location('hook', HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)
VALID = {'display_name': 'Athlete', 'user_id': 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
         'routine_type_ids': {'Gym': 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb'}}


class WorkspaceTests(unittest.TestCase):
    def run_hook(self, files):
        with tempfile.TemporaryDirectory() as folder:
            for name, content in files.items():
                (Path(folder) / name).write_text(content)
            return subprocess.run([sys.executable, str(HOOK)],
                                  input=json.dumps({'cwd': folder}), text=True,
                                  capture_output=True, check=True).stdout

    def test_unrelated_folder_stays_silent(self):
        self.assertEqual(self.run_hook({}), '')

    def test_legacy_marker_requires_setup(self):
        self.assertIn('Only get_athlete_context is allowed',
                      self.run_hook({'source-of-truth.md': ''}))

    def test_example_bootstraps_setup_without_source_of_truth(self):
        self.assertIn('Training setup required', self.run_hook({
            'athlete-config.json': (ROOT / 'references/athlete-config.example.json').read_text()}))

    def test_invalid_config_fails_closed(self):
        for value in ('{broken', '[]', 'null', '{"user_id": "unknown"}'):
            self.assertIn('Training setup required', self.run_hook({'athlete-config.json': value}))

    def test_missing_profile_runs_onboarding(self):
        self.assertIn('current gym program', self.run_hook({'athlete-config.json': json.dumps(VALID)}))

    def test_ready_workspace_runs_check_in(self):
        files = {name: '' for name in ('source-of-truth.md', 'user-profile.md', 'strength-template.md')}
        files['athlete-config.json'] = json.dumps(VALID)
        self.assertIn('morning-check-in', self.run_hook(files))

    def test_bad_identity_and_routines_rejected(self):
        for change in ({'user_id': 'bad'}, {'routine_type_ids': {}},
                       {'routine_type_ids': {'Gym': 'bad'}}, {'display_name': ''},
                       {'user_id': '00000000-0000-0000-0000-000000000000'}):
            self.assertFalse(hook.valid_identity({**VALID, **change}))
        self.assertTrue(hook.valid_identity(VALID))

    def test_live_skills_do_not_embed_chris_identity(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            self.assertNotIn('d11e8eea-7aab-4d6c-85ad-0079243bdbca', path.read_text())
            self.assertIn('ATHLETE.md', path.read_text(), str(path))

    def test_coach_uses_named_tools_without_user_id_arguments(self):
        import re
        for name in ('program-workout', 'review-program', 'morning-check-in', 'weekly-review'):
            text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
            self.assertNotIn('```sql', text)
            self.assertNotIn('execute_sql', text)
            for block in re.findall(r'```json\n(.*?)```', text, re.S):
                self.assertNotIn('"user_id"', block)


if __name__ == '__main__':
    unittest.main()
