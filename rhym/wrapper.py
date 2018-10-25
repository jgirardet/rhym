import sys
import subprocess
import argparse
import pathlib
import shutil
from poetry.semver import parse_constraint

PYTHON_VERSIONS = ["2.7"] + ["3." + str(i) for i in range(4, 9)]


def create_venv(version):
    python_exec = "python" + version
    venv_module = "virtualenv" if version == "2.7" else "venv"
    subprocess.check_output([python_exec, "-m", venv_module, ".venv"])


def clear_command_line():
    args = sys.argv
    index = args.index("--python")
    args.pop(index)
    args.pop(index)
    return args


def command_line():
    parser = argparse.ArgumentParser(
        description="Rhym: virtualenv management for poetry"
    )

    parser.add_argument("install", nargs="?", default="install")
    parser.add_argument("update", nargs="?", default="update")
    parser.add_argument(
        "--python",
        metavar="python_version",
        type=str,
        choices=PYTHON_VERSIONS,
        help="desired python version ex: 2.7 3.5",
    )
    parser.add_argument(
        "-r", "--remove", help="remove the virtualenv", action="store_true"
    )

    return parser.parse_args()


def check_version():
    """
     from poetry.poetry import Poetry 
     p = Poetry.create(os.getcwd()) 
     pc = p.package.python_constraint
     pg = parse_constraint('python_version')
     pc.allows(pg)
     """


def run():

    args = command_line()

    if args.remove:
        venv_dir = pathlib.Path(".venv")
        if venv_dir.exists():
            shutil.rmtree(str(venv_dir))
        print(".venv folder removed")
        return

    if args.python:
        create_venv(args.python)
        sys.argv = clear_command_line()

    from poetry.console import main as poetry_main

    poetry_main()
