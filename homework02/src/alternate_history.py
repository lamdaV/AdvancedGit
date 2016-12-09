import sys
import argparse
import subprocess


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


def git_commit_tree(tree, parent, message):
    commit_tree = subprocess.run(["git", "commit-tree", tree, "-p", parent, "-m", message], stdout=subprocess.PIPE);
    return commit_tree

def generate_alternate_history(trees, branch_name):

    # Source for fixed number format: https://stackoverflow.com/questions/17118071/python-add-leading-zeroes-using-str-format
    message = "alternate_history{0:0>2}"
    for k in xrange(0, -1, -1):
        git_commit_tree(trees[k - 1], trees[k], message.format(k))

def main():
    arguments = parser()
    print(arguments)



if __name__ == "__main__":
    main()
