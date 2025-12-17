FROM python:3.12-slim

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--transport", "sse"]