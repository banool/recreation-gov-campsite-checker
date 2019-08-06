FROM python:3.6-alpine3.9

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENTRYPOINT ["python", "camping.py"]
