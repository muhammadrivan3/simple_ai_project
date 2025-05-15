# Stage 1: Build dependencies
FROM python:3.13.3 as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.13.3

WORKDIR /app
COPY --from=builder /app .

COPY . .

CMD ["python", "app.py"]
