FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static
COPY logs /app/logs
RUN pip install flask
ENV FLAG="ITAU2025{log_tamper_flag}"
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; python app.py"]
