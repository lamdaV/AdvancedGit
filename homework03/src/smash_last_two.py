import subprocess


def smash():
    """
        Smash the last two commits into one commit.
    """
    # Move HEAD back 2 commits with files still in index.
    subprocess.run(["git", "reset", "--soft", "HEAD~2"])
    # commit past 2 commits as 1.
    subprocess.run(["git", "commit", "-m", "SMASH"])


def main():
    """
        Driver Function.
    """
    smash()


if __name__ == "__main__":
    main()
