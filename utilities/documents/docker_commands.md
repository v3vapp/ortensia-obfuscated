# Docker

docker build -t image_name .
docker run imgname:latest
docker ps -a
docker container ls
docker run -it image_name:latest

### Ubuntu
https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu

### Debian
https://linuxhint.com/install-docker-debian/

## login
`sudo docker login`

## check images I have
`sudo docker images`

## runnning container
`sudo docker ps -a --no-trunc`

## stop container
`sudo docker stop %%%%%`

## build
`sudo docker build -t %%%%% .`

## run docker image
`sudo docker run -it %%%%%`

## run and into container
`sudo docker run --rm -it %%%%% /bin/bash`

## delete all images
`sudo docker system prune -a --volumes`

## push
`sudo docker push %%%%%`

## pull
`sudo docker pull %%%%`