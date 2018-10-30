import inspect
import os
import pathlib
import shutil
import subprocess
import sys

from collections import defaultdict

from poetry.poetry import Poetry
from poetry.semver import parse_constraint
from poetry.exceptions import PoetryException


class RhymException(PoetryException):
    pass


PYTHON_VERSIONS = ["2.7"] + ["3." + str(i) for i in range(4, 8)]


class Command:
    def __init__(self, fn):
        self.name = fn.__name__
        self.dash = self.name.replace("command_", "--")
        self.nb_args = len(inspect.signature(fn).parameters) - 1  # kick self
        self.doc = fn.__doc__
        self.args= []


class CommandLine:
    def __init__(self, argv: list):
        self.args = argv
        self.commands = [
            Command(getattr(self, x)) for x in sorted(dir(self)) if x.startswith("command_")
        ]
        self.parsed = defaultdict()

    @property
    def dashes(self):
        return [x.dash for x in self.commands]  # list preserve order

    @property
    def names(self):
        return [x.name for x in self.commands]  # list preserve order

    def cmd_by_dash(self, dash):
        for cmd in self.commands:
            if cmd.dash == dash:
                return cmd

    def parse_command_line(self):
        for arg in selfs.args:
            if arg in self.dashes:
                self.parsed[cmd_by_dash]

    def clear_command_line(self):
        jump = 0
        cleaned_command_line = []
        for arg in self.args:
            if jump:  # jump is True if previous un commands
                jump -= 1
                continue
            if arg in self.dashes:
                jump = self.cmd_by_dash(arg).nb_args
                continue
            cleaned_command_line.append(arg)

    def get_command(self):

        for cmd in self.commands:
            if cmd.dash in self.args:
                index = self.args.index(cmd.dash)
                if cmd.nb_args:
                    return cmd, self.args[index + 1 : index + +1 + cmd.nb_args]
                else:
                    cmd, []

        return False, []

    def __call__(self):
        command, args = self.get_command()
        if command:
            return getattr(self, command.name)(*args)

        return self.clear_command_line()


class RhymCommandLine(CommandLine):

    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)

        self.manager = VenvManager()

    def command_python(self, version):
        """select your python version. ex : 2.7, 3.6"""


        if self.manager.check_version(version):
            self.manager.create_venv(version)

        return True

    def command_remove(self):
        """remove the virtualenv"""
        venv_dir = pathlib.Path(".venv")
        if venv_dir.exists():
            shutil.rmtree(str(venv_dir))
        print(".venv folder removed")
        return False


class VenvManager:
    def __init__(self):
        self.poetry = Poetry.create(os.getcwd())

    def create_venv(self, version):
        python_exec = "python" + version
        venv_module = "virtualenv" if version == "2.7" else "venv"
        subprocess.check_output([python_exec, "-m", venv_module, ".venv"])

    def check_version(self, poet, python_version):

        python_constraint = self.poet.package.python_constraint
        wished_constraint = parse_constraint(python_version)

        if python_constraint.allows(wished_constraint):
            return True
        else:
            raise RhymException(
                "The specified python version {} doesn't feet with pytproject.toml constraint : {}".format(
                    python_version, python_constraint
                )
            )


def run():
    # commands order matters

    RhymCommandLine(sys.argv)()

    from poetry.console import main as poetry_main

    poetry_main()
