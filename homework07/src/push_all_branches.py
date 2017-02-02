import sys
import argparse
import subprocess

# Assume byte encoding to be "utf-8" compatible.
global ENCODING
ENCODING = "utf-8"


def parser():
    """
        Parses argument from the command line.
    """
    parser = argparse.ArgumentParser(
        description="Push all branches on the local branches to the remote.")

    parser.add_argument(
        "-r", "--remote", help="Remote to push to", required=True)

    arguments = parser.parse_args()

    return arguments


def clean_git_branch_result(local_branches):
    """
        Cleans the results of the git_branch.

        Args:
            local_branches:         String of the git branch command.
    """
    # Constants.
    OUTPUT_DELIMITER = "\n"
    CURRENT_BRANCH_INDICATOR = "* "

    cleaned_branches = []
    for branch in local_branches.split(OUTPUT_DELIMITER):
        clean = branch.strip()

        if (clean[:len(CURRENT_BRANCH_INDICATOR)] == CURRENT_BRANCH_INDICATOR):
            cleaned_branches.append(clean[len(CURRENT_BRANCH_INDICATOR):])
        else:
            cleaned_branches.append(branch.strip())

    return cleaned_branches


def git_branch():
    """
        Returns the local branches.
    """
    local_branches = subprocess.run(["git", "branch"], stdout=subprocess.PIPE)
    return clean_git_branch_result(local_branches.stdout.decode(ENCODING).strip())


def clean_git_ls_remote(remotes):
    """
        Cleans the output of git ls-remote

        Args:
            remotes:        String of git ls-remote output.
        Returns:
            List of remote's branches base name.
    """
    # Constants.
    REMOTE_OUTPUT_DELIMITER = "\t"
    BRANCH_NAME_INDEX = 1
    BRANCH_BASE_NAME_INDEX = -1
    BRANCH_NAME_DELIMITER = "/"

    # Clean the input.
    remote_branches = []
    for remote in remotes:
        remote_branch = remote.split(REMOTE_OUTPUT_DELIMITER)[
            BRANCH_NAME_INDEX].strip()
        remote_branches.append(remote_branch.split(
            BRANCH_NAME_DELIMITER)[BRANCH_BASE_NAME_INDEX])

    return remote_branches


def git_ls_remote(remote):
    """
        Returns the output of git ls-remote --heads <remote>

        Args:
            remote:         String of remote repository.
    """

    ls_remote = subprocess.run(
        ["git", "ls-remote", "--heads", remote], stdout=subprocess.PIPE)
    return clean_git_ls_remote(ls_remote.stdout.decode(ENCODING).strip().split("\n"))


def compute_diff(local_branches, remote_branches):
    """
        Get the set difference of local_branches - remote_branches.

        Args:
            local_branches:         List of local branches.
            remote_branches:        List of remote_branches.
        Returns:
            List of elements in the set difference of local_branches - remote_branches.

    """
    return list(set(local_branches) - set(remote_branches))


def git_push(remote, branch_name):
    """
        Executes git push <remote> <src>:<dst>

        Args:
            remote:         String of remote repository.
            branch_name:    String of local branch to push to remote repository.
        Returns:
            Nothing.
    """
    subprocess.run(
        ["git", "push", remote, "{0}:{1}".format(branch_name, branch_name)])


def push_to_remote(branches, remote):
    """
        Push each branches branch to the remote repository.

        Args:
            branches:               List of local branches to push.
            remote:                 String of remote repository to push to.
        Returns:
            Nothing.
    """
    for branch_name in branches:
        git_push(remote, branch_name)


def main():
    """
        Driver Function.
    """
    # Grab CLI arguments.
    arguments = parser()

    # Get the branches existing in the local repo and the remote repo.
    local_branches = git_branch()
    remote_branches = git_ls_remote(arguments.remote)

    # Compute diff and push them to the remote.
    diff = compute_diff(local_branches, remote_branches)
    push_to_remote(diff, arguments.remote)


if __name__ == "__main__":
    main()
