# Git Rebase Verbose

## Description:
This script will perform a rebase on the current branch with a supplied branch. It will print how commit hashes has transformed with their corresponding description.

It assumes the following:
  - All descriptions are unique.
  - Rebase will always succeed without errors.

## How To Use:
`λ python path\to\rebase_verbose.py -b <branch>`

### Arguments:
- `branch`: Branch to rebase with.

**Note:** The argument may come in any order as long as the flag is given.

## Example:
There is an example file `sample_output.txt` within the `src` directory. This was the output of the following command:

`λ python path\to\rebase_verbose.py -b ee6db14`
