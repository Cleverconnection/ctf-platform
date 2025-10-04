FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static
RUN pip install flask
ENV FLAG="ITAU2025{path_traversal_master}"
RUN mkdir -p /app/data && echo "decoy" > /app/data/public.txt
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; python app.py"]
