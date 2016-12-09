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



def main():
    arguments = parser()
    print(arguments)

if __name__ == "__main__":
    main()
