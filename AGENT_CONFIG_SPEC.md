# NEXUS-360 Configuración de Agentes Críticos
## Especificaciones Técnicas para Mercado Amazon US (v2.5)

---

## 1. Global Architecture (New V2.5)
- **LLM Engine**: Gemini 1.5 Pro (Strategy) + **Gemini 3.0 Flash (Calculations/Code Execution)** + Gemini 2.0 Flash (Fallback)
- **Database**: Firebase Firestore (Production) / In-Memory Mock (Dev/Fallback)
- **Storage**: Google Drive (Inputs) + Firebase Storage (Assets)
- **Frontend**: HTML5/JS Dashboard (Port 8000)

---

## 2. NEXUS-2 SCOUT (Market Intelligence)
- **Status**: 🟢 OPERATIONAL / UPGRADED (v2.5)
- **Core Function**: Market Intelligence & Data Ingestion
- **Recent Upgrades**:
  - `DataExpert` "Header Hunter" v1.0: Robust CSV/Excel parsing requiring header detection.
  - **POE Priority Logic**: Automatically prioritizes verified X-Ray/Search Terms data over LLM estimates.
  - **Market Share v2**: Calculates share based on real review counts when available.

---

## 3. STRATEGIST (El Arquitecto de Diferenciación)

### Objetivo
En el mercado US, competir por precio es una carrera al fondo. Este agente debe enfocarse en el **Product-Market Fit psicológico**.

### Configuración de Enfoque
| Módulo | Especificación |
|--------|----------------|
| **Análisis de Pain Points** | Clasificar quejas en: Funcionalidad, Estética, Durabilidad, Empaque |
| **Propuesta de Valor Única** | Generar 3 ángulos de marketing basados en gaps encontrados |
| **Framework** | Aplicar modelo **Jobs-to-be-Done** |

---

## 4. GUARDIAN (El Escudo Legal y Operativo)

### Objetivo
El mercado de EE.UU. es altamente litigioso y regulado. Este agente es el **filtro de viabilidad real**.

### Poder de Veto Automático
```
SI categoría == "Topical" AND certificado_COA == False:
    VETO: ACTIVADO
    FLAG: ROJO (Alto Riesgo)
    MENSAJE: "Producto requiere Certificate of Analysis"
```

---

## 5. MATHEMATICIAN (El Auditor de Rentabilidad)

### Objetivo
Usar **Gemini 3.0 Code Execution** para cálculos financieros precisos (TACoS, ROI, Márgenes).

### Umbrales de Éxito (US Market)
| Variable | Umbral Mínimo | Nota |
|----------|---------------|------|
| Net Margin (Post-PPC) | > 20% | Después de todos los costos |
| ROI (Anualizado) | > 100% | Para justificar el riesgo |
| TACoS Sostenible | < 15% | Para rentabilidad a largo plazo |

---

## 9. NEXUS-9 Technical Auditor (The Watchman)
- **Status**: 🟢 OPERATIONAL
- **Role**: Code Integrity & Security Guardian
- **Capabilities**:
  - Static Code Analysis (`audit_codebase.py`)
  - Secret Scanning (`scan_secrets.py`)
  - Integration Integrity Checks (Firebase/Drive)
- **Protocol**: Enforces "Zero Trust" data policy and ensures no silent failures.

---

*Especificación técnica actualizada en NEXUS-360 v2.5 (2026-02-03)*
