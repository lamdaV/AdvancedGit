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
        "-p", "--path", help="The path to the git repo.", required=True)
    parser.add_argument(
        "-t", "--tree", help="The SHA1 of a git tree in the local repo.", required=True)
    parser.add_argument(
        "-s", "--search", help="A string to search for within the given tree.", required=True)

    arguments = parser.parse_args()

    return arguments


def git_cat_file(git_dir, sha1_hash):
    """
        Run the git_cat_file command.

        Args:
            git_dir:    The string of the git directory to run this command on.
            sha1_hash:  The hash to run the cat-file command on.

        Returns:
            The byte stream output of the cat-file command.
    """
    cat_file_command = subprocess.run(["git", "--git-dir", git_dir, "cat-file", "-p",
                                       sha1_hash], stdout=subprocess.PIPE)

    return cat_file_command.stdout


def clean_results(results):
    """
        Get the file_type and sha1_hash from the results.

        Args:
            results:    A list of byte strings from git_cat_file.

        Returns:
            A list of tuples (b"file_type", b"sha1_hash").
    """
    # Constants.
    LAST_INDEX = -1
    SHA1_INDEX = 0
    TYPE_INDEX = 1

    # Grab the file type and sha1_hash.
    clean = []
    for result in results:
        if (len(result) != 0):
            result_list = result.split(b" ")
            file_type = result_list[TYPE_INDEX]
            sha1_hash = result_list[LAST_INDEX].split(b"\t")[SHA1_INDEX]
            clean.append((file_type, sha1_hash))

    return clean


def search_for_string(contents, search_string):
    """
        Search for strings in the given contents.

        Args:
            contents:       A byte string to parse.
            search_string:  The string to search for in the contents.

        Returns:
            A list of strings containing the search_string.
    """
    # Split the content and encode search_string to a byte.
    lines = contents.split(b"\n")
    search_byte = search_string.encode()

    # Search line-by-line.
    results = []
    for line in lines:
        elements = line.split(b" ")
        if (search_byte in line):
            results.append(line.decode(ENCODING))

    return results


def git_grep(result_list, git_dir, search_string):
    """
        Perform the grep operation.

        Args:
            result_list:    A list of tuples (b"file_type", b"sha1_hash").
            git_dir:        A string of the git directory to perform the grep search on.
            search_string:  A string to search for.

        Returns:
            A list of lines containing the search_string.
    """
    # Constants.
    TYPE_INDEX = 0
    SHA1_INDEX = 1

    # Main loop.
    line_with_string = []
    for result in result_list:
        # Grab arguments from result.
        file_type = result[TYPE_INDEX]
        sha1_hash = result[SHA1_INDEX]

        # Perform operation on SHA1 hash file type.
        if (file_type == b"blob"):
            contents = git_cat_file(git_dir, sha1_hash.decode(ENCODING))
            line_with_string += search_for_string(contents, search_string)
        else:  # There are either blobs or trees
            results = clean_results(git_cat_file(
                git_dir, sha1_hash.decode(ENCODING)).split(b"\n"))
            line_with_string += git_grep(results, git_dir, search_string)

    return line_with_string


def result_printer(results):
    """
        Prints results line-by-line without extra spaces.

        Args:
            results: A list of string results.

        Returns:
            None.
    """
    for result in results:
        print(result)


def main():
    """
        Driver method.
    """
    # Grab arguments from the command line.
    arguments = parser()

    # Perform grep operations.
    results = clean_results(git_cat_file(
        arguments.path, arguments.tree).split(b"\n"))
    results = git_grep(results, arguments.path, arguments.search)

    # Print results line-by-line stripped of extra spaces.
    result_printer(results)

if __name__ == "__main__":
    main()
