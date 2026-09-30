#!/usr/bin/env python3
"""Load only the connected athlete workspace; never fall back to personal data."""
import json
from pathlib import Path
import sys
from uuid import UUID


def valid_identity(config):
    if not isinstance(config, dict) or not isinstance(config.get('display_name'), str):
        return False
    if not config['display_name'].strip():
        return False
    try:
        if UUID(config['user_id']).int == 0:
            return False
        routines = config.get('routine_type_ids')
        if not isinstance(routines, dict) or not routines:
            return False
        for label, value in routines.items():
            if not isinstance(label, str) or not label.strip() or UUID(value).int == 0:
                return False
    except (ValueError, TypeError, KeyError, AttributeError):
        return False
    return True


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict) or not isinstance(payload.get('cwd'), str):
        return 0
    workspace = Path(payload['cwd'])
    config_path = workspace / 'athlete-config.json'
    # Legacy marker allows existing users to migrate, but never bypasses setup.
    if not config_path.is_file() and not (workspace / 'source-of-truth.md').is_file():
        return 0
    try:
        config = json.loads(config_path.read_text())
    except (OSError, ValueError):
        config = None
    if not valid_identity(config):
        print('Training setup required. Run onboarding in the connected folder. '
              'Read references/ATHLETE.md. Only get_athlete_context is allowed until '
              'this athlete has a verified account UUID and routine mapping; do not '
              'recommend training yet.')
    elif any(not (workspace / name).is_file() for name in
             ('source-of-truth.md', 'user-profile.md', 'strength-template.md')):
        print('Run onboarding for this athlete, starting with their current gym program '
              'and suggested changes. Never load another athlete profile as a fallback.')
    else:
        print('Read references/ATHLETE.md and the connected athlete-config.json, '
              'then run morning-check-in for this athlete only.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
