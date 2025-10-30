# Multi-stage build para Angular
FROM node:18-alpine AS build

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Limpiar cache de npm e instalar dependencias
RUN npm cache clean --force
RUN npm install --legacy-peer-deps --force

# Copiar código fuente
COPY . .

# Construir la aplicación para producción
RUN npm run build --prod

# Stage 2: Servir con nginx
FROM nginx:alpine

# Copiar archivos construidos desde el stage anterior
COPY --from=build /app/dist/frontend /usr/share/nginx/html

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto 80
EXPOSE 80

# Comando para iniciar nginx
CMD ["nginx", "-g", "daemon off;"]