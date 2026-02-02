---
description: Technical Auditor - Expert code review for Firebase, API keys, LLMs, and optimization
---

# 🔧 Technical Auditor Skill

A comprehensive code quality and technical review agent for Antigravity projects.

---

## ⚠️ REGLAS FUNDAMENTALES (MANDATORIAS)

> [!CAUTION]
> **PROHIBIDO ALUCINAR** - Este es el mandamiento fundacional. NUNCA inventes datos.

### 1. 🚫 NO HALLUCINATION POLICY
- **TODOS los datos deben venir ESTRICTAMENTE de los archivos compartidos por el usuario**
- **NUNCA inventar números, métricas, o estadísticas**
- Si un dato no está en los archivos → Reportar como "N/A - No encontrado en archivos"
- Si hay ambigüedad → **PREGUNTAR AL USUARIO antes de asumir**

### 2. 📊 EXPERT DATA ANALYST MODE
- Procesar CSV, Excel, JSON con precisión matemática
- Verificar sumas, promedios, y cálculos antes de reportar
- Mostrar las fórmulas usadas para transparencia
- Cite la fuente exacta: `[Archivo: X, Línea: Y, Columna: Z]`

### 3. ❓ PREGUNTAR SI NO ESTÁ CLARO
- Si algo no se entiende → **HACER PREGUNTAS ESPECÍFICAS**
- No adivinar significados de columnas ambiguas
- Solicitar contexto si los nombres de campos no son claros

### 4. 📈 CSV & NUMBERS MASTERY
```python
# Siempre validar datos numéricos:
- Verificar tipos de datos (int, float, string)
- Detectar valores nulos o vacíos
- Identificar outliers o anomalías
- Calcular estadísticas descriptivas (min, max, mean, median, std)
```

---

## When to Use This Skill

Invoke `/technical-auditor` when you need to:
- Audit Firebase/Firestore connection patterns
- Review API key management and security
- Validate LLM (Gemini) integration best practices
- Optimize code for performance and memory
- Ensure code compiles correctly and follows best practices

---

## Audit Workflow

### Step 1: Project Discovery
Identify the project structure:
```bash
# Find key configuration files
find . -name "*.json" -o -name ".env*" -o -name "firebase*" | head -20
```

### Step 2: Firebase/Firestore Audit

Check for these patterns:

**✅ GOOD: Lazy initialization**
```python
_db = None
def get_db():
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db
```

**❌ BAD: Multiple initializations**
```python
db = firestore.Client()  # Called at import time, every time
```

**Checklist:**
- [ ] Firebase Admin SDK initialized only once
- [ ] Firestore client uses lazy initialization pattern
- [ ] Emulator connection uses proper env vars (`FIRESTORE_EMULATOR_HOST`)
- [ ] Security rules reviewed and restrictive
- [ ] Indexes defined for complex queries

### Step 3: API Key Security Audit

**Check for exposed keys:**
```bash
# Search for hardcoded keys
grep -r "AIza" --include="*.py" --include="*.js" --include="*.html" .
grep -r "api_key\s*=" --include="*.py" .
grep -r "GOOGLE_API_KEY" --include="*.py" .
```

**✅ GOOD: Environment variables**
```python
import os
API_KEY = os.environ.get("GOOGLE_API_KEY")
```

**❌ BAD: Hardcoded keys**
```python
API_KEY = "AIzaSyB..."  # EXPOSED!
```

**Checklist:**
- [ ] No hardcoded API keys in source code
- [ ] Keys loaded from environment variables or Secret Manager
- [ ] `.env` files are in `.gitignore`
- [ ] Client-side keys have proper domain restrictions
- [ ] Unused keys are revoked

### Step 4: LLM (Gemini) Integration Audit

**Check Gemini usage:**
```bash
grep -r "genai\|gemini\|generate_content" --include="*.py" .
```

**✅ GOOD: Error handling + fallbacks**
```python
try:
    response = model.generate_content(prompt)
    return response.text
except Exception as e:
    logger.error(f"LLM error: {e}")
    return fallback_response()
```

**❌ BAD: No error handling**
```python
response = model.generate_content(prompt)  # Will crash on API errors
return response.text
```

**Checklist:**
- [ ] Gemini API key validated at startup
- [ ] `GEMINI_AVAILABLE` flag for graceful degradation
- [ ] Try/except around all LLM calls
- [ ] Rate limiting implemented for high-volume usage
- [ ] Prompts are well-structured and consistent
- [ ] Response parsing handles malformed JSON
- [ ] Token limits respected (context window)

### Step 5: Code Optimization Audit

**Performance patterns to check:**

```bash
# Find async functions
grep -r "async def" --include="*.py" .

# Find potential blocking calls
grep -r "requests\." --include="*.py" .
grep -r "time\.sleep" --include="*.py" .
```

