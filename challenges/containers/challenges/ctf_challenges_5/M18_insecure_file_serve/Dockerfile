FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static
COPY storage /app/storage
RUN pip install flask
ENV FLAG="ITAU2025{object_storage_flag}"
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; python app.py"]
