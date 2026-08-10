"""Pipeline de recrutement — qualification, objections, closing, mémoire.

Modules inspirés de sellkit/src/pipeline/ :
- qualification.py : FIELD_QUESTIONS, STAGE_LABELS, CLOSING_STAGES
- objections.py : OBJECTION_CATALOG (8 types), detect_objection() LLM + fallback
- closing.py : ClosingType (5 signaux), STAGE_MAP, detect_closing() LLM + fallback
- memory.py : ProspectMemory, extract_memory() LLM, merge, count, next_missing, format
"""
