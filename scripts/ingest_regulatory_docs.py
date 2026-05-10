#!/usr/bin/env python3
"""
GlobalRegAI — Regulatory Document Ingestion Pipeline
Fetches public regulatory guidance from FDA, EMA, MFDS, ISO
and stores embeddings in Qdrant for RAG.

Requirements: pip install requests qdrant-client ollama tqdm
"""

import json
import os
import sys
import time
import hashlib
from pathlib import Path
from typing import Optional
import requests
from tqdm import tqdm

# ── Config ──────────────────────────────────────────────────
OLLAMA_URL   = os.getenv("OLLAMA_URL",  "http://localhost:11434")
QDRANT_URL   = os.getenv("QDRANT_URL",  "http://localhost:6333")
EMBED_MODEL  = os.getenv("EMBED_MODEL", "nomic-embed-text")
COLLECTION   = "globalregai_regulations"
CHUNK_SIZE   = 800   # characters per chunk
CHUNK_OVERLAP= 150

# ── Public Regulatory Sources (free, no API key required) ────
REGULATORY_SOURCES = [

    # ── FDA Guidance Documents ───────────────────────────────
    {
        "agency": "FDA",
        "category": "Medical Device",
        "title": "Design Controls for Medical Devices (21 CFR 820.30)",
        "url": "https://www.fda.gov/medical-devices/quality-system-qs-regulationmedical-device-good-manufacturing-practices/design-controls",
        "type": "guidance"
    },
    {
        "agency": "FDA",
        "category": "Medical Device",
        "title": "Quality System Regulation (QSR) / QMSR Overview",
        "url": "https://www.fda.gov/medical-devices/quality-system-qs-regulationmedical-device-good-manufacturing-practices",
        "type": "regulation"
    },
    {
        "agency": "FDA",
        "category": "Pharmaceutical",
        "title": "Current Good Manufacturing Practice (cGMP) for Drugs",
        "url": "https://www.fda.gov/drugs/pharmaceutical-quality-resources/current-good-manufacturing-practice-cgmp-regulations",
        "type": "regulation"
    },
    {
        "agency": "FDA",
        "category": "Pharmaceutical",
        "title": "Process Validation: General Principles and Practices",
        "url": "https://www.fda.gov/media/71021/download",
        "type": "guidance"
    },
    {
        "agency": "FDA",
        "category": "Cosmetics",
        "title": "Cosmetic Labeling Guide",
        "url": "https://www.fda.gov/cosmetics/cosmetics-labeling-regulations/cosmetic-labeling-guide",
        "type": "guidance"
    },
    {
        "agency": "FDA",
        "category": "Food",
        "title": "FSMA Food Safety Modernization Act Overview",
        "url": "https://www.fda.gov/food/food-safety-modernization-act-fsma",
        "type": "regulation"
    },
    {
        "agency": "FDA",
        "category": "Food",
        "title": "Hazard Analysis and Risk-Based Preventive Controls (HARPC)",
        "url": "https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-final-rule-preventive-controls-human-food",
        "type": "regulation"
    },

    # ── EMA (European Medicines Agency) ─────────────────────
    {
        "agency": "EMA",
        "category": "Pharmaceutical",
        "title": "EMA GMP Guidelines Overview",
        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/compliance/good-manufacturing-practice",
        "type": "guidance"
    },
    {
        "agency": "EMA",
        "category": "Medical Device",
        "title": "EU MDR 2017/745 — Medical Device Regulation",
        "url": "https://www.ema.europa.eu/en/human-regulatory-overview/research-development/scientific-guidelines",
        "type": "regulation"
    },

    # ── MFDS (Korea Ministry of Food and Drug Safety) ────────
    {
        "agency": "MFDS",
        "category": "Medical Device",
        "title": "MFDS Medical Device Act Overview",
        "url": "https://www.mfds.go.kr/eng/brd/m_60/view.do?seq=71741",
        "type": "regulation"
    },
    {
        "agency": "MFDS",
        "category": "Pharmaceutical",
        "title": "MFDS GMP Regulation for Pharmaceuticals",
        "url": "https://www.mfds.go.kr/eng/brd/m_60/list.do",
        "type": "regulation"
    },

    # ── AEMPS (Spain — Agencia Española de Medicamentos) ────
    {
        "agency": "AEMPS",
        "category": "Medical Device",
        "title": "Regulación de Productos Sanitarios en España",
        "url": "https://www.aemps.gob.es/productos-sanitarios/regulacion-de-productos-sanitarios/",
        "type": "regulation"
    },
    {
        "agency": "AEMPS",
        "category": "Pharmaceutical",
        "title": "Guía de Normas de Correcta Fabricación (GMP)",
        "url": "https://www.aemps.gob.es/industria-farmaceutica/inspeccion-de-normas-de-correcta-fabricacion/",
        "type": "guidance"
    },

    # ── COFEPRIS (Mexico) ────────────────────────────────────
    {
        "agency": "COFEPRIS",
        "category": "General",
        "title": "Marco Jurídico de Dispositivos Médicos",
        "url": "https://www.gob.mx/cofepris/acciones-y-programas/dispositivos-medicos-32115",
        "type": "regulation"
    },

    # ── ANMAT (Argentina) ────────────────────────────────────
    {
        "agency": "ANMAT",
        "category": "Pharmaceutical",
        "title": "Normativas de Medicamentos",
        "url": "https://www.argentina.gob.ar/anmat/regulados/medicamentos/normativas",
        "type": "regulation"
    },
    {
        "agency": "ANMAT",
        "category": "Food",
        "title": "Código Alimentario Argentino",
        "url": "https://www.argentina.gob.ar/anmat/codigoalimentario",
        "type": "regulation"
    },

    # ── ISP (Chile) ──────────────────────────────────────────
    {
        "agency": "ISP",
        "category": "Medical Device",
        "title": "Regulación de Dispositivos Médicos en Chile",
        "url": "https://www.ispch.cl/prestacion/dispositivos-medicos/",
        "type": "regulation"
    },

    # ── INVIMA (Colombia) ────────────────────────────────────
    {
        "agency": "INVIMA",
        "category": "General",
        "title": "Normatividad y Trámites",
        "url": "https://www.invima.gov.co/normatividad",
        "type": "regulation"
    },

    # ── DIGEMID (Peru) ───────────────────────────────────────
    {
        "agency": "DIGEMID",
        "category": "Pharmaceutical",
        "title": "Marco Normativo de Medicamentos",
        "url": "http://www.digemid.minsa.gob.pe/Main.asp?Seccion=3",
        "type": "regulation"
    },

    # ── ISO Standards (publicly available summaries) ─────────
    {
        "agency": "ISO",
        "category": "Medical Device",
        "title": "ISO 13485:2016 — Quality Management Systems for Medical Devices",
        "url": "https://www.iso.org/standard/59752.html",
        "type": "standard"
    },
    {
        "agency": "ISO",
        "category": "Medical Device",
        "title": "ISO 14971:2019 — Risk Management for Medical Devices",
        "url": "https://www.iso.org/standard/72704.html",
        "type": "standard"
    },
    {
        "agency": "ISO",
        "category": "Medical Device",
        "title": "IEC 62304:2006 — Medical Device Software Lifecycle",
        "url": "https://www.iso.org/standard/38421.html",
        "type": "standard"
    },
    {
        "agency": "ISO",
        "category": "General",
        "title": "ISO 9001:2015 — Quality Management Systems",
        "url": "https://www.iso.org/standard/62085.html",
        "type": "standard"
    },
]

