# Git Scripting with Porcelain Commands

# Description:
## revert_except_file
  This script takes a commit SHA1 hash and a path to a file that should be preserved when reverting to a previous commit. The script will save the specified folder, reset to the specified commit, and restore the specified folder. This uses Pythons library for saving to a TemporaryDirectory that will be automatically deleted once the code completes executing.

## smash_last_two
  This script takes no arguments. It will simply combine the last two commits into one commit with a commit message of "SMASH".

## one_step_back
  This script also takes no arguments. Given a git repo with files that are staged and unstaged, this will do 4 things:
    1. All unstaged files are stashed.
    2. HEAD will move back to the previous commit.
    3. The current commit's files are now staged.
    4. All staged files are now unstaged.

# How To Use:
## revert_execpt_file
  `λ python \path\to\revert_except_file.py -c <commit_hash> -f <file_save>`

### Arguments:
  - `commit_hash`: Commit SHA1 Hash to revert to.
  - `file_save`: Path to file within repo to save.

**Note:** The argument may come in any order as long as the flag is given.

## smash_last_two
  `λ python \path\to\smash_last_two.py`

## one_step_back
  `λ python \path\to\one_step_back.py`
