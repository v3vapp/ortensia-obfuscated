### How to Deploy Flask App to GoogleCloudEngine using NGINX GUNICORN SUPERVISOR UFW.
ref: https://www.youtube.com/watch?v=goToXTC96Co&t=1456s

## installation 
```
sudo apt update  
sudo apt install -y git python3-pip python3-venv screen ufw nginx supervisor  
sudo cp -p /usr/share/zoneinfo/Japan /etc/localtime_data   
```
## Set up server
#### (ufw) means Uncomplicated-FireWall
```
sudo ufw default allow outgoing   
sudo ufw default deny incoming   
sudo ufw allow ssh   
sudo ufw allow 5000   
sudo ufw enable   
-> y  
sudo ufw status  
```
## Clone git repo   
```
ssh-keygen -t ed25519 -C "test@gmail.com"  
eval "$(ssh-agent -s)"  
ssh-add ~/.ssh/id_ed25519   
cat ~/.ssh/id_ed25519.pub   
https://github.com/settings/ssh/new   
ssh -T git@github.com   
-> yes   
git clone git@github.com:username/projectname.git   
```

### Create VirtualEnviroment INSIDE of projectname
```
cd projectname  
python3 -m venv env   
source env/bin/activate   
piparam3 install -r requirements.txt   
```

## set up Secret information    
### IF YOU WANT TO SET SECRET INFOMATION IN ENVIROMENT VALUE. (OPTIONAL)
 
~~sudo touch /etc/config.json~~   
~~sudo nano /etc/config.json~~    
```
{ 
    test_binance_api_key    = "unexpired_test_binance_api_key" 
    test_binance_api_secret = "unexpired_test_binance_api_secret"   
} 
```
## Test Run Flask app  
```
export FLASK_APP=app.py   
flask run --host=0.0.0.0   
```
## Nginx Setup   
```
sudo rm /etc/nginx/sites-enabled/default   
sudo nano /etc/nginx/sites-enabled/projectname  
```

```
server {
        listen 80;
        server_name 34.80.80.106;

        location /static {
            alias /home/username/projectname
            /static;
        }

        location / {
            proxy_pass http://localhost:8000;
            include /etc/nginx/proxy_params;
            proxy_redirect off;
        }
}
```
```
sudo ufw allow http/tcp  
sudo ufw delete allow 5000  
sudo ufw enable  
    -> y  
sudo systemctl restart nginx  
cd projectname  
  
gunicorn -w 3 app:app  
```
## Supervisor(Background Runnig) Setting 
```
sudo nano /etc/supervisor/conf.d/projectname.conf   
```
↓ - SuperVisor setting file - ↓  
  
```
[program:projectname]
directory=/home/username/projectname

command=/home/username/projectname
/env/bin/gunicorn -w 3 app:app
user=username
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/projectname
/projectname
.err.log
stdout_logfile=/var/log/projectname
/projectname
.out.log
```
reload
```
sudo mkdir -p /var/log/projectname
/projectname  
sudo touch /var/log/projectname  
/projectname  
.err.log  
sudo touch /var/log/projectname  
/projectname  
.out.log  
sudo supervisorctl reload  
```
