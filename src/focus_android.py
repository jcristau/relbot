# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import re
from util import *


RELBRANCH_RE = re.compile(r"^releases_v(\d+)\.0$")


def get_focus_release_branches(repo):
    return [
        branch.name for branch in repo.get_branches() if RELBRANCH_RE.match(branch.name)
    ]


def major_version_from_focus_release_branch_name(branch_name):
    match = RELBRANCH_RE.match(branch_name)
    if match:
        return int(match[1])
    raise Exception(f"Unexpected release branch name: {branch_name}")


def get_recent_focus_versions(repo):
    major_focus_versions = [
        major_version_from_focus_release_branch_name(branch_name)
        for branch_name in get_focus_release_branches(repo)
    ]
    return sorted(major_focus_versions, reverse=False)[-2:]


def update_android_components_in_focus(ac_repo, focus_repo, author, debug, dry_run):
    update_android_components_nightly(
        ac_repo, focus_repo, author, debug, "main", dry_run
    )
    for version in get_recent_focus_versions(focus_repo):
        release_branch_name = f"releases_v{version}.0"
        try:
            update_android_components_release(
                ac_repo,
                focus_repo,
                "focus",
                release_branch_name,
                version,
                author,
                debug,
                dry_run,
            )
        except Exception as e:
            print(f"{ts()} Failed to update A-C in focus-android {version}: {str(e)}")