# ── Inline regulatory knowledge (always available without internet) ──
INLINE_KNOWLEDGE = [
    {
        "agency": "FDA",
        "category": "Medical Device",
        "title": "21 CFR Part 820 — Quality System Regulation Key Requirements",
        "content": """
FDA 21 CFR Part 820 — Quality System Regulation (QSR) / QMSR Key Requirements:

DESIGN CONTROLS (820.30):
- Design and development planning required
- Design input (requirements) must be documented
- Design output must meet input requirements
- Design review at each stage
- Design verification and validation
- Design transfer to production
- Design changes controlled with review/approval
- Design history file (DHF) maintained

DOCUMENT CONTROLS (820.40):
- Document approval before issuance
- Changes reviewed and approved
- Obsolete documents removed from use

PURCHASING CONTROLS (820.50):
- Supplier qualification
- Approved supplier list
- Purchase orders specify requirements

PRODUCTION & PROCESS CONTROLS (820.70):
- Process controls documented in procedures
- Environmental controls where required
- Personnel qualification
- Equipment maintenance and calibration

CORRECTIVE AND PREVENTIVE ACTION (820.100):
- CAPA system required
- Root cause analysis
- Effectiveness verification

RECORDS (820.180):
- Device Master Record (DMR)
- Device History Record (DHR)
- Quality System Record (QSR)

GMP AUDIT CHECKLIST KEY AREAS:
1. Management responsibility and quality policy
2. Document and record control
3. Design controls
4. Purchasing and supplier controls
5. Production controls
6. Inspection and testing
7. Nonconforming product handling
8. CAPA system
9. Complaint handling
10. Internal audit program
""",
    },
    {
        "agency": "FDA/ICH",
        "category": "Pharmaceutical",
        "title": "ICH Q10 Pharmaceutical Quality System",
        "content": """
ICH Q10 — Pharmaceutical Quality System (PQS) Framework:

KEY ELEMENTS:
1. Process Performance and Product Quality Monitoring
   - Statistical process control (SPC)
   - Trend analysis
   - Product quality reviews (PQR/APR)

2. Corrective Action / Preventive Action (CAPA)
   - Investigation of deviations and OOS results
   - Root cause analysis
   - Effectiveness checks

3. Change Management
   - Change control procedure
   - Impact assessment
   - Post-change monitoring

4. Management Review
   - Quality metrics
   - Resource allocation
   - Continuous improvement

GMP COMPLIANCE REQUIREMENTS:
- Batch records complete and accurate
- Equipment qualification (IQ/OQ/PQ)
- Cleaning validation
- Process validation
- Stability programs
- Environmental monitoring
- Personnel training records

KEY REGULATORY SUBMISSIONS:
- NDA (New Drug Application) — FDA
- ANDA (Abbreviated NDA) — FDA
- MAA (Marketing Authorization Application) — EMA
- IND (Investigational New Drug) — FDA
""",
    },
    {
        "agency": "ISO",
        "category": "Medical Device",
        "title": "ISO 13485:2016 Key Requirements Summary",
        "content": """
ISO 13485:2016 — Medical Devices Quality Management System

SCOPE: Requirements for organizations in the design, production,
installation and servicing of medical devices and related services.

CLAUSE 4 — Quality Management System:
- Document control (4.2.3)
- Record control (4.2.4)
- Quality manual required

CLAUSE 5 — Management Responsibility:
- Quality policy
- Quality objectives
- Management review (at planned intervals)

CLAUSE 6 — Resource Management:
- Human resources competency
- Infrastructure maintenance
- Work environment control

CLAUSE 7 — Product Realization:
7.1 Planning of product realization
7.2 Customer-related processes
7.3 Design and development (can be excluded for manufacturers only)
7.4 Purchasing
7.5 Production and service provision
7.5.2 Cleanliness of product
7.5.3 Installation activities
7.5.4 Service activities
7.5.5 Particular requirements for sterile medical devices
7.5.6 Validation of processes for production and service provision
7.5.7 Particular requirements for validation of sterile barrier systems
7.5.8 Identification
7.5.9 Traceability
7.5.10 Customer property
7.5.11 Preservation of product
7.6 Control of monitoring and measuring equipment

CLAUSE 8 — Measurement, Analysis and Improvement:
8.2.1 Feedback
8.2.2 Complaint handling
8.2.3 Reporting to regulatory authorities
8.2.4 Internal audit
8.3 Control of nonconforming product
8.4 Analysis of data
8.5 Improvement — CAPA

KEY DIFFERENCES FROM ISO 9001:
- Medical device specific requirements throughout
- Risk management integration (links to ISO 14971)
- Regulatory requirements explicitly included
- Sterile product requirements
- Post-market surveillance requirements
""",
    },
    {
        "agency": "EMA",
        "category": "Pharmaceutical",
        "title": "EU GMP Guidelines Part I — Basic Requirements for Medicinal Products",
        "content": """
EU GMP Guidelines Part I — Key Requirements:

CHAPTER 1: PHARMACEUTICAL QUALITY SYSTEM
- Pharmaceutical Quality System (PQS) based on ICH Q10
- Quality Risk Management integrated
- Management oversight and review

CHAPTER 2: PERSONNEL
- Qualified Person (QP) — legally required in EU
- Head of Production and Quality Control independence
- Training program documented
- Personal hygiene requirements

CHAPTER 3: PREMISES AND EQUIPMENT
- Designed to minimize contamination risk
- Classified cleanrooms for sterile products
- Equipment qualification (IQ/OQ/PQ)
- Calibration program

CHAPTER 4: DOCUMENTATION
- Specifications (materials, products)
- Manufacturing formulae and instructions
- Procedures and records
- Batch manufacturing records
- Electronic records acceptable (21 CFR Part 11 equivalent)

CHAPTER 5: PRODUCTION
- Starting material controls
- Batch number system
- In-process controls
- Packaging operations
- Rejected, recovered, and returned materials

CHAPTER 6: QUALITY CONTROL
- QC department independence
- Sampling procedures
- Testing specifications
- Out-of-specification (OOS) investigations
- Reference and retention samples
- Stability program

CHAPTER 7: OUTSOURCED ACTIVITIES
- Contract manufacturing (CMO) requirements
- Technical agreement required
- Auditing of contract facilities

CHAPTER 8: COMPLAINTS AND PRODUCT RECALL
- Recall procedures
- Competent authority notification requirements
- Mock recall exercises

ANNEX 1: MANUFACTURE OF STERILE MEDICINAL PRODUCTS (2022 revision)
- Contamination Control Strategy (CCS)
- Environmental monitoring
- Sterility testing and process simulation

ANNEX 11: COMPUTERISED SYSTEMS
- System validation requirements
- Data integrity requirements
- Audit trail requirements
""",
    },
    {
        "agency": "MFDS",
        "category": "Medical Device",
        "title": "Korea Medical Device GMP Requirements",
        "content": """
한국 의료기기 GMP 요구사항 (MFDS)

의료기기법 및 GMP 고시 주요 내용:

등급 분류:
- 1등급: 위해도 낮음 (신고)
- 2등급: 중간 위해도 (허가 또는 인증)
- 3등급: 중간~높은 위해도 (허가)
- 4등급: 높은 위해도 (허가)

GMP 적합인정 (제조업허가):
- 품질경영시스템 구축 (ISO 13485 기반)
- 제조 및 품질관리 기준서 작성
- 문서 및 기록 관리
- 설계개발 관리
- 구매 관리
- 생산 관리
- 시판후 관리

인허가 서류:
- 기술문서 (Technical File)
- 임상시험자료 (해당 시)
- 성능시험 성적서
- 생물학적 안전성 시험
- 전기안전 시험 (해당 시)

MFDS 심사 프로세스:
1. 제조업 허가 / GMP 심사
2. 품목허가 신청
3. 기술문서 심사
4. 임상자료 검토 (해당 시)
5. 허가증 발급

국제 상호인정협정 (MRA):
- IMDRF (International Medical Device Regulators Forum) 참여국
- APEC RHSC 참여

수출 지원:
- 수출용 의료기기 제조증명서
- 수출국 요구 서류 지원
""",
    },
    {
        "agency": "GLOBAL",
        "category": "Audit",
        "title": "GMP Audit Checklist — Universal Framework",
        "content": """
GMP AUDIT CHECKLIST — Universal Framework for Regulatory Audits

PRE-AUDIT PREPARATION:
□ Review previous audit findings and CAPA status
□ Review quality metrics trends
□ Prepare audit schedule and agenda
□ Request advance documentation

SECTION 1: QUALITY MANAGEMENT SYSTEM (20 points)
□ Quality manual current and approved
□ Quality objectives documented and measured
□ Management review conducted (frequency per SOP)
□ Internal audit program active
□ CAPA system functional with effectiveness checks
□ Document control system (version control, approval, distribution)
□ Change control process for all changes

SECTION 2: PERSONNEL (15 points)
□ Organizational chart current
□ Job descriptions for all key positions
□ Training records complete and current
□ GMP training documented
□ Hygiene procedures followed
□ Health monitoring (where required)

SECTION 3: PREMISES & EQUIPMENT (20 points)
□ Facility maintenance records
□ Equipment qualification records (IQ/OQ/PQ)
□ Calibration records current
□ Cleaning validation/verification records
□ Environmental monitoring results (trending)
□ Pest control records

SECTION 4: PRODUCTION (25 points)
□ Batch records complete and accurate
□ In-process controls performed and documented
□ Deviation handling process
□ Line clearance procedures followed
□ Labeling controls
□ Reconciliation performed

SECTION 5: QUALITY CONTROL (20 points)
□ Specifications current and approved
□ Test methods validated
□ OOS/OOT investigation process
□ Retain samples program
□ Stability program ongoing
□ Reference standards managed

AUDIT FINDINGS CLASSIFICATION:
- Critical: Direct patient safety risk → 48-hour response
- Major: QMS breakdown → 30-day CAPA
- Minor: Improvement needed → 60-day CAPA
- Observation: Best practice suggestion

CAPA TEMPLATE:
1. Problem Description (what, when, where, extent)
2. Immediate Containment Actions
3. Root Cause Analysis (5-Why, Fishbone, etc.)
4. Corrective Actions
5. Preventive Actions (systemic)
6. Implementation Timeline
7. Effectiveness Verification Method
8. Sign-off and Close-out
""",
    },
    {
        "agency": "AEMPS",
        "category": "Medical Device",
        "title": "Requisitos para Productos Sanitarios en España (AEMPS)",
        "content": """
AEMPS (España) — Requisitos para Productos Sanitarios:

CLASIFICACIÓN (Reglamento UE 2017/745):
- Clase I: Bajo riesgo
- Clase IIa: Riesgo moderado
- Clase IIb: Riesgo potencial
- Clase III: Alto riesgo

PROCEDIMIENTOS CLAVE:
1. Declaración de Conformidad CE
2. Evaluación por Organismo Notificado (salvo Clase I)
3. Marcado CE obligatorio
4. Registro en la base de datos EUDAMED
5. Comunicación de comercialización a la AEMPS

REQUISITOS DEL SISTEMA DE CALIDAD:
- ISO 13485:2016 es el estándar de referencia
- Gestión de riesgos (ISO 14971)
- Vigilancia post-comercialización
- Designación de Persona Responsable del cumplimiento normativo (PRRC)
""",
    },
    {
        "agency": "COFEPRIS",
        "category": "Pharmaceutical",
        "title": "Buenas Prácticas de Fabricación en México (NOM-059-SSA1)",
        "content": """
COFEPRIS (México) — NOM-059-SSA1-2015 Buenas Prácticas de Fabricación:

OBJETIVO: Establecer los requisitos mínimos necesarios para el proceso de fabricación de los medicamentos para uso humano comercializados en el país.

SISTEMA DE GESTIÓN DE CALIDAD:
- Gestión de riesgos de calidad
- Manual de Calidad
- Auditorías internas 및 a proveedores
- CAPA (Acciones Correctivas 및 Preventivas)

PERSONAL:
- Organigrama actualizado
- Responsable Sanitario con perfil profesional
- Capacitación continua documentada

INSTALACIONES Y EQUIPOS:
- Calificación 및 validación (IQ/OQ/PQ)
- Mantenimiento preventivo
- Control de áreas limpias (Clasificación ISO)
""",
    },
]


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def get_embedding(text: str) -> Optional[list]:
    """Get embedding from Ollama."""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()["embedding"]
    except Exception as e:
        print(f"  Embedding error: {e}")
        return None


