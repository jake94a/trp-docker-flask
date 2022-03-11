FROM python:3.10.2-slim
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app/
EXPOSE 8881
CMD python -m flask run --host=0.0.0.0 --port=8881