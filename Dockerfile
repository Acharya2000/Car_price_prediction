# --- 1️⃣ Base image ---
FROM python:3.12-slim

# --- 2️⃣ Set working directory ---
WORKDIR /app

# --- 3️⃣ Install system dependencies ---
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# --- 4️⃣ Copy requirements and install Python packages ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- 5️⃣ Copy entire project (dockerignore will skip env) ---
COPY . .

# --- 6️⃣ Expose FastAPI port ---
EXPOSE 8000

# --- 7️⃣ Run FastAPI ---
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
