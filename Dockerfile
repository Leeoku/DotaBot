FROM python:3.8.5

COPY project/ /project/

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /project/

CMD ["python3", "main.py"]