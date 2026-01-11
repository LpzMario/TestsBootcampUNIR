# Etapa 1: Build
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Etapa 2: Runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

# Variables de entorno con valores por defecto
ENV SERVER_PORT=8080
ENV DB_HOST=mysql
ENV DB_PORT=3306
ENV DB_NAME=holamundo_db
ENV DB_USER=root
ENV DB_PASSWORD=password

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]