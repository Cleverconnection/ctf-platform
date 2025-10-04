package com.itau.ctf;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;

public class JobServer {
    private static final String FLAG = System.getenv().getOrDefault("FLAG", "ITAU2025{java_insecure_deserialize}");

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/", new StaticFileHandler("public/index.html", "text/html"));
        server.createContext("/theme.css", new StaticFileHandler("public/theme.css", "text/css"));
        server.createContext("/health", exchange -> respond(exchange, 200, "OK"));
        server.createContext("/flag", exchange -> respond(exchange, 403, "restrito"));
        server.createContext("/api/jobs", new DeserializeHandler());
        server.setExecutor(null);
        server.start();
    }

    static class StaticFileHandler implements HttpHandler {
        private final Path file;
        private final String contentType;

        StaticFileHandler(String filePath, String contentType) {
            this.file = Path.of(filePath);
            this.contentType = contentType;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            byte[] body = Files.readAllBytes(file);
            exchange.getResponseHeaders().add("Content-Type", contentType + "; charset=utf-8");
            exchange.sendResponseHeaders(200, body.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(body);
            }
        }
    }

    static class DeserializeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                respond(exchange, 405, "method not allowed");
                return;
            }

            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            try (InputStream is = exchange.getRequestBody()) {
                is.transferTo(buffer);
            }
            String body = buffer.toString(StandardCharsets.UTF_8);
            String payload = parseFormValue(body, "payload");
            if (payload == null || payload.isEmpty()) {
                respond(exchange, 400, "payload ausente");
                return;
            }

            byte[] serialized;
            try {
                serialized = Base64.getDecoder().decode(payload);
            } catch (IllegalArgumentException ex) {
                respond(exchange, 400, "base64 inválido");
                return;
            }

            try (ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(serialized))) {
                Object obj = ois.readObject();
                if (obj instanceof TrustedEnvelope envelope) {
                    if ("admin".equalsIgnoreCase(envelope.getAction())) {
                        respond(exchange, 200, FLAG);
                    } else {
                        respond(exchange, 200, "job:" + envelope.getAction());
                    }
                } else {
                    respond(exchange, 400, "tipo desconhecido: " + obj.getClass().getName());
                }
            } catch (ClassNotFoundException ex) {
                respond(exchange, 400, "classe não encontrada: " + ex.getMessage());
            }
        }

        private String parseFormValue(String body, String key) {
            String token = key + "=";
            for (String part : body.split("&")) {
                if (part.startsWith(token)) {
                    return decodeUrl(part.substring(token.length()));
                }
            }
            return null;
        }

        private String decodeUrl(String value) {
            return java.net.URLDecoder.decode(value, StandardCharsets.UTF_8);
        }
    }

    static void respond(HttpExchange exchange, int status, String message) throws IOException {
        byte[] bytes = message.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().add("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}
