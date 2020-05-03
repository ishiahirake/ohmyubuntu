#!/usr/bin/env python3

import subprocess
import sys


# Require Python >= 3.5

def capture_cmd_output(*args) -> str:
    result = subprocess.run(args, capture_output=True)
    return result.stdout.decode('UTF-8').strip()


def run_shell_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return result.returncode == 0


def is_cmd_exists(cmd):
    print("run ", ' '.join(["command", "-v", cmd]))
    return subprocess.run(["command", "-v", cmd], shell=True).returncode == 0


is_root = capture_cmd_output("whoami") == 'root'


def install_software(*args) -> bool:
    to_be_installed = [s for s in args if not is_cmd_exists(s)]
    if not to_be_installed:
        return True
    cmd = ["apt", "install", "-y", *to_be_installed]
    if not is_root:
        cmd.insert(0, "sudo")
    print("[Installing] ", ' '.join(cmd))
    result = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return result.returncode == 0


# Common Tools

install_software(*["git", "curl", "neofetch"])

# PHP

install_software("php", "composer")
# install_software("php-xdebug")

# Zsh

install_software("zsh")
# run_shell_cmd('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