def ensure_collection():
    """Create Qdrant collection if it doesn't exist."""
    try:
        # Check if collection exists
        r = requests.get(f"{QDRANT_URL}/collections/{COLLECTION}")
        if r.status_code == 200:
            print(f"  Collection '{COLLECTION}' already exists.")
            return True
    except:
        pass

    # Get embedding dimension from a test embedding
    print("  Creating Qdrant collection...")
    test_embed = get_embedding("test")
    if not test_embed:
        print("  ERROR: Cannot connect to Ollama for embeddings.")
        return False

    dim = len(test_embed)
    payload = {
        "vectors": {
            "size": dim,
            "distance": "Cosine"
        }
    }
    r = requests.put(f"{QDRANT_URL}/collections/{COLLECTION}", json=payload)
    if r.status_code in (200, 201):
        print(f"  Collection created (dim={dim}).")
        return True
    else:
        print(f"  ERROR creating collection: {r.text}")
        return False


def ingest_document(doc: dict, doc_id_start: int) -> int:
    """Ingest a document into Qdrant. Returns number of chunks added."""
    content = doc.get("content", "")
    if not content:
        return 0

    chunks = chunk_text(content)
    points = []

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        if not embedding:
            continue

        doc_id = int(hashlib.md5(f"{doc['title']}-{i}".encode()).hexdigest()[:8], 16)
        points.append({
            "id": doc_id,
            "vector": embedding,
            "payload": {
                "agency":    doc.get("agency", ""),
                "category":  doc.get("category", ""),
                "title":     doc.get("title", ""),
                "chunk":     chunk,
                "chunk_idx": i,
                "source":    doc.get("url", "inline"),
                "type":      doc.get("type", "knowledge"),
            }
        })
        time.sleep(0.05)

    if points:
        r = requests.put(
            f"{QDRANT_URL}/collections/{COLLECTION}/points",
            json={"points": points}
        )
        if r.status_code in (200, 201):
            return len(points)
        else:
            print(f"  ERROR inserting points: {r.text}")

    return 0


