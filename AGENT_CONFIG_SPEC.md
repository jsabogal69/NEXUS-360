# NEXUS-360 Configuración de Agentes Críticos
## Especificaciones Técnicas para Mercado Amazon US

---

## 1. STRATEGIST (El Arquitecto de Diferenciación)

### Objetivo
En el mercado US, competir por precio es una carrera al fondo. Este agente debe enfocarse en el **Product-Market Fit psicológico**.

### Configuración de Enfoque

| Módulo | Especificación |
|--------|----------------|
| **Análisis de Pain Points** | Clasificar quejas en: Funcionalidad, Estética, Durabilidad, Empaque |
| **Propuesta de Valor Única (USP)** | Generar 3 ángulos de marketing basados en gaps encontrados |
| **Framework** | Aplicar modelo **Jobs-to-be-Done** |

### Regla de Decisión Táctica
```
SI gap_insatisfacción_líder < 20%:
    SUGERIR: "Iteración de producto antes de invertir"
    FLAG: AMARILLO (Riesgo Moderado)
```

### System Prompt Recomendado
```
Actúa como un Consultor Senior de Marca en EE.UU. Analiza el archivo 
de reviews adjunto. Identifica las 3 frustraciones recurrentes en 
reseñas de 2 y 3 estrellas. Propón una modificación física al producto 
o un bundle de valor que anule esas quejas. Estima el impacto en 
Conversion Rate.
```

---

## 2. GUARDIAN (El Escudo Legal y Operativo)

### Objetivo
El mercado de EE.UU. es altamente litigioso y regulado. Este agente es el **filtro de viabilidad real**.

### Configuración de Enfoque

| Módulo | Especificación |
|--------|----------------|
| **Certificaciones** | Cruzar con CPSC, FDA, EPR |
| **Análisis de Patentes** | Escaneo de red flags en títulos/descripciones |
| **Restricciones de Categoría** | Identificar gating (Hazmat, Pesticides, Topical) |

### Poder de Veto Automático
```
SI categoría == "Topical" AND certificado_COA == False:
    VETO: ACTIVADO
    FLAG: ROJO (Alto Riesgo)
    MENSAJE: "Producto requiere Certificate of Analysis"
```

### Matriz de Riesgos (para Dossier)

| Riesgo | Descripción | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Regulatorio | Certificaciones faltantes | ALTO | Obtener antes de envío |
| Patentes | Diseño similar a existente | MEDIO | Consulta legal |
| Gating | Categoría restringida | ALTO | Solicitar aprobación Amazon |
| Liability | Producto de riesgo personal | CRÍTICO | Seguro de responsabilidad |

---

## 3. MATHEMATICIAN (El Auditor de Rentabilidad)

### Objetivo
Para 2026, los costos de PPC y logística en Amazon US son volátiles. Este agente debe ser **pesimista para ser realista**.

### Configuración de Enfoque

| Módulo | Especificación |
|--------|----------------|
| **Simulación de Escenarios** | 3 escenarios: Conservador, Esperado, Agresivo |
| **TACoS** | Total Advertising Cost of Sales (no solo ACoS) |
| **Logística** | Comparar 3PL vs FBA, especialmente Q4 |

### Umbrales de Éxito (US Market)

| Variable | Umbral Mínimo | Nota |
|----------|---------------|------|
| Net Margin (Post-PPC) | > 20% | Después de todos los costos |
| ROI (Anualizado) | > 100% | Para justificar el riesgo |
| Conversion Rate Est. | > 10% | Para ser competitivo |
| TACoS Sostenible | < 15% | Para rentabilidad a largo plazo |

### Modelo de 3 Escenarios

```
CONSERVADOR (Pesimista):
  - Ventas: -30% vs estimado
  - PPC: +40% vs estimado
  - Margen: Debe seguir siendo > 15%

ESPERADO (Base):
  - Ventas: Según datos POE
  - PPC: ACoS promedio de categoría
  - Margen: Target > 25%

AGRESIVO (Optimista):
  - Ventas: +20% vs estimado
  - PPC: -20% vs estimado
  - Margen: Potencial > 35%
```

---

## 4. Implementación Técnica

### Archivos a Modificar

| Agente | Archivo | Cambios |
|--------|---------|---------|
| STRATEGIST | `agents/nexus_4_strategist/core.py` | Pain points, USP, Jobs-to-be-Done |
| GUARDIAN | `agents/nexus_8_guardian/core.py` | Matriz de riesgos, Veto automático |
| MATHEMATICIAN | `agents/nexus_5_mathematician/core.py` | 3 escenarios, TACoS, umbrales |

### Prioridad de Implementación

1. 🔴 **GUARDIAN Veto Automático** - Crítico para evitar pérdidas
2. 🟡 **MATHEMATICIAN 3 Escenarios** - Mejora decisiones de inversión
3. 🟢 **STRATEGIST Pain Points** - Mejora diferenciación

---

## 5. Próximos Pasos

- [x] Implementar clasificación de Pain Points en Strategist ✅
- [x] Agregar Matriz de Riesgos al output de Guardian ✅
- [x] Crear modelo de 3 escenarios en Mathematician ✅
- [x] Definir umbrales de veto automático ✅
- [ ] Integrar análisis de patentes (fuente externa) - PENDIENTE API

---

*Especificación técnica implementada en NEXUS-360 v2.0 (2026-01-20)*
