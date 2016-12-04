# Git Grep With Plumbing Commands

# Description:
An implementation of Git's grep command using plumbing commands.

# How To Use:
Call the script like so:

`λ python grep-tree-contents.py -p <git_repo> -t <tree_sha1> -s <search_string>`

## Arguments:
`git_repo`: The path string to the git repository to grep in. This path should be the the .git direcotry within the repo.
`tree_sha1`: This should be the tree's sha1 to search within.
`search_string`: The string to search for within the tree.

**Note:** The argument may come in any order as long as the flag is given.

# Example:
There is an example file `trialRun.txt` within the `src` directory. This was the output of the following command:

`$ λ python grep-tree-contents.py -p path\to\js-parsons\.git\ -t 4a218e -s example > trialRun.txt`
