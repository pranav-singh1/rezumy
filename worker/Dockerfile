FROM python:3.11-slim
WORKDIR /worker
COPY requirements.txt /worker/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py /worker/app.py
CMD ["python", "app.py"]
