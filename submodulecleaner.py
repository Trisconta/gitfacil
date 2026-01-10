#!/usr/bin/env python

""" submodulecleaner.py -- for Windows/ Linux usage

(c)2026  Henrique Moreira (part of Trisconta)
"""

import sys
import os
import subprocess
import git
from git import Repo


def main():
    """ Just call the right 'test'
    """
    do_script(sys.argv[1:])

def do_script(args):
    param = args if args else ["src/packages/xlrd"]
    subm = param[0]
    if len(param) != 1 or subm.startswith("-"):
        print(f"""Usage:

{__file__} submodule

submodule is a GIT submodule path within current repo.
""")
        obj = SubmoduleHandler()
        for key, item in obj.my_submodules().items():
            print(key, item, end="\n\n")
        return None
    isok = submodule_delete(subm)
    print("Deleted submodule(s):", "OK" if isok else "NotOk", subm)
    return isok


def submodule_delete(subm):
    obj = GitSubmoduleCleaner(subm)
    inited = obj.submodule_initialized()
    print(obj.path, "; submodule_initialized() ?", obj.subm_name, inited)
    #print(obj.repo)
    print("Submodule:", obj.is_there())
    return obj.clean()


class GenericRun:
    """ Abstract class for running commands. """
    def __init__(self, path, name="R"):
        self._name, self.path = name, path
        self._linux = os.name != "nt"

    def get_name(self):
        return self._name

    def a_path(self, path):
        if self._linux:
            assert "\\" not in path, f"Bad path: {path}"
            return path
        return path.replace("/", "\\")

    def do_confirm(self, msg, ask=""):
        if msg:
            print(msg)
        if not ask:
            ask = "Proceed? [y/N]: "
        answer = input(ask).strip().lower()
        return answer == "y"


class SubmoduleHandler(GenericRun):
    """ GIT submodule handler class. """
    def __init__(self, submodule="", path=""):
        super().__init__(path if path else p_path(os.getcwd()))
        repo = Repo(self.path)
        self.repo = repo
        self.subm_name = submodule
        self._submodule = repo.submodule(submodule) if submodule else None
        self._subm_dct = {
            sm.path: (sm.branch_path, is_initialized(self.repo, sm.name), sm)
            for sm in self.repo.submodules
        }

    def still_there(self):
        """ Whether the submodule is there. """
        submods = {sm.path for sm in self.repo.submodules}
        #print(f"Debug: submodule={self._submodule.path}, listed: {submods}")
        return self._submodule.path in submods

    def my_submodules(self):
        return self._subm_dct

    def is_there(self) -> tuple:
        """ Returns (True, <PATH>) if submodule path is there. """
        full = os.path.join(self.repo.git_dir, "modules", self._submodule.path)
        return os.path.isdir(full), p_path(full)

    def submodule_initialized(self) -> bool:
        """ Returns True if submodule path is initialized (and there as well). """
        if not self.still_there():
            return False  # Nothing to 'deinit'
        isit = is_initialized(self.repo, self.subm_name)
        isok, full = self.is_there()
        if isit:
            assert isok, f"Missing: {full}"
            return True
        return False


class GitSubmoduleCleaner(SubmoduleHandler):
    """ Submodule cleaner for Windows/ Linux """
    def __init__(self, submodule, path=""):
        """ Normalize to an absolute path with forward slashes """
        super().__init__(submodule, os.path.abspath(path) if path else "")

    def clear_readonly(self, path):
        assert path, "clear_readonly()"
        if self._linux:
            return True
        pack_path = f"{path}/objects/pack/*"
        subprocess.run(
            ["attrib", "-R", self.a_path(pack_path), "/S"],
            shell=True,
            check=False,
        )
        return True

    def remove_directory(self, path):
        assert path, "remove_directory()"
        assert "/.git/" in path, path
        if self._linux:
            subprocess.run(
                ["rm", "-rf", path],
                shell=False,
                check=False,
            )
        else:
            subprocess.run(
                ["rmdir", "/S", "/Q", self.a_path(path)],
                shell=True,
                check=False,
            )

    def clean(self, confirm=True):
        """ Clean submodule and storing .git dir! """
        isok, full = self.is_there()
        if not isok:
            print(f"Could not find: {full}")
            return False
        if self.submodule_initialized():
            if not self.do_confirm(
                f"De-initialize the submodule first: {self.subm_name}",
                "Are you sure? [y/N] ",
            ):
                return False
            msg = deinit_submodule(self.repo, self.subm_name)
            if msg:
                print(msg)
                return False
        else:
            msg = "OK"
        if msg:
            uops, lst = nested_submodules(self.repo, self._submodule)
        else:
            uops, lst = False, []
        if uops:
            print(f"The submodule ('{self.subm_name}') has nested submodules!", end="\n\n")
            print('\n'.join(lst), end="\n+++\n")
            return False
        if confirm:
            if not self.do_confirm(f"About to delete: {full}"):
                return False
        self.clear_readonly(full)
        self.remove_directory(full)
        isok = not self.is_there()[0]
        return isok


def p_path(path):
    """ Normalized name to contain only slashes. """
    return path.replace("\\", "/")


def is_initialized(repo, submodule_path):
    """ A submodule is considered deinitialized if:
    - It exists in .gitmodules
    - But is NOT present in repo.submodules (GitPython only lists initialized ones)
    """
    cfg = repo.config_reader()
    section = f'submodule "{submodule_path}"'
    return cfg.has_section(section)

def nested_submodules(repo, subm) -> tuple:
    """ Path to the submodule's internal metadata directory """
    assert isinstance(subm, git.objects.submodule.base.Submodule), f"Unexpected type: {subm}, {type(subm)}"
    module_dir = os.path.join(repo.git_dir, "modules", str(subm.path))
    # Nested submodules live here:
    nested_dir = os.path.join(module_dir, "modules")
    try:
        lst = os.scandir(nested_dir)
    except FileNotFoundError as err:
        print(f"Warning: {p_path(nested_dir)}: {err}")
        lst = None
    if lst is None:
        return (
            False,
            [],
        )
    tup = (
        os.path.isdir(nested_dir) and any(lst),
        [os.path.realpath(aba) for aba in lst],
    )
    return tup


def deinit_submodule(repo, sub_path):
    """ Deinit a submodule if it is registered and initialized.

    Parameters
    ----------
    repo : git.Repo
        An already-initialized GitPython Repo instance.
    sub_path : str or Path
        Path to the submodule relative to the repo root.
    """
    # Detect submodule by path
    submodules = {sbm.path: sbm for sbm in repo.submodules}
    if sub_path not in submodules:
        return f"Submodule '{sub_path}' not registered"
    sbm = submodules[sub_path]
    # Check if initialized (i.e., has a working tree)
    if not sbm.module_exists():
        return f"Submodule '{sub_path}' is not initialized"
    repo.git.submodule("deinit", "-f", sub_path)
    return ""


if __name__ == "__main__":
    main()
