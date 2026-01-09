# NEXUS-360 Operational Rules

## 1. Memory First
* **Protocol**: No agent acts without checking `validated_intelligence` in Firebase.
* **Requirement**: Before generating new insights or taking action, query the shared knowledge base to avoid redundancy and ensure context.

## 2. Persistence
* **Protocol**: Every process must log its state.
* **Requirement**: Updates must be pushed to the `projects` collection or relevant sub-collections (`raw_inputs`, `outputs`) immediately. Stateless operation is forbidden.

## 3. Visual Audit
* **Protocol**: Brand Consistency.
* **Requirement**: Use the Agentic Browser to ensure `www.obs360.co` styling (colors, typography, "Calidez Latina" tone) is mirrored in the dashboard.
* **Check**: Generated HTML/PDFs must match the OBS360 visual identity.

## 4. The Guardian's Gate
* **Protocol**: Data Validation.
* **Requirement**: All data entering the `validated_intelligence` collection and all final `outputs` MUST be validated by NEXUS-8.
