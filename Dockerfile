FROM python:3.7

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5000

CMD cd ./FastBridgeApp && uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
