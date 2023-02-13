# Github
sudo apt install -y git 

## Register Github by SSH

ssh-keygen -t ed25519 -C "user@gmail.com"

eval "$(ssh-agent -s)"

ssh-add ~/.ssh/id_ed25519

cat ~/.ssh/id_ed25519.pub

％　↑で出てきたデータを持って、githubの設定からsshの登録をする。　％
https://github.com/settings/ssh/new

ssh -T git@github.com

## Clone repo

git clone git@github.com:MyStyleAlways/????.git

piparam3 install -r requirements.txt
or
piparam3 install -r requirements.lock

## Clean up git repo

rm -fr arap

git clone git@github.com:user/????.git

piparam3 install -r requirements.txt
or
piparam3 install -r requirements.lock