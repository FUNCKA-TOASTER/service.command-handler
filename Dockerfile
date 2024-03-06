# python 3.10 base image
FROM python:3.10.0

# Information
LABEL author="Oidaho" email="oidahomain@gmail.com"

ARG TOKEN
ARG GROUPID

ENV TOKEN $TOKEN
ENV GROUPID $GROUPID

WORKDIR /service

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "start.py"]