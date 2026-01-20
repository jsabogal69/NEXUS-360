# NEXUS-360 GUARDRAILS
## Políticas y Reglas de Control del Sistema

---

## 🔴 MANDAMIENTO #1: NO DATA INVENTION

**Fecha establecido:** 2026-01-20

### Regla
> Ningún agente puede INVENTAR datos cuantitativos. Todos los valores numéricos deben provenir de fuentes verificables.

### Aplicación
| Tipo de Dato | Fuente Permitida | Si No Hay Datos |
|--------------|------------------|-----------------|
| Precios (MSRP, ASP) | Archivos POE (X-Ray, Amazon) | Mostrar "PENDIENTE" |
| Ventas mensuales | Archivos POE | Mostrar "PENDIENTE" |
| Market Share | Archivos POE | Mostrar "PENDIENTE" |
| TAM/SAM/SOM | Cálculo basado en POE | Mostrar "PENDIENTE" |
| TOP 10 Competidores | LLM (análisis cualitativo) | ✅ Permitido con disclaimer |
| Pros/Cons/Gaps | LLM (análisis) | ✅ Permitido |
| Sentimiento/Trends | LLM (análisis) | ✅ Permitido |

### Implementación
- **Scout Agent**: Usa LLM para TOP 10 pero marca precios como "⚡ ESTIMADO IA"
- **Strategist Agent**: Solo calcula MSRP/TAM si hay datos POE reales
- **Architect Agent**: Muestra badges de fuente de datos (🟢 POE / 🟡 ESTIMADO / 🔴 PENDIENTE)

---

## 📁 GUARDRAIL #2: GUIA CONTENIDO POE

**Fecha establecido:** 2026-01-20

### Regla
> El archivo "GUIA CONTENIDO POE" es el índice maestro que define qué columnas extraer de cada archivo.

### Archivos POE Reconocidos

| Archivo | Columnas Clave | Uso |
|---------|---------------|-----|
| `NicheDetailsProductsTab` | ASP, Click Share, Total Ratings, Launch Date | Precios, market share |
| `Helium_10_Xray` | Sales (Monthly), Revenue, BSR, FBA Fees, Active Sellers | Ventas, costos |
| `NicheDetailsSearchTermsTab` | Search Volume, Click Share, Conversion Rate | Keywords |
| `POE - Reviews` | Topic, % Mentions, Sentiment | Análisis cualitativo |

### Columnas Detectadas Automáticamente
```
price: Average Selling Price, ASP, Price, Precio, Cost, MSRP
sales: Sales (Monthly), Monthly Sales, Units, Ventas
revenue: Revenue, Ingresos, Monthly Revenue
bsr: BSR, Rank, Best Sellers Rank
reviews: Total Ratings, Reviews, Ratings
click_share: Click Share, Market Share
fba_fees: FBA Fees, Fulfillment Fee
```

---

## 🏷️ GUARDRAIL #3: TRANSPARENCIA DE FUENTES

**Fecha establecido:** 2026-01-20

### Regla
> Todo dato mostrado en el reporte debe indicar claramente su fuente.

### Badges de Fuente
| Badge | Color | Significado |
|-------|-------|-------------|
| 📁 DATOS POE | 🟢 Verde | Datos de archivos verificados - CONSISTENTES |
| ⚡ ESTIMADO IA | 🟡 Amarillo | Datos generados por LLM - PUEDEN VARIAR |
| ⚠️ PENDIENTE | 🔴 Rojo | Sin datos disponibles |

### Implementación
- Cada sección del reporte incluye badge de fuente
- Metodología y fórmula visible debajo de cada cálculo
- Disclaimer cuando datos son estimados

---

## 📊 GUARDRAIL #4: CONSISTENCIA DE REPORTES

**Fecha establecido:** 2026-01-20

### Regla
> Mismo input = Mismo output. Los reportes deben ser reproducibles.

### Causas de Inconsistencia (EVITAR)
- ❌ LLM genera datos nuevos cada scan
- ❌ Precios/ventas sin fuente POE

### Soluciones Implementadas
- ✅ Datos cuantitativos SOLO de archivos POE
- ✅ LLM solo para análisis cualitativo (pros, cons, gaps)
- ✅ Cache de resultados por archivo POE

---

## 🔍 GUARDRAIL #5: DETECCIÓN AUTOMÁTICA DE ARCHIVOS

**Fecha establecido:** 2026-01-20

### Regla
> El sistema debe detectar automáticamente archivos de pricing sin configuración manual.

### Keywords de Nombre de Archivo
```
xray, x-ray, helium, h10, cerebro, magnet (Helium10)
amazon, seller, product, listing, competitor (Amazon)
price, precio, pricing, sales, ventas (Genérico)
niche, analysis, export, data (Exports)
```

### Detección por Columnas
Si el archivo tiene ≥2 de estas columnas, se considera archivo de pricing:
- price, sales, revenue, bsr, asin, title, reviews
- precio, ventas, ingresos, titulo, costo

---

## 🛡️ GUARDRAIL #6: COMPLIANCE (GUARDIAN)

**Fecha establecido:** Previo

### Categorías de Producto con Reglas Especiales
| Categoría | Regulaciones |
|-----------|-------------|
| Suplementos | FDA, etiquetado nutricional |
| Belleza/Personal Care | Ingredientes, alergenos |
| Electrónicos | FCC, certificaciones |
| Niños | CPSC, seguridad |

### Keywords para Detección Belleza/Personal Care
```
skincare, haircare, cosmetic, shampoo, conditioner, lotion, cream,
serum, moisturizer, cleanser, soap, deodorant, toothpaste, mouthwash,
razor, shaving, body wash, sunscreen, makeup, foundation, mascara...
```

---

## 📋 CHANGELOG DE GUARDRAILS

| Fecha | Guardrail | Cambio |
|-------|-----------|--------|
| 2026-01-20 | #1 | Establecido NO DATA INVENTION |
| 2026-01-20 | #2 | Añadido soporte columnas POE Guide |
| 2026-01-20 | #3 | Implementado badges de fuente |
| 2026-01-20 | #4 | Establecido principio de consistencia |
| 2026-01-20 | #5 | Expandida detección automática |
| 2026-01-19 | #6 | Expandido Guardian Beauty/Personal Care |

---

## ✏️ CÓMO AGREGAR NUEVOS GUARDRAILS

1. Documentar en este archivo con fecha
2. Implementar en el agente correspondiente
3. Agregar tests si aplica
4. Actualizar CHANGELOG
