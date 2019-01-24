import sublime
import sublime_plugin


class GitRebaseOperationCommand(sublime_plugin.TextCommand):
    def run(self, edit, cmd):
        # validate command
        if cmd not in ("drop", "edit", "exec", "fixup", "pick", "reword", "squash"):
            return sublime.error_message("Invalid command")
        # validate scope
        for sel in self.view.sel():
            # find first word of current line
            pt = self.view.line(sel).a
            while self.view.substr(pt) in ' \t':
                pt += 1
            # replace first word with command string
            self.view.replace(edit, self.view.word(pt), cmd)
