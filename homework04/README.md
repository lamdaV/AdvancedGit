# Git Merge Toy Tool

# Description:

## auto_merge_with_comments

This is a toy tool. It assumes the following:

```
- Special conflicted lines (e.g. >>>>>) will never arise naturally in the files.
- The repo has strictly EITHER safe auto-merges or files that are in a conflicted editing state.
```

# How To Use:

`λ python path\to\auto_merge_with_comments.py -u <preference_branch> -c <commented_branch> -b <output_branch> -p <prefix>`

# Arguments:

- `preference_branch`: Branch in which changes are taken and left uncommented.
- `commented_branch`: Branch in which changes are taken and commented with supplied prefix string.
- `output_branch`: Branch in which the merge is stored on.
- `prefix`: String to comment the commented branch changes.

**Note:** The argument may come in any order as long as the flag is given.
