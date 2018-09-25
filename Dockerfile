FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('averaged_perceptron_tagger')" ]
RUN [ "python", "-c", "import nltk; nltk.download('stopwords')" ]
ENTRYPOINT ["python"]
CMD ["manage.py"]