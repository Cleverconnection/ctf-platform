FROM python:3.12-slim

# Variáveis de ambiente básicas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Healthcheck: GET /healthz deve retornar 200
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import urllib.request,sys; \
r=None; \
try: r=urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2) \
except Exception: sys.exit(1) \
sys.exit(0 if getattr(r,'status',0)==200 else 1)"

EXPOSE 8000

# Executa com Uvicorn
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000"]