def main():
    print("\n" + "="*52)
    print(" GlobalRegAI — Regulatory Knowledge Base Setup")
    print("="*52)

    # Check Ollama
    print("\n[1/3] Checking Ollama connection...")
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        if EMBED_MODEL not in models and not any(EMBED_MODEL in m for m in models):
            print(f"  Pulling embedding model: {EMBED_MODEL}...")
            requests.post(
                f"{OLLAMA_URL}/api/pull",
                json={"name": EMBED_MODEL, "stream": False},
                timeout=300
            )
        print(f"  Ollama ready. Models: {models[:3]}...")
    except Exception as e:
        print(f"  ERROR: Cannot connect to Ollama at {OLLAMA_URL}")
        print(f"  Make sure GlobalRegAI services are running.")
        sys.exit(1)

    # Check Qdrant
    print("\n[2/3] Setting up Qdrant vector database...")
    try:
        requests.get(f"{QDRANT_URL}/healthz", timeout=5)
    except:
        print(f"  ERROR: Cannot connect to Qdrant at {QDRANT_URL}")
        sys.exit(1)

    if not ensure_collection():
        sys.exit(1)

    # Ingest inline knowledge
    print("\n[3/3] Loading regulatory knowledge base...")
    total_chunks = 0

    for doc in tqdm(INLINE_KNOWLEDGE, desc="  Ingesting documents"):
        n = ingest_document(doc, total_chunks)
        total_chunks += n
        tqdm.write(f"  ✓ [{doc['agency']}] {doc['title'][:50]} ({n} chunks)")

    print(f"\n  Total chunks loaded: {total_chunks}")
    print("\n" + "="*52)
    print(" Knowledge base ready!")
    print(" GlobalRegAI can now answer questions about:")
    print("  - FDA medical device & drug regulations")
    print("  - EU GMP guidelines (EMA)")
    print("  - Korea MFDS requirements")
    print("  - ISO 13485, 14971, 9001")
    print("  - GMP audit checklists")
    print("="*52 + "\n")


if __name__ == "__main__":
    main()
