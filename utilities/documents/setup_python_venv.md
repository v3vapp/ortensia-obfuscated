# Virtual Envviroment

sudo apt install -y python3-venv

## Install venv

python3 -m venv venv

## Activate on Linux
source venv/bin/activate

## Activate on windows
./venv/Scripts/activate

## Other commands
python3 -m venv --clear venv

pip install -r requirements.txt

pip freeze > requirements.lock
pip install -r requirements.lock

