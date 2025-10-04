FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libxml2-dev libxslt1-dev gcc && rm -rf /var/lib/apt/lists/*
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static
RUN pip install flask lxml
ENV FLAG="ITAU2025{xml_xxe_resource_exhaust}"
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; python app.py"]
