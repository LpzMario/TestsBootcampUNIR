# Usar una imagen base de Python actualizada
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py .

# Exponer el puerto 5000 para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]