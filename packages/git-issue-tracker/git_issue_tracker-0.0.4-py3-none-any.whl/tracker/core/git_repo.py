import logging
import shutil

import git
from git import Repo

from tracker.env import GIT_USER_PASS
from tracker.core.connectors.webhook_parser import RefChangeRequest

logger = logging.getLogger("git:repository:init_repo")

def get_repo(request: RefChangeRequest) -> Repo:
    repo_path = '/tmp/tracker_{}'.format(request.repo_name)

    def checkout_repo(path):
        r: Repo = None
        try:
            r = git.Repo(path)
        except Exception as e:
            logger.error(e)

        if r is None:
            logger.info("Cloning with GitPython over https with the username and token")
            try:
                r = git.Repo.clone_from("https://{}:{}@{}".format(
                    GIT_USER_PASS["username"],
                    GIT_USER_PASS["token"],
                    request.repo_link.split("https://")[1]), path)
            except Exception as e:
                logger.error(e)
        return r

    repo = checkout_repo(repo_path)
    try:
        logger.info("Fetch changes from remote")
        repo.git.fetch()
    except Exception as e:
        try:
            logger.info("Remove folder with project due to error in git tree {}".format(repo_path))
            shutil.rmtree(repo_path)
        except OSError as e:
            logger.error("Error: {} : {}".format(repo_path, e.strerror))
        checkout_repo(repo_path)

    return repo
