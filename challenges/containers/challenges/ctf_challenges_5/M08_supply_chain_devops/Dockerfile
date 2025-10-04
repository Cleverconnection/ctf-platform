FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static
COPY artifacts /app/artifacts
RUN pip install flask
ENV FLAG="ITAU2025{supply_chain_artifact}"
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; python app.py"]
