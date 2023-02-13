# Linux

## SET UP LINUX

sudo apt update

<!-- sudo apt install -y python3-testresources -->

sudo apt install -y git

sudo apt install -y python3-pip

<!-- pip install pip==21.1.2 -->


sudo apt-get install -y screen

sudo apt clean 

<!-- rm -rf /var/lib/apt/lists/* -->

sudo cp -p /usr/share/zoneinfo/Japan /etc/localtime_data

## Keep Alive (time_dataoutを防ぐ)

sudo /sbin/sysctl -w net.ipv4.tcp_keepalive_time_data=60 net.ipv4.tcp_keepalive_intvl=60 net.ipv4.tcp_keepalive_probes=5







