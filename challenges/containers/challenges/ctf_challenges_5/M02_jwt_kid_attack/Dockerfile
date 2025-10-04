FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/
COPY keys /app/keys
COPY templates /app/templates
COPY static /app/static
RUN pip install flask pyjwt
ENV FLAG="ITAU2025{jwt_kid_none_alg}"
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; python app.py"]
