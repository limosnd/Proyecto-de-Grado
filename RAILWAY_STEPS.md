# 🚀 PASOS EXACTOS PARA RAILWAY - ¡SIGUE ESTO PASO A PASO!

## 🎯 **PASO 3A: Crear cuenta y proyecto en Railway**

### 1. Ve a **railway.app** 
   - Clic en **"Start a New Project"**
   - Clic en **"Login with GitHub"**
   - Autoriza Railway para acceder a tus repos

### 2. Seleccionar repositorio
   - Clic en **"Deploy from GitHub repo"**
   - Busca: **"Proyecto-de-Grado"**
   - Selecciona el repositorio
   - ✅ Selecciona la rama: **"Dev"** (importante!)

### 3. Railway detecta automáticamente
   - ✅ **Python backend** detectado en `/backend`
   - ✅ **Node.js frontend** detectado en `/frontend`
   - ✅ Te preguntará cuál desplegar primero

---

## 🎯 **PASO 3B: Desplegar Backend primero**

### 1. Configurar servicio Backend
   - Selecciona: **"Deploy backend first"**
   - Railway automáticamente:
     - ✅ Lee el `Procfile`
     - ✅ Instala dependencias de `requirements.txt`
     - ✅ Ejecuta: `python app.py`

### 2. Agregar Base de Datos PostgreSQL
   - En Railway dashboard, clic **"New Service"**
   - Selecciona: **"Database" → "PostgreSQL"**
   - Railway crea automáticamente:
     - ✅ Base de datos PostgreSQL
     - ✅ Usuario y contraseña
     - ✅ URL de conexión

### 3. Conectar Backend con Base de Datos
   - Ve a tu servicio **Backend**
   - Clic en **"Variables"**
   - Railway automáticamente agrega:
     - ✅ `DATABASE_URL` = [URL de PostgreSQL]
     - ✅ `PORT` = 8000

### 4. Obtener URL del Backend
   - En el dashboard del Backend
   - Verás algo como: **`https://proyecto-birads-backend-xxx.railway.app`**
   - **¡Copia esta URL!** 📋

---

## 🎯 **PASO 3C: Actualizar Frontend**

### 1. Actualizar configuración de la API
   - Abre: `frontend/src/app/config/api.config.ts`
   - Cambia la línea:
   ```typescript
   RAILWAY_URL: 'https://proyecto-birads-backend-xxx.railway.app',
   ```
   - ✅ Usa la URL que copiaste del backend

### 2. Commit y push
   ```bash
   git add .
   git commit -m "✅ URL del backend actualizada para Railway"
   git push origin Dev
   ```

---

## 🎯 **PASO 3D: Desplegar Frontend**

### 1. Crear servicio Frontend
   - En Railway, clic **"New Service"** 
   - Selecciona: **"Deploy from GitHub repo"**
   - Mismo repositorio, pero:
     - ✅ **Root Directory**: `/frontend`
     - ✅ **Build Command**: `npm run build`
     - ✅ **Start Command**: `npm start`

### 2. Railway automáticamente:
   - ✅ Detecta Angular
   - ✅ Instala dependencias
   - ✅ Hace build de producción
   - ✅ Sirve la aplicación

### 3. Obtener URL del Frontend
   - Verás algo como: **`https://proyecto-birads-frontend-xxx.railway.app`**
   - **¡Esta es tu aplicación funcionando!** 🎉

---

## 🌟 **RESULTADO FINAL:**

✅ **Backend API**: `https://proyecto-birads-backend-xxx.railway.app`
✅ **Frontend App**: `https://proyecto-birads-frontend-xxx.railway.app` 
✅ **API Docs**: `https://proyecto-birads-backend-xxx.railway.app/docs`
✅ **Base de datos PostgreSQL**: Funcionando automáticamente
✅ **Certificado SSL**: Automático
✅ **Deploy automático**: Cada git push actualiza la app

---

## 💡 **¿TODO LISTO?**

1. ✅ **Código subido a GitHub** - HECHO
2. 🔄 **Siguiente**: Ve a **railway.app** y sigue los pasos de arriba
3. 🎯 **En 10 minutos**: Tu app estará funcionando en todo el mundo

**¡Avísame cuando hayas creado el proyecto en Railway y te ayudo con el siguiente paso!** 🚀