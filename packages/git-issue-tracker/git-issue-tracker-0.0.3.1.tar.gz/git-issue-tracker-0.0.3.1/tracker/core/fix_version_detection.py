import logging
import re

from tracker.core.connectors.issue_handler import IssueHandler
from tracker.core.connectors.webhook_parser import RefChangeRequest
from tracker.core.git_repo import get_repo
from tracker.env import MERGE_PATTERN_SEARCH_TO_SKIP, ISSUE_TRACKER_PATTERN

logger = logging.getLogger("git:repository:process")
separator = "======="


def process_hook_data(request: RefChangeRequest, handler: IssueHandler):
    try:
        committed_issues = __find_merged_commits__(request)
        handler.handle(committed_issues, request)
    except Exception as e:
        logger.error("Error has happened either on processing ref change or post hook" + str(e))


def __find_merged_commits__(request: RefChangeRequest) -> [str]:
    repo = get_repo(request)

    included_issues = set()
    commits = repo.git.log('--pretty=Commit: %h Date: %ci%nAuthor: %ce%n%n%s%n%b%n{}'.format(separator),
                           '{}'.format(request.to_hash[:8]),
                           '^{}'.format(request.from_hash[:8]))
    for commit_str in re.split("{}\n?".format(separator), commits):
        if re.search(MERGE_PATTERN_SEARCH_TO_SKIP, commit_str) is not None:
            logger.info(
                "Found merge commit which skip further processing. Pattern {}".format(MERGE_PATTERN_SEARCH_TO_SKIP))
            logger.info(commit_str)
            break
        stripped_commit_msg = commit_str.strip()
        if stripped_commit_msg == '':
            continue

        logger.info("Parsed msg:\n{}".format(stripped_commit_msg))

        search = re.findall(ISSUE_TRACKER_PATTERN, commit_str)
        if len(search) > 0:
            for issue in search:
                included_issues.add(issue)

    return included_issues
