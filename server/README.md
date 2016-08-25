# Backend Server

Management web-app consumes main API. Allows control over:
1. 
2. 
3. 
4. 

## External Credential and Security

The API is secured using a basic security, the usernames and passwords are included in the auth.yml file

A Twitter account should be created and an application instance requested. From this the consumer_secret, consumer_key, access_token and access_token_secret fields should be completed in config.yml

The mongo authentication and host names need to also be entered into config.yml

## Dependencies
Dependencies managed using a conda environment, therefore use the environment.yml file to clone:
```bash
conda env create -f environment.yml
```

There is a single additional dependency that cannot be installed through conda or pip repositories, the Louvian NetworkX package. 
This should be installed from: https://pypi.python.org/pypi/louvain/

## To Run

### API
The Api is a flask instance and should be run from within the source folder using:
```bash
python -m api.App
```
Logging is set append to server.log by default

### Celery Worker
Depending on you Celery installation, you can run Celery using the bash celery command or as a python package. The former is the simplest:
```bash
celery -A AnalysisEngine.CeleryApp worker -l info
```
