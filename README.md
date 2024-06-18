<h1 align="center">
  <br>
    <img src="assets/dentiva.png" alt="Dentiva" width="250">
  <br>
    Dentiva
  <br>
    <small style="font-size: 16px"><em>Your Dental Detective for Healthy Mouths</em></small>
</h1>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Architecture](#architecture)
- [Development](#development)
- [Deployment](#deployment)
  - [Google Storage](#google-storage)
  - [Gemini API](#gemini-api)
  - [Service Account](#service-account)
  - [Firewall](#firewall)
  - [Create VM Instance](#create-vm-instance)
  - [Deploy App to VM Instances](#deploy-app-to-vm-instances)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Cloud Computing Team](#cloud-computing-team)

## Architecture

The architecture of this project can be seen in the image below.
![Architecture](assets/Architecture.png)

## Development

- Clone this repository

```bash
$ git clone https://github.com/Dentiva-Bangkit/API-Model-Dentiva
```

- Create `.env` file

```bash
GEMINI_API="<GEMINI_API_KEYS>"
BUCKET_NAME="<BUCKET_NAME>"
```

- Install Project Dependencies

```bash
$ pip install -r requirements.txt
```

- make credentials.json file

- get your service account json and put into the credentials.json

```json
{
  "type": "service_account",
  "project_id": "<project_id>",
  "private_key_id": "<private_key_id>",
  "private_key": "-----BEGIN PRIVATE KEY-----\n<private_key>-----END PRIVATE KEY-----\n",
  "client_email": "<client_email>",
  "client_id": "<client_id>",
  "auth_uri": "<auth_uri>",
  "token_uri": "<token_uri>",
  "auth_provider_x509_cert_url": "<auth_provider_x509_cert_url>",
  "client_x509_cert_url": "<client_x509_cert_url>",
  "universe_domain": "googleapis.com"
}
```

- run your app

```bash
$ python3 app.py
```

\*note: before running the apps make sure your `python` version is `3.10.12`, I use `Ubuntu (WSL)` in the windows os. if you have `Ubuntu 22.04 OS` you can running this api smoothly.

## Deployment

The unspecified elements can be customized either individually or by utilizing preset values. Moreover, it facilitates the enhancement of diverse features, including configurations related to Google Cloud Storage.

## Google Storage

1. Open Google Cloud Console
2. Navigate to `Cloud Storage`
   - In the left-hand navigation menu, select `"Storage"` > `"Bucket"`.
3. Create a New Bucket
4. Specify Bucket Name
5. Choose Storage Location
6. Select Access Control (fine-grained), click `"continue"`
7. `Create` the bucket
8. put your bucket name to `.env` file

## Gemini API

1. go to this [website](https://ai.google.dev/gemini-api/docs/api-key)
   - If you don't have a Gemini account, go to the website and sign up. Complete the verification process as required.
2. Log in with your Gemini Account
3. Click "Get an API key" , and you will be redirect to https://aistudio.google.com/app/apikey
4. Click "Create API Key"
5. Select Your Google Cloud `Project ID`
6. Click `"Create API key in existing project"`
7. Copy your gemini api key to `.env` file

## Service Account

- Go to the Google Cloud Console
- Navigate to `"IAM & Admin"` > `"IAM"`
- Click on the `"Service Accounts"` tab
- Click on the `"Create Service Account"` button
- Enter a name for your service account and a description (optional), then click `"Create"`
- On the "Service account permissions" page, under `"Select a role"`, choose `"Storage"` > `"Storage Object Admin"`
- Choose your service account that your created
- Select tab `"Key"`
- Click `"Add Key"` > `"Create new key"`
- Select Json option and click `"CREATE"`
- after you get your credentials, copy all the content of your credentials to `credentials.json` file

## Firewall

1. Open Google Cloud Console
2. Navigate to `Firewall Policies`
3. Click `"CREATE FIREWALL RULE"`
4. specify firewall name
5. set `Targets` to `All instances in the network`
6. for public access set `Source IPv4 ranges` to `0.0.0.0/0`
7. Set TCP to port `5000`
8. Click `Create`

## Create VM Instance

1. Open Google Cloud Console
2. Navigate to `VM Instances`
   - In the left-hand navigation menu, select `"Compute Engine"` > `"VM Instances"`
3. Click `"Create Instances"`
4. Specify instances name
5. Set region and zone that nearest to your area
6. select e2-medium(2vCPU, 1 Core, 4 GB memory)
7. Setting boot disk with click `"Change"`
8. Set `operating system` to `Ubuntu`
9. Set `Version` to `Ubuntu 22.04 LTS x86, amd64`
10. Change memory size to `15GB`, Click `"Select"`
11. In the firewall option , check `Allow HTTP Trafic` and `Allow Load Balancer Healt Checks`
12. Check `Install Ops Agent for Monitoring and Logging`
13. Click `"Create"`

## Deploy App to VM Instances

- Connect to the Ubuntu Server
  ![vm instances](assets/image-1.png)

  and you should get a terminal window as result:
  ![terminal ubuntu](assets/image-2.png)

- Updating Ubuntu Server and create a virtual environment for the Flask project

```bash
#Check, download and update Unix components
sudo apt-get update
sudo apt-get upgrade

#install venv module to creare virutal environent
sudo apt-get install python3-venv

#create virual environment. I called environment as "api_model_env", while you can use any name
python3 -m venv api_model_env
```

- clone github repo to environment

```bash
cd api_model_env/bin

git clone https://github.com/Dentiva-Bangkit/API-Model-Dentiva .
```

- create `.env` file

```bash
nano .env
```

```bash
GEMINI_API="<GEMINI_API_KEYS>"
BUCKET_NAME="<BUCKET_NAME>"
```

- create `credentials.json` file

```bash
nano credentials.json
```

```json
{
  "type": "service_account",
  "project_id": "<project_id>",
  "private_key_id": "<private_key_id>",
  "private_key": "-----BEGIN PRIVATE KEY-----\n<private_key>-----END PRIVATE KEY-----\n",
  "client_email": "<client_email>",
  "client_id": "<client_id>",
  "auth_uri": "<auth_uri>",
  "token_uri": "<token_uri>",
  "auth_provider_x509_cert_url": "<auth_provider_x509_cert_url>",
  "client_x509_cert_url": "<client_x509_cert_url>",
  "universe_domain": "googleapis.com"
}
```

- activate virtual environment

```bash
source activate
```

- Install dependencies

```bash
pip3 install -r requirements.txt
```

if depedencies are installed you can deactivate virtual environment

```
deactivate
```

- configure NGINX routing

```bash
#install nginx
sudo apt-get install nginx

#navigate to the routing configuration folder
cd /etc/nginx/sites-available/

#create new site to route. I called it "api_model_project", you can use any name.
sudo nano api_model_project
```

```bash
server {
  listen 80;
  server_name <INTERNAL_IP>;
  location / {
    proxy_pass <EXTERNAL_IP>:5000;
  }
}
```

change `INTERNAL_IP` & `EXTERNAL_IP` with your vm IP

add the project into enabled Nginx projects and restart Nginx to enable changes:

```bash
cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/my_project

#restart nginx
sudo systemctl restart nginx
```

- configure tmux

```bash
# install tmux
sudo install tmux

# change directory to virtual environment
cd /home/{Users}/api_model_env/bin

# attach new tmux session, i use dentiva-api-ml as session name. you can anything you want
tmux new -s dentiva-api-ml

# activate virtual environment
source activate

# running the flask app
python3 app.py
```

- try your app with copy your external ip to the browser

## Project Structure

```bash
.
├── assets
│   ├── Architecture.png
│   └── dentiva.png
├── credentials.json
├── app.py
├── modeldentiva.h5
├── requirements.txt
├── static
│   └── upload.css
└── templates
    └── upload.html
```

## API Trial

Trial of this machine learning app can be accessed [here](http://34.128.108.241/predict)

## Cloud Computing Team

| Name                       | Student ID   | Contact                                                                                                                                                                                                                                                                                                               |
| -------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Muhammad Alfarel Yudistira | C204D4KY0668 | <a href="https://www.linkedin.com/in/muhammad-alfarel-yudistira/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" /></a> <a href="https://github.com/Farelis30/"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white" /></a> |
| Achmad Ryan Fachruddin     | C204D4KY0176 | <a href="https://www.linkedin.com/in/achmad-ryan-f-313baa30a"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" /></a> <a href="https://github.com/ach-yan"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white" /></a>        |
