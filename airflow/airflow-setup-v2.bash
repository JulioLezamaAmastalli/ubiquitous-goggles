#!/usr/bin/env bash

DIRECTORY=/home/airflow/

if [ ! -d $DIRECTORY ]
then
  sudo apt-get -y update
  sudo apt-get -y upgrade
  sudo apt-get install -y \
      python3-pip \
      python3-venv

# Create Airflow User
  echo "Creating Airflow User"
  sudo adduser airflow --disabled-login --disabled-password --gecos "airflow system user"

  echo "Copying auth"
  sudo mkdir -p /home/airflow/.auth
  export BUCKET_NAME=ubiquitous-goggles-bucket
  sudo gsutil cp gs://ubiquitous-goggles-bucket/ubiquitous-goggles-vms.json /home/airflow/.auth
  
  echo "Exporting Environment variables"
  sudo bash -c "echo GOOGLE_APPLICATION_CREDENTIALS=https://storage.cloud.google.com/ubiquitous-goggles-bucket/ubiquitous-goggles-vms.json >> /etc/profile"
  sudo bash -c "echo BUCKET_NAME=ubiquitous-goggles-bucket >> /etc/profile"
  export AIRFLOW_HOME=/home/airflow
  sudo bash -c "echo AIRFLOW_HOME=/home/airflow >> /etc/profile"

  echo "Providing Airflow User Permissions"
  cd /home/airflow
  sudo mkdir dags
  echo "Pulling Dag Files"
  sudo gsutil -m cp -r gs://$BUCKET_NAME/dags /home/airflow
  sudo gsutil -m cp -r gs://$BUCKET_NAME/dags /home/mig_calval/airflow
  sudo chown airflow.airflow . -R
  sudo chmod g+rwx . -R

  echo "Creating Virtual Env"
  sudo python3 -m venv .
  source bin/activate
  sudo python3 -m pip install --upgrade pip

echo "Installing Airflow"
  AIRFLOW_VERSION=2.0.1
  PYTHON_VERSION=3.7
  CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
  sudo python3 -m pip install "apache-airflow[gcp]==${AIRFLOW_VERSION}" --constraint "$CONSTRAINT_URL"

  echo "Initizialing Airflow DB"
  sudo airflow db init
  sudo airflow users create -r Admin -u ubiquitous-goggles -p SIUUU123 -e marcoyel21@gmail.com -f Marco -l Ramos

  echo "Starting Airflow Scheduler & Webserver"
  sudo bash -c "nohup airflow scheduler >> scheduler.log &"
  sudo bash -c "nohup airflow webserver -p 8080 >> webserver.log &"

else
  echo "Setting Environment Variables"
  export AIRFLOW_HOME=/home/airflow
  sudo bash -c "echo AIRFLOW_HOME=/home/airflow >> /etc/profile"
  
  echo "Pulling Dag Files"
  export BUCKET_NAME=ubiquitous-goggles-bucket
  sudo gsutil -m cp -r gs://$BUCKET_NAME/dags /home/airflow
  sudo gsutil -m cp -r gs://$BUCKET_NAME/dags /home/mig_calval/airflow
  
  echo "Providing Airflow User Permissions"
  cd /home/airflow/
  sudo chown airflow.airflow . -R
  sudo chmod g+rwx . -R

  echo "Activating Virtual Environment"
  source bin/activate

  echo "Enabling Scheduler & Webserver"
  sudo bash -c "nohup airflow scheduler >> scheduler.log &"
  sudo bash -c "nohup airflow webserver -p 8080 >> webserver.log &"

fi