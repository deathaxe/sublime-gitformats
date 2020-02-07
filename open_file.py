import os

import sublime
import sublime_plugin

try:
    import sys

    if sys.version >= "3.8":
        # python 3.8 doesn't need the realpath patch
        raise AssertionError()

    if sys.getwindowsversion().major < 6:
        # Windows NT/2000/XP don't support the realpath patch
        raise AssertionError()

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


except (AttributeError, ImportError, AssertionError):

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
    return None


def is_work_tree(path):
    """Check if 'path' is a valid git working tree.

    A working tree contains a `.git` directory or file.

    Arguments:
        path (string): The path to check.

    Returns:
        bool: True if path contains a '.git'
    """
    return path and os.path.exists(git_path(path))


def rev_parse_toplevel(file_path):
    """Split the 'file_path' into working tree and relative path.

    The file_path is converted to a absolute real path and split into
    the working tree part and relative path part.

    Note:
        This is a local alternative to calling the git command:

            git rev-parse --show-toplevel

    Arguments:
        file_path (string): Absolute path to a file.

    Returns:
        A tuple of two the elements (working tree, file path).
    """
    if file_path:
        path, name = os.path.split(realpath(file_path))
        # files within '.git' path are not part of a work tree
        while path and name:
            if is_work_tree(path):
                return path
            path, name = os.path.split(path)
    return None


def rev_parse_gitdir(file_path):
    path = rev_parse_toplevel(file_path)
    if path:
        gitdir = git_path(path)
        path = parse_gitfile(gitdir) or gitdir
    return path


def rev_parse_commondir(file_path):
    path = rev_parse_gitdir(file_path)
    if path:
        worktree = rev_parse_toplevel(path)
        if worktree:
            path = git_path(worktree)
    return path


def init_variables(file_path):
    worktree = rev_parse_toplevel(file_path)
    if not worktree:
        return None

    gitdir = git_path(worktree)
    gitfile_content = parse_gitfile(gitdir)
    if gitfile_content:
        gitdir = gitfile_content
        super_worktree = rev_parse_toplevel(gitdir)
        commondir = git_path(super_worktree)
    else:
        super_worktree = worktree
        commondir = gitdir

    return {
        "GIT_COMMON_DIR": commondir,
        "GIT_DIR": gitdir,
        "GIT_SUPER_WORK_TREE": super_worktree,
        "GIT_WORK_TREE": worktree,
    }


class GitOpenFileCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return rev_parse_toplevel(self.view.file_name()) is not None

    def run(self, edit, name, syntax=None):
        variables = init_variables(self.view.file_name())
        file_path = sublime.expand_variables(name, variables)
        view = self.view.window().open_file(file_path)
        if syntax:
            view.assign_syntax(syntax)
