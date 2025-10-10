import logging
import git

def pull_git_info(absolute_path: str) -> dict[str, str] | None:
    """
    Retrieve basic Git metadata from a repository at the given path.

    Extracts:
        - Current commit hash
        - Active branch name
        - Author name and email
        - Commit timestamp (formatted)

    Args:
        absolute_path: Path to the root of the Git repository.

    Returns:
        A dictionary with Git metadata if successful, or None if the path is not a valid Git repository.
    """
    try:
        # Initialize the Git repository object
        repo = git.Repo(absolute_path)

        # Get the latest commit and active branch
        commit = repo.head.commit
        branch = repo.active_branch.name

        # Build and return metadata dictionary
        return {
            "commit": commit.hexsha,
            "branch": branch,
            "author": f"{commit.author.name} <{commit.author.email}>",
            "date": commit.committed_datetime.strftime('%a %b %d %H:%M:%S %Y %z')
        }

    except git.exc.InvalidGitRepositoryError:
        logging.warning("No valid Git repository found at: %s", absolute_path)
        return None
    except Exception as e:
        logging.error("Unexpected error while retrieving Git info from %s: %s", absolute_path, e)
        return None