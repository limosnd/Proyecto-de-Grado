# 🎯 PASOS EXACTOS RAILWAY - ¡COPIA Y PEGA ESTO!

## **PASO 1: Ir a Railway** (2 minutos)

### 1. Abre tu navegador
- Ve a: **https://railway.app**
- Clic en **"Start a New Project"**

### 2. Conectar GitHub
- Clic en **"Login with GitHub"**
- Te redirige a GitHub
- Clic en **"Authorize Railway"**
- Acepta permisos

---

## **PASO 2: Crear Proyecto Backend** (3 minutos)

### 1. Seleccionar repositorio
- Clic en **"Deploy from GitHub repo"**
- Busca: **"Proyecto-de-Grado"**
- ✅ Selecciona el repositorio
- ✅ Branch: **"Dev"** (importante!)

### 2. Configurar servicio
- Railway detecta Python automáticamente
- **Root Directory**: Escribir `/backend`
- **Build Command**: Dejar vacío
- **Start Command**: `python app.py`
- Clic **"Deploy"**

---

## **PASO 3: Agregar Base de Datos** (1 minuto)

### En el dashboard de Railway:
1. Clic **"New Service"**
2. Clic **"Database"**
3. Selecciona **"PostgreSQL"**
4. Clic **"Add PostgreSQL"**
5. ✅ Railway crea la BD automáticamente

---

## **PASO 4: Conectar BD al Backend** (1 minuto)

### En tu servicio Backend:
1. Clic en el servicio **"backend"**
2. Ve a pestaña **"Variables"**
3. Railway automáticamente agrega `DATABASE_URL`
4. Si no está, clic **"New Variable"**:
   - **Name**: `DATABASE_URL`
   - **Value**: Se copia automáticamente de PostgreSQL

---

## **PASO 5: Obtener URL del Backend** (30 segundos)

### En el servicio Backend:
1. Ve a pestaña **"Settings"**
2. En **"Domains"** verás algo como:
   - `proyecto-de-grado-backend-production-xxxx.up.railway.app`
3. **¡COPIA ESTA URL!** 📋

---

## **PASO 6: Actualizar Frontend** (2 minutos)

### En tu computadora:
1. Abre: `frontend/src/app/config/api.config.ts`
2. Encuentra esta línea:
   ```typescript
   RAILWAY_URL: 'https://proyecto-birads-backend.railway.app',
   ```
3. Cámbiala por tu URL real:
   ```typescript
   RAILWAY_URL: 'https://proyecto-de-grado-backend-production-xxxx.up.railway.app',
   ```

### Subir cambios:
```bash
git add .
git commit -m "✅ URL backend actualizada"
git push origin Dev
```

---

## **PASO 7: Crear Frontend** (2 minutos)

### En Railway dashboard:
1. Clic **"New Service"**
2. Clic **"GitHub Repo"**
3. Selecciona **"Proyecto-de-Grado"**
4. **Root Directory**: `/frontend`
5. **Build Command**: `npm run build`
6. **Start Command**: `npm start`
7. Clic **"Deploy"**

---

## **PASO 8: ¡LISTO!** (30 segundos)

### URLs finales:
- **Frontend**: `https://proyecto-de-grado-frontend-xxxx.up.railway.app`
- **Backend**: `https://proyecto-de-grado-backend-xxxx.up.railway.app`
- **API Docs**: `https://proyecto-de-grado-backend-xxxx.up.railway.app/docs`

---

# 🎉 **¡TU APP ESTÁ EN VIVO!**

## ✅ **Lo que funciona automáticamente:**
- 🌍 **Acceso mundial** - Cualquiera puede usar tu app
- 🔒 **HTTPS automático** - Certificado SSL incluido
- 🔄 **Updates automáticos** - Cada git push actualiza la app
- 📊 **Monitoreo** - Logs y métricas en Railway
- 💾 **Base de datos** - PostgreSQL funcionando 24/7

## 🚀 **Para actualizaciones futuras:**
Solo haz `git push origin Dev` y Railway actualiza automáticamente!

---

**¡Empezamos con el PASO 1? Ve a railway.app y avísame cuando llegues ahí!** 🎯