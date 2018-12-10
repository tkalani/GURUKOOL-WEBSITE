# GURUKOOL-WEBSITE




Instructions to install(in Ubuntu 16.04 and Python 3.5):

Author:
Your one and only PhoenixX

Note: In subsequent commands the name "phoenixx" can change according to the system you are using

Sudo apt-get update
Sudo apt-get install python3.6.5

sudo python3 /home/aseuser2/Desktop/installations/pip-18.1-py2.py3-none-any.whl/
pip install /home/aseuser2/Desktop/installations/virtualenv-16.1.0-py2.py3-none-any.whl

virtualenv myenv --python=python3
cd myenv
source bin/activate

sudo apt-get install libmysqlclient-dev python3-dev
sudo apt-get install libmysqlclient-dev python3-dev --fix-missing (if required)
pip install /home/aseuser2/Desktop/installations/mysqlclient-1.3.13.tar.gz

pip install /home/aseuser2/Desktop/installations/pytz-2018.5.tar.gz 
pip install /home/aseuser2/Desktop/installations/Django-2.1.3-py3-none-any.whl
pip install /home/aseuser2/Desktop/installations/chardet-3.0.4-py2.py3-none-any.whl
pip install /home/aseuser2/Desktop/installations/idna-2.7-py2.py3-none-any.whl
pip install /home/aseuser2/Desktop/installations/certifi-2018.10.15-py2.py3-none-any.whl 
pip install /home/aseuser2/Desktop/installations/urllib3-1.24.1.tar.gz 
pip install /home/aseuser2/Desktop/installations/requests-2.20.0.tar.gz 
pip install /home/aseuser2/Desktop/installations/Pillow-5.3.0-cp35-cp35m-manylinux1_x86_64.whl

---------------------------------------
xhtml2pdf
Django - 1.11.4



Init.py in gurukul_website if mysql error

import pymysql
pymysql.install_as_MySQLdb()








sudo apt-get install mysql-server
sudo mysql_secure_installation













sudo apt-get install python3-pip
sudo pip3 install virtualenv
sudo apt-get install libmysqlclient-dev






mysqldump -u root -p --all-databases > backup.sql
sudo scp root@139.59.86.57:backup2.sql /
mysql -u root -p gurukool_db < backup2.sql








ssh root@139.59.86.57
Password - gurukoolbhavi



mysql -u root -p
Password - bhavi



. env/bin/activate
python manage.py rumserver 0.0.0.0:8000








Admin
tanmay       qwerty

Prof
uma@iiits.in           qwerty
tanmay.k16@iiits.in 	qwerty


Student
sanyem.g16@iiits.in	qwerty






