FROM python:3.8

WORKDIR /service
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt