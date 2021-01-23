FROM python:3.7

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . /api

COPY . .

ENTRYPOINT [ "python", "./main.py" ]