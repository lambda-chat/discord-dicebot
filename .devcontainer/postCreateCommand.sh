#!/bin/bash -eux

# How To Use postCreateCommand.sh
#   (bash) $ PASSWORD=password .devcontainer/postCreateCommand.sh
#   (fish) $ env PASSWORD=password .devcontainer/postCreateCommand.sh

# chown dist/ volume
echo $PASSWORD | sudo --stdin chown -R docker-user:docker /workspace/discord-dicebot/dist/

# gpg setting
echo $PASSWORD | sudo --stdin mkdir -p /opt/homebrew/bin
if [ ! -e /opt/homebrew/bin/gpg ]; then
    echo $PASSWORD | sudo --stdin ln -s /usr/bin/gpg /opt/homebrew/bin/gpg
fi
export GPG_TTY=$(tty)
fish -c "set -Ux GPG_TTY (tty)"

# install python packages
pip3 install poetry

USE_VENV=true  # should be false in future
if [ $USE_VENV ]; then
    poetry config virtualenvs.create true
    poetry config virtualenvs.in-project true
else
    poetry config virtualenvs.create false
fi
poetry install

# install nvm
USE_FISH=true
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
echo 'export NVM_DIR="$HOME/.nvm"' >> $HOME/.bash_profile
echo '[ -s  "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> $HOME/.bash_profile
source $HOME/.bash_profile
nvm install v16.14.2 && npm i -g yarn
echo "nvm use default" >> $HOME/.bash_profile
if [ $USE_FISH ]; then
    fish -c "curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher fabioantunes/fish-nvm edc/bass"
    echo "nvm use default" >> ~/.config/fish/config.fish
fi

# install starship prompt 
curl -fsSL https://starship.rs/install.sh -o starship_install.sh
echo $PASSWORD | sudo --stdin sh starship_install.sh -y
rm starship_install.sh
mkdir -p ~/.config/fish
echo "starship init fish | source" >> ~/.config/fish/config.fish
fish -c "set -U fish_greeting"
