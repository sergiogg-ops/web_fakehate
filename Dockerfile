FROM python:3.12
WORKDIR /web_fakehate
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]
