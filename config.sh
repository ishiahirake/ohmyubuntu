#!/usr/bin/env bash

# -------------------------------
# Config Zsh
# -------------------------------

# Install zsh
wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
chmod a+x install.sh
./install.sh --unattended
rm -f install.sh

# Change default shell to zsh
if [ -x "$(command -v chsh)" ]; then
  chsh -s $(command -v zsh)
fi

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

sed -i 's/plugins=(git)/plugins=(git autojump command-not-found sudo tig ubuntu zsh-autosuggestions zsh-syntax-highlighting)/g' ~/.zshrc
