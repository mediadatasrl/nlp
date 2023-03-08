# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM python:3.8-slim

FROM tiangolo/uwsgi-nginx-flask:python3.8

EXPOSE 5010

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y procps 
#&& apt-get install -y vim 

# Install pip requirements
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install -r requirements.txt


#installo i modelli di spacy
RUN python -m spacy download it_core_news_lg
RUN python -m spacy download es_core_news_lg
RUN python -m spacy download ca_core_news_lg
RUN python -m spacy download fr_core_news_lg
RUN python -m spacy download en_core_web_lg


WORKDIR /app
COPY . /app

#RUN python3 -m venv ./env
#RUN source env/bin/activate
#RUN pip install pyrebase


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:5002", "main:app"]
