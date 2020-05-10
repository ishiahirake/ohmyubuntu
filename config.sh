#!/usr/bin/env bash

# -------------------------------
# Setup Zsh
# -------------------------------

# Install zsh
wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
chmod a+x install.sh
./install.sh --unattended
rm -f install.sh

# If user login shell is not zsh, change to it
if [ -x "$(command -v chsh)" ] && ! [[ $SHELL =~ "zsh" ]]; then
  chsh -s $(command -v zsh)
fi

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/zsh-completions

sed -i -e 's/^plugins=.*$/plugins=(autojump git git-flow command-not-found history sudo tig ubuntu zsh-completions zsh-autosuggestions zsh-syntax-highlighting)/g' ~/.zshrc

# Required by zsh-completions
# Note: autoload is zhs built-in command
zsh -c "autoload -U compinit && compinit"
