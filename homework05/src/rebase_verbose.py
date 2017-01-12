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
    parser = argparse.ArgumentParser(description="auto merge with comments")

    parser.add_argument(
        "-b", "--branch", help="Branch or commit hash", required=True)

    arguments = parser.parse_args()

    return arguments


def git_log():
    """
        Performs a git log --online.
    """
    git_log = subprocess.run(
        ["git", "log", "--oneline"], stdout=subprocess.PIPE)
    return git_log.stdout.decode(ENCODING)


def parse_patch(patch):
    """
        Parse the patch into a list of tuples (Commit, Description).

        Args:
            patch:      Patch string to be parsed.

        Returns:
            List of tuples (Commit, Description).
    """
    # Constants.
    COMMIT_INDEX = 0
    DESCRIPTION_INDEX = 1
    DELIMITER = " "
    NUMBER_OF_SPLITS = 1

    # Parse the patch into a list of tuples (Commit, Description).
    patch_list = []
    lines = patch.split("\n")[:-1]
    for line in lines:
        values = line.split(DELIMITER, NUMBER_OF_SPLITS)
        patch_list.append((values[COMMIT_INDEX], values[DESCRIPTION_INDEX]))

    return patch_list


def git_rebase(branch):
    """
        Runs git rebase on the given branch

        Args:
            branch:     Branch or commit hash to perform rebase on.

        Returns:
            None.
    """
    subprocess.run(["git", "rebase", branch])


def build_verbose_text(pre_patch_list, post_patch_list, branch):
    """
        Builds the verbose text to be printed.

        Args:
            pre_patch_list:     List of tuples (commit_index, description) from pre-patch.
            post_patch_list:    List of tuples from post_patch.
            branch:             String of branch name or hash that was rebased to.

        Returns:
            String of verbose text.
    """
    # Constants.
    COMMIT_INDEX = 0
    DESCRIPTION_INDEX = 1

    # Build the String.
    builder = ""
    for k in range(len(post_patch_list)):
        post_line = post_patch_list[k]

        # Check if we have reached the given branch in the rebase.
        if (post_line[COMMIT_INDEX] == branch):
            builder += "{0} is the new base: {1}\n".format(
                post_line[COMMIT_INDEX], post_line[DESCRIPTION_INDEX])
            break

        # Find the matching description and build the pre becomes post String.
        for i in range(len(pre_patch_list)):
            pre_line = pre_patch_list[i]
            if (pre_line[DESCRIPTION_INDEX] == post_line[DESCRIPTION_INDEX]):
                builder += "{0} becomes {1}: {2}\n".format(pre_line[COMMIT_INDEX], post_line[
                    COMMIT_INDEX], pre_line[DESCRIPTION_INDEX])
                break

    return builder


def rebase_verbose(branch):
    """
        Perform a rebase verbose.

        Args:
            branch:     Branch to rebase to.

        Returns:
            The verbose rebase String.
    """
    pre_patch = git_log()
    pre_patch_list = parse_patch(pre_patch)

    git_rebase(branch)

    post_patch = git_log()
    post_patch_list = parse_patch(post_patch)

    return build_verbose_text(pre_patch_list, post_patch_list, branch)


def main():
    """
        Driver Function.
    """
    arguments = parser()
    print(rebase_verbose(arguments.branch))


if __name__ == "__main__":
    main()
