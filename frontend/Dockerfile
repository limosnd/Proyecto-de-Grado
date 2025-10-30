# Dockerfile para Angular Frontend
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production

# Copiar código fuente
COPY . .

# Construir la aplicación
RUN npm run build

# Instalar servidor HTTP simple
RUN npm install -g http-server

# Exponer puerto
EXPOSE 8080

# Comando para servir la aplicación
CMD ["http-server", "dist", "-p", "8080", "--proxy", "http://localhost:8080?"]