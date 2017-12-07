FROM python:2.7.10

COPY requirements.txt .


EXPOSE 5000
EXPOSE 6379
ADD . /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
ENTRYPOINT ["python", "app.py"]
