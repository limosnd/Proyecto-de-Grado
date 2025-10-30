from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    rol = Column(String(50), nullable=False)
    observaciones = Column(Text)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default='now()')

class Reporte(Base):
    __tablename__ = "reportes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    resultado_birads = Column(String(20), nullable=False)
    detalles_json = Column(Text, nullable=False)
    nombre_paciente = Column(String(100))