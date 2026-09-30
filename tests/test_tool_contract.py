"""Verify Coach Cadence uses only the narrow Workout Tracker MCP contract."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LIVE_SKILLS = {
    'program-workout': {
        'get_athlete_context', 'get_workout_history', 'publish_workout',
        'get_programmed_workout'},
    'review-program': {'list_programmed_workouts', 'get_programmed_workout'},
    'morning-check-in': {'list_programmed_workouts', 'reschedule_programmed_workout'},
    'weekly-review': {'list_programmed_workouts'},
}
ALLOWED_TOOLS = {
    'get_athlete_context', 'get_workout_history', 'publish_workout',
    'list_programmed_workouts', 'get_programmed_workout',
    'reschedule_programmed_workout',
}


class ToolContractTests(unittest.TestCase):
    def skill_text(self, name):
        return (ROOT / 'skills' / name / 'SKILL.md').read_text()

    def test_live_skills_name_required_tools(self):
        for skill, tools in LIVE_SKILLS.items():
            text = self.skill_text(skill)
            for tool in tools:
                self.assertIn(f'`{tool}`', text, f'{skill} must call {tool}')

    def test_live_skills_contain_no_raw_database_access(self):
        for skill in LIVE_SKILLS:
            text = self.skill_text(skill).lower()
            self.assertNotIn('execute_sql', text, skill)
            self.assertNotIn('```sql', text, skill)
            self.assertNotRegex(text, r'\b(select|insert|update|delete)\s+(from|into|workout\.)')

    def test_json_examples_are_valid_and_never_accept_user_id(self):
        for skill in LIVE_SKILLS:
            text = self.skill_text(skill)
            for block in re.findall(r'```json\n(.*?)```', text, re.S):
                value = json.loads(block)
                self.assertNotIn('user_id', value, skill)

    def test_reference_allows_exact_named_tool_set(self):
        text = (ROOT / 'references' / 'ATHLETE.md').read_text()
        listed = set(re.findall(r'^- `([a-z_]+)` —', text, re.M))
        self.assertEqual(listed, ALLOWED_TOOLS)
        self.assertIn('do not accept\na `user_id` argument', text)
        self.assertIn('Do not use `execute_sql`', text)

    def test_identity_is_checked_on_every_data_flow(self):
        for skill in LIVE_SKILLS:
            text = self.skill_text(skill)
            self.assertIn('athlete_id', text, skill)

    def test_publish_contract_is_atomic_and_idempotent(self):
        text = self.skill_text('program-workout')
        self.assertIn('one transaction', text)
        self.assertIn('request_id', text)
        self.assertIn('do not generate a new ID after a timeout', text)
        self.assertIn('target_duration_secs', text)
        self.assertIn('is_per_side', text)


if __name__ == '__main__':
    unittest.main()
