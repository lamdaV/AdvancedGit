import sys
import argparse
import subprocess
import tempfile
import shutil
import os.path

# Assume byte encoding to be "utf-8" compatible.
global ENCODING
ENCODING = "utf-8"


def parser():
    """
        Parses argument from the command line.
    """
    parser = argparse.ArgumentParser(description="git grep tree contents.")

    parser.add_argument(
        "-c", "--commit_hash", help="SHA1 Hash of commit to revert back to.", required=True)
    parser.add_argument(
        "-f", "--file", help="File path to save.", required=True)

    arguments = parser.parse_args()

    return arguments


def revert(commit_hash, filepath):
    """
        Performs a git reset --hard to a particular commit but keeps a particular file of the current commit.

        Args:
            commit_hash:    SHA1 commit hash
            filepath:       String of the filepath to save.

        Returns:
            None
    """
    # Use a temp directory to save the particular file.
    with tempfile.TemporaryDirectory() as temp_directory:
        shutil.copy(filepath, temp_directory)

        reset_result = subprocess.run(
            ["git", "reset", "--hard", commit_hash], stdout=subprocess.PIPE)

        print(reset_result.stdout.decode(ENCODING))

        file_name = os.path.basename(filepath)
        directory = os.path.dirname(filepath)

        shutil.copy(os.path.join(temp_directory, file_name), directory)


def main():
    """
        Driver Function.
    """
    arguments = parser()

    revert(arguments.commit_hash, arguments.file)


if __name__ == "__main__":
    main()
