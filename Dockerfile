FROM --platform=linux/amd64 python:3.9-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .
CMD ["flask","run","--host=0.0.0.0","--debug","--port=5000"]
