"""Exercise actual skill SQL in an explicitly named disposable local Postgres DB.

PGHOST=/absolute/socket/path PGPORT=55439 PGDATABASE=cadence_contract_test \
python3 -m unittest discover -s tests -p test_sql_contract.py -v
"""
import os
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
WIFE = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'
CHRIS = 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb'
ROUTINE = 'cccccccc-cccc-4ccc-8ccc-cccccccccccc'
PLAN = 'dddddddd-dddd-4ddd-8ddd-dddddddddddd'
OTHER_PLAN = 'eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee'
SESSION = 'ffffffff-ffff-4fff-8fff-ffffffffffff'
VALUES = {'user_id': WIFE, 'routine_type_id': ROUTINE, 'plan_id': PLAN,
          'date': '2026-09-28', 'overall_notes': "Athlete''s own program",
          'section': 'main', 'position': '1', 'exercise': 'Side plank',
          'variant': 'Side plank', 'sets': '2', 'reps_or_null': 'NULL',
          'weight_or_null': 'NULL', 'seconds_or_null': '30',
          'true_or_false': 'true', 'notes': 'Per side'}


def query_blocks(name):
    text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
    blocks = re.findall(r'```sql\n(.*?)```', text, re.S)
    return [re.sub(r'<([^>]+)>', lambda m: VALUES[m[1]], q) for q in blocks]


@unittest.skipUnless(os.getenv('PGDATABASE') == 'cadence_contract_test'
                     and os.getenv('PGHOST', '').startswith('/'),
                     'requires disposable local cadence_contract_test database')
class SQLContractTests(unittest.TestCase):
    def test_publish_review_and_reschedule_two_athletes(self):
        publish = next(q for q in query_blocks('program-workout') if q.startswith('WITH plan'))
        actuals = next(q for q in query_blocks('review-program') if 'FROM workout.workout_sets ws' in q)
        reschedule = next(q for q in query_blocks('morning-check-in') if 'UPDATE workout.programmed_workouts' in q)
        sql = f"""
BEGIN;
CREATE SCHEMA workout;
CREATE TABLE workout.workout_routine_types (id uuid PRIMARY KEY, name text);
CREATE TABLE workout.user_routines (id uuid DEFAULT gen_random_uuid(), user_id uuid, routine_type_id uuid, name text, is_active boolean);
CREATE TABLE workout.programmed_workouts (id uuid PRIMARY KEY, user_id uuid, routine_type_id uuid, status text, coach_notes text, programmed_at timestamptz, scheduled_for date, updated_at timestamptz, completed_workout_session_id uuid);
CREATE TABLE workout.programmed_workout_sets (id uuid DEFAULT gen_random_uuid(), programmed_workout_id uuid REFERENCES workout.programmed_workouts, slot_label text, position int, exercise_name text, selected_variant text, target_sets int, target_reps int, target_weight_lbs numeric, target_duration_secs int, is_per_side boolean, coach_notes text);
CREATE TABLE workout.workout_sessions (id uuid PRIMARY KEY, user_id uuid, date timestamptz, deleted_at timestamptz);
CREATE TABLE workout.workout_sets (user_id uuid, session_id text, routine_type_id uuid, exercise_name text, variant text, set_number int, weight_lbs numeric, reps int, duration_secs int, notes text, date timestamptz, deleted_at timestamptz);
INSERT INTO workout.workout_routine_types VALUES ('{ROUTINE}', 'Gym');
INSERT INTO workout.user_routines(user_id,routine_type_id,name,is_active) VALUES ('{WIFE}','{ROUTINE}','Gym',true), ('{CHRIS}','{ROUTINE}','Gym',true);
INSERT INTO workout.programmed_workouts(id,user_id,routine_type_id,status,scheduled_for) VALUES ('{OTHER_PLAN}','{CHRIS}','{ROUTINE}','pending','2026-01-01');
{publish}
DO $$ BEGIN
IF (SELECT count(*) FROM workout.programmed_workout_sets WHERE programmed_workout_id='{PLAN}') <> 1 THEN RAISE EXCEPTION 'Expected one complete plan'; END IF;
IF (SELECT user_id FROM workout.programmed_workouts WHERE id='{PLAN}') <> '{WIFE}' THEN RAISE EXCEPTION 'Wrong plan owner'; END IF;
END $$;
INSERT INTO workout.workout_sessions VALUES ('{SESSION}','{WIFE}',now(),NULL);
UPDATE workout.programmed_workouts SET status='completed',completed_workout_session_id='{SESSION}' WHERE id='{PLAN}';
INSERT INTO workout.workout_sets(user_id,session_id,routine_type_id,exercise_name,variant,set_number,duration_secs,date) VALUES ('{WIFE}',upper('{SESSION}'),'{ROUTINE}','Side plank','Side plank',1,30,now()), ('{CHRIS}',upper('{SESSION}'),'{ROUTINE}','Other athlete','Other athlete',1,999,now());
CREATE TEMP TABLE actuals AS {actuals.rstrip().rstrip(';')};
DO $$ BEGIN
IF (SELECT count(*) FROM actuals) <> 1 OR (SELECT duration_secs FROM actuals LIMIT 1) <> 30 THEN RAISE EXCEPTION 'Actuals ownership or UUID/text join failed'; END IF;
END $$;
UPDATE workout.programmed_workouts SET status='pending' WHERE id='{PLAN}';
{reschedule}
DO $$ BEGIN
IF (SELECT scheduled_for FROM workout.programmed_workouts WHERE id='{OTHER_PLAN}') <> '2026-01-01'::date THEN RAISE EXCEPTION 'Other athlete was rescheduled'; END IF;
IF (SELECT scheduled_for FROM workout.programmed_workouts WHERE id='{PLAN}') <> CURRENT_DATE THEN RAISE EXCEPTION 'Athlete was not rescheduled'; END IF;
END $$;
"""
        # Parse and execute every remaining read template against the same schema.
        for name in ('program-workout', 'review-program', 'weekly-review', 'morning-check-in'):
            for query in query_blocks(name):
                if query.lstrip().startswith('SELECT'):
                    sql += '\n' + query
        sql += '\nROLLBACK;\n'
        result = subprocess.run(['psql', '-X', '-v', 'ON_ERROR_STOP=1'], input=sql,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
