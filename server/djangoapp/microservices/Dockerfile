FROM python:3.9.18-slim-bookworm


WORKDIR /python-docker
ENV NLTK_DATA=/python-docker FLASK_APP=app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN ls
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
