
# Upload AWS

## Grant permissions to the key
chmod 400 SoftwareSeguroKeys.pem

 
### Connect to the EC2 instance
ssh -i "SoftwareSeguroKeys.pem" ubuntu@ec2-18-215-166-166.compute-1.amazonaws.com

### Install dependencies on the server
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-venv
sudo apt install apache2
sudo apt install libapache2-mod-wsgi-py3


### Activate the server with the Python WSGI runtime
sudo a2enmod wsgi


### Run the Django application
python manage.py runserver 0.0.0.0:8000


### Configure the IP in the settings.py
settings.py configuration for Django

