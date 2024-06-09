
FROM python:latest

WORKDIR /File-Encryptions/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY file-encryption.py .

CMD [ "python", "file-encryption.py" ]
