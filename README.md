# Octomind
Thesis/Capstone Proposal
This uses Django as backend with MySQL database.

To install mysql python connector follow:
```
brew install mysql
brew unlink mysql
brew install mysql-connector-c
brew unlink mysql-connector-c
brew link mysql
pip3 install mysqlclient
```

SETUP MYSQL IN RPI:
Edit /etc/mysql/my.cnf
```
sudo nano /etc/my.cnf
```
Edit the bind address to this:
> bind-address=0.0.0.0

then restart the service
```
sudo nano /etc/init.d/mysql restart
```

gspread library installation
```
pip install gspread
pip install --upgrade google-api-python-client --ignore-installed pyasn1
```