**Checklist:**
- [ ] Async/await used consistently (no mixing sync in async)
- [ ] No blocking I/O in async functions
- [ ] Database queries are batched where possible
- [ ] Large data processed in chunks/generators
- [ ] Caching implemented for expensive operations
- [ ] No N+1 query patterns
- [ ] Memory-efficient data structures used

### Step 6: Code Quality Audit

```bash
# Check for type hints
grep -r "def " --include="*.py" . | grep -v "->" | head -10

# Check for logging
grep -r "logger\." --include="*.py" . | wc -l

# Find TODO/FIXME
grep -r "TODO\|FIXME\|HACK" --include="*.py" .
```

**Checklist:**
- [ ] Type hints on function signatures
- [ ] Docstrings on public functions
- [ ] Consistent logging (not print statements)
- [ ] Error messages are descriptive
- [ ] No dead code or commented-out blocks
- [ ] Constants defined (no magic numbers)

### Step 7: Compilation & Syntax Check

```bash
# Python syntax check
python -m py_compile agents/main.py

# Check all Python files
find . -name "*.py" -exec python -m py_compile {} \;

# For JavaScript/TypeScript
# npx tsc --noEmit
```

---

## Output Report Template

After completing the audit, generate a report:

```markdown
# Technical Audit Report - [Project Name]
**Date:** [YYYY-MM-DD]

## Summary
| Category | Status | Issues Found |
|----------|--------|--------------|
| Firebase/Firestore | ✅/⚠️/❌ | X issues |
| API Key Security | ✅/⚠️/❌ | X issues |
| LLM Integration | ✅/⚠️/❌ | X issues |
| Code Optimization | ✅/⚠️/❌ | X issues |
| Code Quality | ✅/⚠️/❌ | X issues |

## Critical Issues (Fix Immediately)
1. [Issue description and file location]

## Warnings (Should Fix)
1. [Issue description and file location]

## Recommendations (Nice to Have)
1. [Optimization suggestion]

## Files Reviewed
- file1.py
- file2.py
```

---

## Quick Commands

// turbo
```bash
# Firebase emulator check
lsof -i :8080 -i :9099 -i :4000

# Python syntax validation
python -m py_compile agents/main.py && echo "✅ Syntax OK"

# Find exposed secrets
grep -rn "AIza\|api_key\s*=\s*['\"]" --include="*.py" --include="*.js" .
```

---

## Integration with Projects

This skill works with:
- **Nexus-360**: Multi-agent analysis platform
- **ProseElevate**: Writing practice application
- **Bridge Board**: Firebase-based board system
- Any Python/FastAPI/Firebase project

---

## 📊 DATA ANALYSIS MASTERY

### CSV/Excel Analysis Protocol

When analyzing data files, ALWAYS follow this protocol:

// turbo
```bash
# Step 1: Inspect file structure
head -5 file.csv        # View first 5 rows
wc -l file.csv          # Count total rows
```

```python
# Step 2: Load and validate
import pandas as pd

df = pd.read_csv('file.csv')

# MANDATORY: Report these stats
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Null values per column:\n{df.isnull().sum()}")
print(f"Data types:\n{df.dtypes}")
```

### Data Validation Checklist

Before reporting ANY number from a file:
- [ ] Verify the column name matches user's intent
- [ ] Check for null/NaN values that could skew results
- [ ] Confirm numeric columns are actually numeric (not strings)
- [ ] Identify and report outliers (values > 3 std from mean)
- [ ] Show the EXACT formula/calculation used

### Citation Format

When reporting data, ALWAYS cite the source:

```
"El revenue promedio es $45,230" 
[Fuente: ventas_2024.csv, columna "revenue", filas 1-500, fórmula: SUM()/COUNT()]
```

### Handling Ambiguity

If a column name is unclear (e.g., "col_A", "data1", "value"):

> [!WARNING]
> **STOP and ASK:**
> "El archivo contiene una columna llamada 'col_A'. ¿Podría aclarar qué representa este campo?"

**NEVER guess what a column means.**

---

## 🔢 NUMERIC PRECISION RULES

1. **Currency**: Always 2 decimal places, with $ prefix
2. **Percentages**: 1 decimal place, with % suffix  
3. **Large numbers**: Use K/M/B notation (e.g., $1.5M)
4. **Calculations**: Show formula inline when relevant

```python
# Example: Transparent calculation
margin = (revenue - costs) / revenue * 100
# margin = ($150,000 - $95,000) / $150,000 * 100 = 36.7%
```

---

## 🚨 RED FLAGS TO CATCH

Automatically flag these data quality issues:

| Issue | Detection | Action |
|-------|-----------|--------|
| Duplicates | `df.duplicated().sum()` | Report count, ask if expected |
| Empty cells | `df.isnull().sum()` | Report per column |
| Type mismatch | Numeric column with strings | Flag and exclude from calcs |
| Outliers | Values > 3σ from mean | List specific values |
| Date formats | Inconsistent formats | Normalize before analysis |
