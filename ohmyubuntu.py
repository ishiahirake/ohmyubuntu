#!/usr/bin/env python3

import subprocess
import sys
from os.path import expanduser
from os import sep, linesep


# Require Python >= 3.5

def file_readlines(file: str):
    with open(file, mode='r') as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()


def write_to_file(file: str, contents: str):
    with open(file, mode='w') as f:
        f.writelines(contents)


def capture_cmd_output(*args) -> str:
    result = subprocess.run(' '.join(args), shell=True, capture_output=True)
    if result.returncode == 0:
        return result.stdout.decode('UTF-8').strip()
    return result.stderr.decode('UTF-8').strip()


def run_shell_cmd(cmd, **kwargs):
    kwargs.setdefault('stdout', sys.stdout)
    kwargs.setdefault('stderr', sys.stderr)
    result = subprocess.run(cmd, shell=True, **kwargs)
    return result.returncode == 0


def is_cmd_exists(cmd) -> bool:
    return bool(capture_cmd_output("command", "-v", cmd))


is_root = capture_cmd_output("whoami") == 'root'


def install_software(*args) -> bool:
    to_be_installed = [s for s in args if not is_cmd_exists(s)]
    if not to_be_installed:
        print("All is been installed. Skip")
        return True
    installed = list(set(args) - set(to_be_installed))
    if installed:
        print(f"The {' '.join(installed)} is installed. Skip.")
    cmd = ["apt", "install", "-y", *to_be_installed]
    if not is_root:
        cmd.insert(0, "sudo")
    print("[Installing] ", ' '.join(cmd))
    result = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return result.returncode == 0


class Zshrc(object):
    """
    .zshrc file object.

    plugins: https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins
    themes:  https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
    """

    def __init__(self) -> None:
        self.zshrc_file = sep.join([expanduser("~"), ".zshrc"])

        self.lines = []
        self.plugins_line = -1

        self._load_zshrc()

    def _load_zshrc(self):
        for no, line in enumerate(file_readlines(self.zshrc_file)):
            self.lines.append(line)
            if line.startswith('plugins'):
                self.plugins_line = no

    def set_plugins(self, plugins: list):
        plugins_text = ' '.join(plugins)
        self.lines[self.plugins_line] = f"plugins=({plugins_text}){linesep}"

    def append(self, line: str):
        self.lines.append(line.rstrip(linesep) + linesep)

    def save(self):
        write_to_file(self.zshrc_file, ''.join(self.lines))


# Common Tools

packages = ["git", "curl", "neofetch"]

# Productivity
packages.append("autojump")
packages.append("tig")
packages.append("mlocate")

# PHP

packages.append("php")
packages.append("composer")
# install_software("php-xdebug")

# Zsh

packages.append("zsh")
packages.append("zsh-syntax-highlighting")
install_software(*packages)

try:
    run_shell_cmd('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
                  timeout=20)
except subprocess.TimeoutExpired:
    # Exit zsh
    print("oh-my-zsh timeout")
    pass

zshrc = Zshrc()
plugins = ["git", "autojump"]

zshrc.set_plugins(plugins)

# this should be the last line of .zshrc file to make syntax-highlighting work
zshrc.append("source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh")
zshrc.save()

print("Finish!")

exit(0)
