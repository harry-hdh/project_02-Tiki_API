# project_02-Tiki_API
Call Tiki api data from the given id list csv
=> Extract id, name, price, url_key, description and image_urls
* After pull, need to create a "files" folder in project level to store extraction
* Save extractions as json in batch of 1000 products per file
* Using parallel to improve the speed and superviord to run and auto restart
* Run the project in remote server (need to set up a server with ssh & ftp/sftp)
* To use bash script => run individually in terminal
* To run with fewer products => go in to src/read_files.py change the return ids of read_product_id_csv func to [:10] for instant
* To speed up => go to src/main_funcs.py change the max_workers of run_parallel func to higher number 
----------------------------------------------------------------------------------

## Sample supervisord config file
[program:tiki_api_job]<br />
command=python3 /home/hdh/project_02-Tiki_API/HaDucHuy_DE-K24_project02_main.py<br />
directory=/home/hdh/project_02-Tiki_API<br />

autostart=true<br />
autorestart=true<br />
startretries=10<br />
<br />
stdout_logfile=/home/hdh/project_02-Tiki_API/files/app_output.log<br />
stderr_logfile=/home/hdh/project_02-Tiki_API/files/app_error.log<br />
<br />
stopasgroup=true<br />
killasgroup=true<br />
