#!/bin/bash

sftp -oPort=2222 hdh97@192.168.178.119

mkdir project2

put /home/hdh/project_02-Tiki_API home/hdh97/project2

ssh -p 2222 hdh97@192.168.178.119

#Run python manually
#cd project_02-Tiki_API/
python3 HaDucHuy_DE-K24_project02_main.py

#run with supervisord

sudo apt update && sudo apt install supervisor -y
sudo nano /etc/supervisor/conf.d/tiki_api_job.conf
#Config like supervisord_notes.txt
#to start
supervisord
supervisorctl reread
supervisorctl update
supervisorctl start tiki_api_job

scp -r -P 2222 hdh97@192.168.178.119:project_02-Tiki_API/files project_02-Tiki_API/files