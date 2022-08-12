FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /server
WORKDIR /server
ADD ../server/requirements.txt /server/
RUN pip install -r requirements.txt