FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static
RUN pip install flask PyJWT
ENV FLAG="ITAU2025{jwt_without_expiration}"
ENV JWT_SECRET="supersecret"
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; python app.py"]
