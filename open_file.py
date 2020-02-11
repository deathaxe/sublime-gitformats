import os
import sys

import sublime_plugin

__all__ = ["GitOpenFileCommand"]

GIT_SEP = os.sep + ".git" + os.sep


if (
    sys.version < "3.8"
    and sys.platform == "win32"
    and sys.getwindowsversion().major >= 6
):

    from nt import _getfinalpathname

    def realpath(path):
        """Resolve symlinks and return real path to file.

        Note:
            This is a fix for the issue of `os.path.realpath()` not to resolve
            symlinks on Windows as it is an alias to `os.path.abspath()` only.
            see: http://bugs.python.org/issue9949

            This fix applies to local paths only as symlinks are not resolved
            by _getfinalpathname on network drives anyway.

            Also note that _getfinalpathname in Python 3.3 throws
            `NotImplementedError` on Windows versions prior to Windows Vista,
            hence we fallback to `os.path.abspath()` on these platforms.

        Arguments:
            path (string): The path to resolve.

        Returns:
            string: The resolved absolute path if exists or path as provided
                otherwise.
        """
        try:
            if path:
                real_path = _getfinalpathname(path)
                if real_path[5] == ":":
                    # Remove \\?\ from beginning of resolved path
                    return real_path[4:]
                return os.path.abspath(path)
        except FileNotFoundError:
            pass
        return path


else:

    def realpath(path):
        """Resolve symlinks and return real path to file.

        Arguments:
            path (string): The path to resolve.

        Returns:
            string: The resolved absolute path.
        """
        return os.path.realpath(path) if path else None


def git_path(path):
    return os.path.join(path, ".git")


def parse_gitfile(gitfile):
    try:
        with open(gitfile) as file:
            text = file.read()
            if text.startswith("gitdir: "):
                return realpath(text[len("gitdir: ") :].strip())
    except OSError:
        pass
    return gitfile


def is_work_tree(path):
    """Check if 'path' is a valid git working tree.

    A working tree contains a `.git` directory or file.

    Arguments:
        path (string): The path to check.

    Returns:
        bool: True if path contains a '.git'
    """
    return path and os.path.exists(git_path(path))


def rev_parse_commondir(file_path):
    """Return the .git directory of the file's worktree's super repository.

    This is a local alternative to calling the git command:

        git rev-parse --git-common-dir

    Arguments:
        file_path (string): a absolute or relative file path

    Returns:
        string: The .git directory of the file_path's worktree's super repository or
        None: if the file is not located in a repository.
    """
    path = rev_parse_gitdir(file_path)
    if path and not path.endswith(".git"):
        start = path.find(GIT_SEP)
        if start > -1:
            return path[: start + len(GIT_SEP) - 1]
    return path


def rev_parse_gitdir(file_path):
    """Return the .git directory of the file's worktree.

    This is a local alternative to calling the git command:

        git rev-parse --absolute-git-dir

    Arguments:
        file_path (string): a absolute or relative file path

    Returns:
        string: The .git directory of the file_path's worktree or
        None: if the file is not located in a repository.
    """
    path = rev_parse_worktree(file_path)
    if path:
        return parse_gitfile(git_path(path))
    return path


def rev_parse_super_worktree(file_path):
    """Return the root directory of the file's worktree's super repository.

    This is a local alternative to calling the git command:

        git rev-parse --show-superproject-working-tree

    Arguments:
        file_path (string): a absolute or relative file path

    Returns:
        string: The root directory of the file_path's worktree's super repository or
        None: if the file is not located in a repository.
    """
    path = rev_parse_gitdir(file_path)
    if path:
        if path.endswith(".git"):
            return os.path.split(path)[0]
        else:
            return path.split(GIT_SEP)[0]
    return path


def rev_parse_worktree(file_path):
    """Return the toplevel directory of the file's worktree.

    This is a local alternative to calling the git command:

        git rev-parse --show-toplevel

    Arguments:
        file_path (string): a absolute or relative file path

    Returns:
        string: The worktree root directory or
        None: if the file is not located in a repository.
    """
    if file_path:
        path, name = os.path.split(realpath(file_path))
        while path and name:
            if is_work_tree(path):
                return path
            path, name = os.path.split(path)
    return None


class GitOpenFileCommand(sublime_plugin.TextCommand):

    variables = {
        "$GIT_COMMON_DIR": rev_parse_commondir,
        "$GIT_DIR": rev_parse_gitdir,
        "$GIT_SUPER_WORK_TREE": rev_parse_super_worktree,
        "$GIT_WORK_TREE": rev_parse_worktree,
    }

    def is_enabled(self):
        return rev_parse_worktree(self.view.file_name()) is not None

    def run(self, edit, name, syntax=None):
        file_path = name
        for var, expander in self.variables.items():
            if var in file_path:
                abspath = expander(self.view.file_name())
                if abspath:
                    file_path = file_path.replace(var, abspath)
                break

        view = self.view.window().open_file(file_path)
        if syntax:
            view.assign_syntax(syntax)
