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
    parser = argparse.ArgumentParser(description="git grep tree contents.")

    parser.add_argument(
        "-t", "--trees", help="A list of tree SHA1 hashes to create the alternate history.", nargs="+", required=True)
    parser.add_argument(
        "-n", "--name", help="A name for the new branch", required=True)

    arguments = parser.parse_args()

    return arguments


def git_commit_tree(tree, message, parent=None):
    """
        Performs a git commit-tree.

        Args:
            tree:       String SHA1 Hash of the tree.
            message:    String of the message associated with this commit.
            parent:     Optional: String of the SHA1 Hash of the parent commit.

        Returns:
            A byte encoded commit SHA1 Hash.
    """
    command = ["git", "commit-tree", "-m", message, tree]
    if (parent):
        command += ["-p", parent]

    commit_tree = subprocess.run(command, stdout=subprocess.PIPE)
    return commit_tree.stdout


def git_update_ref(branch_name, commit_hash):
    """
        Performs a git update-ref.

        Args:
            branch_name:        String of the new branch with alternate history.
            commit_hash:        The primary Commit SHA1 hash.

        Returns
    """
    update_ref = subprocess.run(["git", "update-ref", "-m", "alternate_history_generated",
                                 "refs/heads/" + branch_name, commit_hash], stdout=subprocess.PIPE)
    return update_ref.stdout


def generate_alternate_history(trees, branch_name):
    """
        Generates the Alternate History.

        Args:
            trees:          List of SHA1 Tree strings
            branch_name:    String of the new branch with alternate history.
    """
    # Source for fixed number format:
    # https://stackoverflow.com/questions/17118071/python-add-leading-zeroes-using-str-format
    message = "alternate_history{0:0>2}"

    # Create the base Commit.
    commit_hash = git_commit_tree(trees[0], message.format(0))

    # Link each subsequent tree to the base Commit.
    for k in range(1, len(trees)):
        commit_hash = git_commit_tree(trees[k], message.format(
            k), commit_hash.decode(ENCODING).rstrip())

    # Perform the update_ref to create a new branch with alternate history.
    git_update_ref(branch_name, commit_hash.decode(ENCODING).rstrip())


def main():
    """
        Driver Function.
    """
    arguments = parser()

    print("[ INFO ]: Processing...", end="")
    generate_alternate_history(arguments.trees, arguments.name)
    print("completed")


if __name__ == "__main__":
    main()
