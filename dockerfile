FROM python:3.7-slim

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn numpy sklearn scipy joblib curl flask_wtf wtforms pandas
