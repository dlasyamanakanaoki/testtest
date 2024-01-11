import urllib.request
import sys
import json

RULESET_NAME = 'default branch protection'


def craete_default_branch_protection_ruleset(repository_name, secret_token):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {secret_token}',
    }
    url = f'https://api.github.com/repos/{repository_name}/rulesets'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        rulesets = json.loads(res.read())
    is_ruleset_exists = False
    for ruleset in rulesets:
        if ruleset['name'] == RULESET_NAME:
            is_ruleset_exists = True
            break
    if is_ruleset_exists:
        print(f'ruleset "{RULESET_NAME}" already exists')
    else:
        data = {
            "name": RULESET_NAME,
            "target": "branch",
            "enforcement": "active",
            "conditions": {
                "ref_name": {
                    "include": [
                        "~DEFAULT_BRANCH"
                    ],
                    "exclude": []
                }
            },
            "rules": [
                {
                    "type": "deletion",
                },
                {
                    "type": "pull_request",
                    "parameters": {
                        "dismiss_stale_reviews_on_push": False,
                        "require_code_owner_review": False,
                        "require_last_push_approval": False,
                        "required_approving_review_count": 0,
                        "required_review_thread_resolution": False,
                    }
                },
                {
                    "type": "non_fast_forward",
                },
            ]
        }
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as res:
                ruleset = json.loads(res.read())
        except urllib.error.HTTPError as e:
            print(e.read())


if __name__ == '__main__':
    repository_name = sys.argv[1]
    secret_token = sys.argv[2]
    craete_default_branch_protection_ruleset(repository_name, secret_token)
    sys.exit(0)
