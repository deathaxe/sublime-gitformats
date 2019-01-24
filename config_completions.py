import sublime
import sublime_plugin

KEYS = {
    "add": ["ignoreErrors"],
    "alias": [],
    "am": ["keepcr, threeWay"],
    "apply": ["ignoreWhitespace", "whitespace"],
    "blame": ["blankBoundary", "date", "showEmail", "showRoot"],
    "branch": ["autoSetupMerge", "autoSetupRebase"],
    "branch.<name>": [
        "description", "merge", "mergeOptions", "pushRemote", "rebase", "remote",
    ],
    "commit": ["cleanup", "gpgSign", "status", "template", "verbose"],
    "color": [
        "branch", "branch.current", "branch.local", "branch.plain",
        "branch.remote", "branch.upstream", "decorate.current",
        "decorate.local", "decorate.plain", "decorate.remote",
        "decorate.upstream", "diff", "diff.current", "diff.local", "diff.plain",
        "diff.remote", "diff.upstream", "grep", "grep.current", "grep.local",
        "grep.plain", "grep.remote", "grep.upstream", "interactive",
        "interactive.current", "interactive.local", "interactive.plain",
        "interactive.remote", "interactive.upstream", "pager", "showBranch",
        "status", "status.current", "status.local", "status.plain",
        "status.remote", "status.upstream", "ui",
    ],
    "column": ["branch", "clean", "status", "tag", "ui"],
    "core": [
        "abbrev", "askPass", "attributesFile", "autocrlf", "bare",
        "bigFileThreshold", "checkStat", "commentChar", "compression",
        "createObject", "deltaBaseCacheLimit", "editor", "eol", "excludesFile",
        "fileMode", "filemode", "filesRefLockTimeout", "fsyncObjectFiles",
        "gitProxy", "hideDotFiles", "hooksPath", "ignoreCase", "ignoreStat",
        "logAllRefUpdates", "looseCompression", "notesRef", "packedGitLimit",
        "packedGitWindowSize", "packedRefsTimeout", "pager", "precomposeUnicode",
        "preferSymlinkRefs", "preloadIndex", "protectHFS", "protectNTFS",
        "quotePath", "repositoryFormatVersion", "safecrlf", "sharedRepository",
        "sparseCheckout", "splitIndex", "sshCommand", "symlinks", "trustctime",
        "untrackedCache", "warnAmbiguousRefs", "whitespace", "worktree",
    ],
    "credential": ["helper", "useHttpPath", "username", "ignoreSIGHUP"],
    "credential.<url>": ["helper", "useHttpPath", "username", "ignoreSIGHUP"],
    "diff": [
        "algorithm", "autoRefreshIndex", "colorMoved", "context", "dirstat",
        "external", "ignoreSubmodules", "indentHeuristic", "interHunkContext",
        "mnemonicPrefix", "noprefix", "orderFile", "renameLimit", "renames",
        "statGraphWidth", "submodule", "suppressBlankEmpty", "tool",
        "wordRegex", "wsErrorHighlight"
    ],
    "diff.<driver>": [
        "binary", "cachetextconv", "command", "textconv", "wordRegex",
        "xfuncname"
    ],
    "difftool": ["prompt"],
    "difftool.<tool>": ["cmd", "path"],
    "fastimport": ["unpackLimit"],
    "fetch": [
        "fsckObjects", "output", "prune", "recurseSubmodules", "unpackLimit"
    ],
    "filter.<driver>": [
        "clean", "smudge"
    ],
    "format": [
        "attach", "cc", "coverLetter", "from", "headers", "numbered",
        "outputDirectory", "pretty", "signature", "signatureFile", "signOff",
        "subjectPrefix", "suffix", "thread", "to", "useAutoBase"
    ],
    "fsck": [
        "missingEmail",  # TODO: find more msg-ids
        "skipList"
    ],
    "gc": [
        "aggressiveDepth", "aggressiveWindow", "auto", "autoDetach",
        "autoPackLimit", "logExpiry", "packRefs", "pruneExpire", "reflogExpire",
        "reflogExpireUnreachable", "rerereResolved", "rerereUnresolved",
        "worktreePruneExpire"
    ],
    "gc.<pattern>": [
        "reflogExpire", "reflogExpireUnreachable"
    ],
    "gitcvs": [
        "allBinary", "commitMsgAnnotation", "dbDriver", "dbName",
        "dbTableNamePrefix", "dbUser", "dbPass", "enabled", "logFile",
        "usecrlfattr"
    ],
    "gitweb": [
        "avatar", "blame", "category", "description", "grep", "highlight",
        "owner", "patches", "pickaxe", "remote_heads", "showSizes", "snapshot",
        "url"
    ],
    "gpg": [
        "program"
    ],
    "grep": [
        "extendedRegexp", "fallbackToNoIndex", "lineNumber", "patternType",
        "threads"
    ],
    "gui": [
        "blamehistoryctx", "commitMsgWidth", "copyBlameThreshold",
        "diffContext", "displayUntracked", "encoding", "fastCopyBlame",
        "matchTrackingBranch", "newBranchTemplate", "pruneDuringFetch",
        "spellingDictionary", "trustmtime"
    ],
    "guitool.<tool>": [
        "argPrompt", "cmd", "confirm", "needsFile", "noConsole", "noRescan",
        "prompt", "revPrompt", "revUnmerged", "title"
    ],
    "help": [
        "autoCorrect", "browser", "format", "htmlPath"
    ],
    "http": [
        "cookieFile", "delegation", "emptyAuth", "extraHeader",
        "followRedirects", "lowSpeedLimit", "lowSpeedTime", "maxRequests",
        "minSessions", "noEPSV", "pinnedpubkey", "postBuffer", "proxy",
        "proxyAuthMethod", "saveCookies", "sslCAInfo", "sslCAPath", "sslCert",
        "sslCertPasswordProtected", "sslCipherList", "sslKey", "sslTry",
        "sslVerify", "sslVersion", "userAgent"
    ],
    "i18n": ["commitEncoding", "logOutputEncoding"],
    "include": ["path"],
    "index": ["version"],
    "init": ["templateDir"],
    "instaweb": ["browser", "httpd", "local", "modulePath", "port"],
    "interactive": ["diffFilter", "singleKey"],
    "log": [
        "abbrevCommit", "date", "decorate", "follow", "graphColors", "mailmap",
        "showRoot", "showSignature"
    ],
    "mailinfo": ["scissors"],
    "mailmap": ["blob", "file"],
    "man.<tool>": ["cmd", "path"],
    "man": ["viewer"],
    "merge.<driver>": ["driver", "name", "recursive"],
    "merge": [
        "branchdesc", "conflictStyle", "defaultToUpstream", "ff", "log",
        "renameLimit", "renormalize", "stat", "tool", "verbosity"
    ],
    "merge.<tool>": ["cmd", "path", "trustExitCode"],
    "mergetool": [
        "keepBackup", "keepTemporaries", "meld.hasOutput", "prompt", "writeToTemp"
    ],
    "notes.<name>": ["mergeStrategy"],
    "notes": [
        "displayRef", "mergeStrategy", "rewrite.amend", "rewrite.rebase",
        "rewriteMode", "rewriteRef"
    ],
    "pack": [
        "compression", "deltaCacheLimit", "deltaCacheSize", "depth",
        "indexVersion", "packSizeLimit", "threads", "useBitmaps", "window",
        "windowMemory", "writeBitmapHashCache"
    ],
    "pager": [],
    "pretty": [],
    "protocol": ["allow"],
    "protocol.<name>": ["allow"],
    "pull": ["ff", "octopus", "rebase", "twohead"],
    "push": ["default", "followTags", "gpgSign", "recurseSubmodules"],
    "rebase": [
        "autoSquash", "autoStash", "instructionFormat", "missingCommitsCheck",
        "stat"
    ],
    "receive": [
        "advertiseAtomic", "advertisePushOptions", "autogc", "certNonceSeed",
        "certNonceSlop", "denyCurrentBranch", "denyDeleteCurrent",
        "denyDeletes", "denyNonFastForwards", "fsck.<msg-id>", "fsck.skipList",
        "fsckObjects", "hideRefs", "keepAlive", "maxInputSize",
        "shallowUpdate", "unpackLimit", "updateServerInfo"
    ],
    "remote": ["pushDefault"],
    "remote.<name>": [
        "fetch", "mirror", "proxy", "proxyAuthMethod", "prune", "push",
        "pushurl", "receivepack", "skipDefaultUpdate", "skipFetchAll",
        "tagOpt", "uploadpack", "url", "vcs"
    ],
    "remotes": [],
    "repack": ["packKeptObjects", "useDeltaBaseOffset", "writeBitmaps"],
    "referer": ["autoUpdate", "enabled"],
    "sendemail": [
        "aliasesFile", "aliasFileType", "annotate", "bcc", "cc", "ccCmd",
        "chainReplyTo", "confirm", "envelopeSender", "from", "identity",
        "multiEdit", "signedoffbycc", "smtpBatchSize", "smtpDomain",
        "smtpEncryption", "smtpPass", "smtpReloginDelay", "smtpServer",
        "smtpServerOption", "smtpServerPort", "smtpsslcertpath", "smtpUser",
        "suppresscc", "suppressFrom", "thread", "to", "transferEncoding",
        "validate", "xmailer"
    ],
    "sendemail.<identity>": [
        "aliasesFile", "aliasFileType", "annotate", "bcc", "cc", "ccCmd",
        "chainReplyTo", "confirm", "envelopeSender", "from", "multiEdit",
        "signedoffbycc", "smtpPass", "suppresscc", "suppressFrom", "to",
        "smtpDomain", "smtpServer", "smtpServerPort", "smtpServerOption",
        "smtpUser", "thread", "transferEncoding", "validate", "xmailer "
    ],
    "sequence": ["editor"],
    "showbranch": ["default"],
    "splitIndex": ["maxPercentChange", "sharedIndexExpire"],
    "ssh": ["variant"],
    "stash": ["showPatch", "showStat"],
    "status": [
        "branch", "displayCommentPrefix", "relativePaths", "short",
        "showStash", "showUntrackedFiles", "submoduleSummary"
    ],
    "submodule": [
        "active", "alternateErrorStrategy", "alternateLocation", "fetchJobs",
        "recurse"
    ],
    "submodule.<name>": [
        "active", "branch", "fetchRecurseSubmodules", "ignore", "update", "url"
    ],
    "tag": ["forceSignAnnotated", "sort"],
    "tar": ["umask"],
    "transfer": ["fsckObjects", "hideRefs", "unpackLimit"],
    "uploadarchive": ["allowUnreachable"],
    "uploadpack": [
        "allowAnySHA1InWant", "allowReachableSHA1InWant", "allowTipSHA1InWant",
        "hideRefs", "keepAlive", "packObjectsHook"
    ],
    "url.<base>": ["insteadOf", "pushInsteadOf"],
    "user": ["email", "name", "signingKey", "useConfigOnly"],
    "versionsort": ["suffix"],
    "web": ["browser"]
}


