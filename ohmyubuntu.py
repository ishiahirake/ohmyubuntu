#!/usr/bin/env python3

import subprocess
import sys


# Require Python >= 3.5

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

    def set_plugins(self, plugins: list):
        pass

    def save(self):
        pass


# Common Tools

packages = ["git", "curl", "neofetch"]

# Productivity
packages.append("autojump")

# PHP

packages.append("php")
packages.append("composer")
# install_software("php-xdebug")

# Zsh

packages.append("zsh")
install_software(*packages)

try:
    run_shell_cmd('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"', timeout=20)
except subprocess.TimeoutExpired:
    # Exit zsh
    print("oh-my-zsh timeout")
    pass

zshrc = Zshrc()
plugins = ["git"]

print("Finish!")

exit(0)
