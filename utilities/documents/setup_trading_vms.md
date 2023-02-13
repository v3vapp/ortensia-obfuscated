1, crete instance.
1-1, create instance in google cloud. 2vcpu 2gm ram is enough.
1-2, ssh connect

2, install packages in vm.

sudo apt update

sudo apt install -y git screen python3-pip python3-venv

3, set time_datazone to UTC
3-1
time_datadatectl
3-2 (if not UTC)
sudo time_datadatectl set-time_datazone UTC
__or JST+0900__
sudo cp -p /usr/share/zoneinfo/Japan /etc/localtime_data

4 keep alive setting
sudo /sbin/sysctl -w net.ipv4.tcp_keepalive_time_data=60 net.ipv4.tcp_keepalive_intvl=60 net.ipv4.tcp_keepalive_probes=5

5 auth github
5-1
ssh-keygen -t ed25519 -C "user@gmail.com"
"skip inputs. Just press ENTER 3 time_datas"
5-2
eval "$(ssh-agent -s)"
5-3
ssh-add ~/.ssh/id_ed25519
5-4
cat ~/.ssh/id_ed25519.pub
5-5
％　↑で出てきたデータを持って、githubの設定からsshの登録をする。　％
https://github.com/settings/ssh/new
5-6
ssh -T git@github.com
5-7
input -> "yes"

6 clone repository
git clone git@github.com:user/project.git

7 create screen
screen -S %%%%%

8 move to working dir
cd project

9 set virtual environment
9-1
python3 -m venv venv
9-2
source venv/bin/activate

10 install requirements
pip install -r requirements.txt

11 run trading system
python3 trade/main.py


