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
        "-u", "--use", help="SHA1 commit preference hash.", required=True)
    parser.add_argument("-c", "--commitify",
                        help="SHA1 commit comment hash.", required=True)
    parser.add_argument(
        "-b", "--branch", help="Output branch name", required=True)
    parser.add_argument(
        "-p", "--prefix", help="Prefix String of the comment.", required=True)

    arguments = parser.parse_args()

    return arguments


def evaluate_file(changed_file, prefix):
    """
        Evaluates the changed_file and outputs the list of new lines for the
        file.

        Args:
            changed_file:           The file to be evaluated.
            prefix:                 The comment prefix of the commitify_branch.

        Returns:
            List of new lines for the changed_file.
    """
    # Constants.
    PREFERENCE_ARROW = ">>>>>>>"
    DIVIDER = "======="
    COMMITIFY_ARROW = "<<<<<<<"

    commitify_flag = False
    new_file_lines = []
    with open(changed_file, "r") as file_lines:
        for line in file_lines:
            if ((PREFERENCE_ARROW in line) or (COMMITIFY_ARROW in line)):
                commitify_flag = False
                continue
            elif (DIVIDER in line):
                commitify_flag = True
                continue

            if (commitify_flag):
                new_file_lines.append(prefix + line)
            else:
                new_file_lines.append(line)

    return new_file_lines


def write_new_file(changed_file, new_file_lines):
    """
        Overwrite the changed_file with a list of lines.

        Args:
            changed_file:       The file name to overwrite.
            new_file_lines:     The List of lines to write.

        Returns:
            Nothing.
    """
    with open(changed_file, "w") as file_lines:
        for line in new_file_lines:
            file_lines.write(line)


def update_files(changed_files, prefix):
    """
        Scans a list of files and resolves the merge changes.

        Args:
            changed_files:      The list of files that have been changed.
            prefix:             The comment prefix to append to the commitify
                                branch.

        Returns:
            Nothing.
    """
    for changed_file in changed_files:
        if (changed_file == ""):
            break

        new_file_lines = evaluate_file(changed_file, prefix)
        write_new_file(changed_file, new_file_lines)


def auto_merge(preference_branch, commitify_branch, output_branch, prefix):
    """
        Performs the auto_merge function.

        Args:
            preference_branch:      The branch to take preference of changes.
            commitify_branch:       The branch to comment out changes with
                                    supplied prefix.
            output_branch:          The branch where to output the merge files.
            prefix:                 The prefix for the comment of the supplied
                                    comment.

        Returns:
            Nothing.
    """
    # Switch to output_branch.
    subprocess.run(["git", "checkout", output_branch])

    # Begin to merge branches.
    subprocess.run(["git", "merge", preference_branch, commitify_branch])

    # Get changed files name
    changed_files_command = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=U"], stdout=subprocess.PIPE)
    changed_files = changed_files_command.stdout.decode(ENCODING).split("\n")

    update_files(changed_files, prefix)


def main():
    """
        Driver Function.
    """
    arguments = parser()

    auto_merge(arguments.use, arguments.commitify,
               arguments.branch, arguments.prefix)


if __name__ == "__main__":
    main()
