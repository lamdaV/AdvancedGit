import sys
import argparse
import subprocess


def move_back():
    """
        Move Back is defined by 4 operations:
            (1) Head should become the previous commit
            (2) What was last commit before the script was run should become staged changes to head
            (3) What changes were staged before the script was run should become unstaged
            (4) Any unstaged changes before the script was run should be stashed
    """
    # Stash unstaged changes only (4).
    subprocess.run(["git", "stash", "--keep-index", "-u"])
    # Unstage staged changes (3).
    subprocess.run(["git", "reset"])
    # Go back one commit (1) (2) (3).
    subprocess.run(["git", "reset", "--soft", "HEAD~"])


def main():
    """
        Driver Function.
    """
    move_back()


if __name__ == "__main__":
    main()
