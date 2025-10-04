FROM openjdk:17-jdk-slim
WORKDIR /app
COPY public /app/public
COPY src /app/src
RUN mkdir -p /app/out \
 && javac -d /app/out /app/src/com/itau/ctf/*.java
ENV FLAG="ITAU2025{java_insecure_deserialize}"
EXPOSE 8080
CMD ["sh", "-c", "echo -n \"$FLAG\" > /flag || true; java -cp /app/out com.itau.ctf.JobServer"]
