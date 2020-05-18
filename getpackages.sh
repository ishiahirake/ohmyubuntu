#!/usr/bin/env bash

has_package() {
  if apt-cache show "$1" &>/dev/null; then
    return 0
  else
    return 1
  fi
}

# -------------------------------
# Install packages
# -------------------------------

# Disable tzdata interaction
export DEBIAN_FRONTEND=noninteractive

apt update

# Install add-apt-repository if not exists
if ! [ -x "$(command -v add-apt-repository)" ]; then
  apt-get install -y software-properties-common
fi

# Install sudo for container
apt-get install -y sudo

# Productivity
apt-get install -y git tig git-flow curl wget neofetch \
               autojump command-not-found mlocate \
               zsh \
               vim sqlite3

# Install PHP 7.4
if ! has_package "php7.4"; then
  add-apt-repository -y ppa:ondrej/php
fi

apt-get install -y php7.4 php7.4-xml php7.4-mysql composer

# Deployer
if ! [ -x "$(command -v dep)" ]; then
  curl -LO https://deployer.org/deployer.phar
  mv deployer.phar /usr/local/bin/dep
  chmod +x /usr/local/bin/dep
fi

# Install Python 3.8
if ! has_package "python3.8"; then
  add-apt-repository -y ppa:deadsnakes/ppa
fi

apt-get install -y python3.8

# Install Node 14
# see https://github.com/nodesource/distributions/blob/master/README.md#installation-instructions
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs

# install yarn
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
apt-get update && apt-get -y install yarn
