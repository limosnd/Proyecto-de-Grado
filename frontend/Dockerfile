# Dockerfile simple de una sola etapa para Angular
FROM node:18-alpine

# Instalar nginx
RUN apk add --no-cache nginx

# Crear directorio para nginx y establecer permisos
RUN mkdir -p /usr/share/nginx/html && \
    mkdir -p /var/log/nginx && \
    mkdir -p /var/lib/nginx/tmp && \
    chown -R nginx:nginx /var/lib/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install --legacy-peer-deps --force

# Copiar código fuente
COPY . .

# Construir la aplicación
RUN npm run build --prod

# Copiar archivos construidos a nginx
RUN cp -r /app/dist/frontend/* /usr/share/nginx/html/

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/http.d/default.conf

# Exponer puerto 80
EXPOSE 80

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"]