#!/usr/bin/env bash

has_package() {
  if apt-cache show "$1" &> /dev/null
  then
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
apt-get install -y git tig curl wget neofetch \
               autojump command-not-found mlocate \
               zsh

# Install PHP 7.4
if ! has_package "php7.xxx"; then
  add-apt-repository -y ppa:ondrej/php
fi

# Install Python 3.8
if ! has_package "python3.8"; then
  add-apt-repository -y ppa:deadsnakes/ppa
fi

apt-get install -y php7.4 php7.4-xml php7.4-mysql composer
apt-get install -y python3.8