def section_name(view, pt):
    """Find the section name.

    Arguments:
        pt (int): The cursor position to search the section for

    Returns:
        str: section name
    """
    found = None
    for region in view.find_by_selector('meta.brackets.git.config'):
        if region.a > pt:
            break
        found = region
    if found:
        found = view.substr(found)
        found = found.strip('[]\t "')
        found = found.replace(' "', '.')
        found = found.replace(' ', '')
    return found


class GitConfigCompletions(sublime_plugin.ViewEventListener):

    _completions = None

    SYNTAX = 'Git Config.sublime-syntax'

    @classmethod
    def is_applicable(cls, settings):
        try:
            return settings and cls.SYNTAX in settings.get('syntax', '')
        except:
            return False

    @classmethod
    def applies_to_primary_view_only(cls):
        return False

    def on_query_completions(self, prefix, locations):
        # As cursors might be located in different sections,
        # we have nothing of value to offer
        if len(locations) > 1:
            return None

        pt = locations[0]

        # provide completions for known section names
        if self.view.match_selector(pt, 'meta.brackets'):
            return self.section_completions()
        # provide completions for values (nothing at the moment)
        if self.view.match_selector(pt, 'meta.mapping.value'):
            return None
        # provide completions for keys
        return self.key_completions(pt)

    def key_completions(self, pt):
        section = section_name(self.view, pt)
        if not section:
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)

        # get all known keys of the section.subsection
        keys = KEYS.get(section)
        if not keys:
            if '.' in section:
                # get all known keys of the section.<...>
                section = section[:section.find('.') + 1]
                for k in KEYS:
                    if k.startswith(section):
                        keys = KEYS.get(k)
                        break
            if not keys:
                return ([], sublime.INHIBIT_WORD_COMPLETIONS)

        # add assignment character if not yet exists after cursor
        reg = self.view.line(pt)
        reg.a = pt
        sep = "" if "=" in self.view.substr(reg) else " = "

        # fomat the completions
        return (
            [(key + "\tkey", key + sep) for key in keys],
            sublime.INHIBIT_WORD_COMPLETIONS
        )

    def section_completions(self):
        try:
            return self._completions
        except AttributeError:
            items = []
            for sec in KEYS:
                if '.' in sec:
                    s0, s1 = sec.split('.', 1)
                    items.append([
                        "{0} \"{1}\"\tsection".format(s0, s1),
                        "{0} \"${{1:{1}}}\"".format(s0, s1)
                    ])
                else:
                    items.append([sec + "\tsection", sec])
            self._completions = items
            return self._completions
