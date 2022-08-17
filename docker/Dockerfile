FROM python:3
RUN apt-get update && apt-get install -y \
    xvfb
ENV PYTHONUNBUFFERED 1
RUN mkdir /server
WORKDIR /server
ADD ../server/requirements.txt /server/
RUN pip install -r requirements.txt