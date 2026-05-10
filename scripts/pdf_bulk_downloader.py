#!/usr/bin/env python3
"""
GlobalRegAI — 규정 PDF 대량 다운로드 & 텍스트 추출
FDA / EMA / ICH / PIC/S / WHO / IMDRF 공식 문서
"""

import os
import time
import json
from pathlib import Path
import requests

PDF_DIR = Path("rag/regulatory-docs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "GlobalRegAI/1.0 (Educational Use)"}

# ══════════════════════════════════════════════════════════════
# 전체 무료 PDF 목록 (공식 기관 공개 문서)
# ══════════════════════════════════════════════════════════════
PDF_CATALOG = [

    # ── FDA 의료기기 가이던스 ────────────────────────────────
    {
        "title": "FDA Design Controls Guidance for Medical Devices",
        "agency": "FDA", "category": "Medical Device", "language": "en",
        "url": "https://www.fda.gov/media/116573/download",
        "filename": "FDA_Design_Controls_Guidance.pdf"
    },
    {
        "title": "FDA Guidance: Applying Human Factors and Usability Engineering",
        "agency": "FDA", "category": "Medical Device", "language": "en",
        "url": "https://www.fda.gov/media/80974/download",
        "filename": "FDA_Human_Factors_Guidance.pdf"
    },
    {
        "title": "FDA General Principles of Software Validation",
        "agency": "FDA", "category": "Medical Device Software", "language": "en",
        "url": "https://www.fda.gov/media/73141/download",
        "filename": "FDA_Software_Validation.pdf"
    },
    {
        "title": "FDA Content of 510(k) Submissions",
        "agency": "FDA", "category": "Medical Device 510k", "language": "en",
        "url": "https://www.fda.gov/media/71984/download",
        "filename": "FDA_510k_Content_Guidance.pdf"
    },
    {
        "title": "FDA De Novo Classification Process Guidance",
        "agency": "FDA", "category": "Medical Device", "language": "en",
        "url": "https://www.fda.gov/media/87987/download",
        "filename": "FDA_DeNovo_Guidance.pdf"
    },
    {
        "title": "FDA Cybersecurity Medical Devices Guidance 2023",
        "agency": "FDA", "category": "Medical Device Cybersecurity", "language": "en",
        "url": "https://www.fda.gov/media/119933/download",
        "filename": "FDA_Cybersecurity_Guidance_2023.pdf"
    },

    # ── FDA 의약품 가이던스 ──────────────────────────────────
    {
        "title": "FDA Q7A GMP Guidance for Active Pharmaceutical Ingredients",
        "agency": "FDA", "category": "Pharmaceutical GMP", "language": "en",
        "url": "https://www.fda.gov/media/71518/download",
        "filename": "FDA_Q7A_GMP_API.pdf"
    },
    {
        "title": "FDA Process Validation General Principles",
        "agency": "FDA", "category": "Pharmaceutical Validation", "language": "en",
        "url": "https://www.fda.gov/media/71021/download",
        "filename": "FDA_Process_Validation.pdf"
    },
    {
        "title": "FDA Data Integrity and cGMP Compliance Guidance",
        "agency": "FDA", "category": "Pharmaceutical Data Integrity", "language": "en",
        "url": "https://www.fda.gov/media/119397/download",
        "filename": "FDA_Data_Integrity_cGMP.pdf"
    },
    {
        "title": "FDA Investigating OOS Test Results Guidance",
        "agency": "FDA", "category": "Pharmaceutical QC", "language": "en",
        "url": "https://www.fda.gov/media/72001/download",
        "filename": "FDA_OOS_Investigation_Guidance.pdf"
    },
    {
        "title": "FDA Pharmaceutical cGMP for 21st Century",
        "agency": "FDA", "category": "Pharmaceutical GMP", "language": "en",
        "url": "https://www.fda.gov/media/71012/download",
        "filename": "FDA_cGMP_21st_Century.pdf"
    },
    {
        "title": "FDA Bioanalytical Method Validation Guidance",
        "agency": "FDA", "category": "Pharmaceutical Validation", "language": "en",
        "url": "https://www.fda.gov/media/70858/download",
        "filename": "FDA_Bioanalytical_Method_Validation.pdf"
    },
    {
        "title": "FDA Guidance: ANDA Submissions - Content and Format",
        "agency": "FDA", "category": "Pharmaceutical ANDA", "language": "en",
        "url": "https://www.fda.gov/media/70943/download",
        "filename": "FDA_ANDA_Content_Format.pdf"
    },

    # ── FDA 식품 가이던스 ────────────────────────────────────
    {
        "title": "FDA FSMA Preventive Controls for Human Food",
        "agency": "FDA", "category": "Food Safety", "language": "en",
        "url": "https://www.fda.gov/media/99572/download",
        "filename": "FDA_FSMA_Preventive_Controls.pdf"
    },
    {
        "title": "FDA Hazard Analysis and Risk-Based Preventive Controls (HARPC)",
        "agency": "FDA", "category": "Food Safety HARPC", "language": "en",
        "url": "https://www.fda.gov/media/99569/download",
        "filename": "FDA_HARPC_Guidance.pdf"
    },

    # ── ICH 가이드라인 ───────────────────────────────────────
    {
        "title": "ICH Q7 GMP for Active Pharmaceutical Ingredients",
        "agency": "ICH", "category": "Pharmaceutical GMP", "language": "en",
        "url": "https://database.ich.org/sites/default/files/Q7%20Guideline.pdf",
        "filename": "ICH_Q7_GMP_API.pdf"
    },
    {
        "title": "ICH Q8(R2) Pharmaceutical Development",
        "agency": "ICH", "category": "Pharmaceutical Development", "language": "en",
        "url": "https://database.ich.org/sites/default/files/Q8%28R2%29%20Guideline.pdf",
        "filename": "ICH_Q8R2_Pharmaceutical_Development.pdf"
    },
    {
        "title": "ICH Q9(R1) Quality Risk Management",
        "agency": "ICH", "category": "Quality Risk Management", "language": "en",
        "url": "https://database.ich.org/sites/default/files/Q9-R1-Step4-Guideline_2023_0126.pdf",
        "filename": "ICH_Q9R1_Quality_Risk_Management.pdf"
    },
    {
        "title": "ICH Q10 Pharmaceutical Quality System",
        "agency": "ICH", "category": "Quality System", "language": "en",
        "url": "https://database.ich.org/sites/default/files/Q10%20Guideline.pdf",
        "filename": "ICH_Q10_PQS.pdf"
    },
    {
        "title": "ICH Q11 Development and Manufacture of Drug Substances",
        "agency": "ICH", "category": "Drug Substance", "language": "en",
        "url": "https://database.ich.org/sites/default/files/Q11%20Guideline.pdf",
        "filename": "ICH_Q11_Drug_Substances.pdf"
    },
    {
        "title": "ICH Q12 Pharmaceutical Product Lifecycle Management",
        "agency": "ICH", "category": "Lifecycle Management", "language": "en",
        "url": "https://database.ich.org/sites/default/files/Q12_Guideline_Step4_2019_1119.pdf",
        "filename": "ICH_Q12_Lifecycle.pdf"
    },
    {
        "title": "ICH E6(R3) Good Clinical Practice",
        "agency": "ICH", "category": "Clinical", "language": "en",
        "url": "https://database.ich.org/sites/default/files/ICH_E6(R3)_GuideLine_Step4_2024_0519.pdf",
        "filename": "ICH_E6R3_GCP.pdf"
    },

    # ── EU/EMA GMP 가이드라인 ────────────────────────────────
    {
        "title": "EU GMP Guidelines Annex 1 - Manufacture of Sterile Medicinal Products (2022)",
        "agency": "EMA/EC", "category": "Pharmaceutical GMP Annex 1", "language": "en",
        "url": "https://health.ec.europa.eu/system/files/2022-09/2022_gmp-guidelines_annex1_en_0.pdf",
        "filename": "EU_GMP_Annex1_Sterile_2022.pdf"
    },
    {
        "title": "EU GMP Annex 11 - Computerised Systems",
        "agency": "EMA/EC", "category": "Pharmaceutical GMP Computerised", "language": "en",
        "url": "https://health.ec.europa.eu/system/files/2022-09/vol4_an11_en_0.pdf",
        "filename": "EU_GMP_Annex11_Computerised.pdf"
    },

    # ── IMDRF 가이드라인 ─────────────────────────────────────
    {
        "title": "IMDRF UDI Guidance - Unique Device Identification",
        "agency": "IMDRF", "category": "Medical Device UDI", "language": "en",
        "url": "https://www.imdrf.org/sites/default/files/docs/imdrf/final/technical/imdrf-tech-190321-udi-systguid-n48.pdf",
        "filename": "IMDRF_UDI_Guidance.pdf"
    },
    {
        "title": "IMDRF Software as Medical Device (SaMD) Framework",
        "agency": "IMDRF", "category": "Medical Device Software", "language": "en",
        "url": "https://www.imdrf.org/sites/default/files/docs/imdrf/final/technical/imdrf-tech-140918-samd-framework-classification_0.pdf",
        "filename": "IMDRF_SaMD_Framework.pdf"
    },

    # ── WHO GMP 가이드라인 ───────────────────────────────────
    {
        "title": "WHO GMP for Pharmaceutical Products (TRS 986 Annex 2)",
        "agency": "WHO", "category": "Pharmaceutical GMP", "language": "en",
        "url": "https://www.who.int/docs/default-source/medicines/norms-and-standards/guidelines/production/trs986-annex2-gmp-pharmaceuticals.pdf",
        "filename": "WHO_GMP_Pharmaceuticals_TRS986.pdf"
    },
    {
        "title": "WHO GMP Medical Devices",
        "agency": "WHO", "category": "Medical Device GMP", "language": "en",
        "url": "https://iris.who.int/bitstream/handle/10665/44697/9789241501736_eng.pdf",
        "filename": "WHO_GMP_Medical_Devices.pdf"
    },
]


def download_all_pdfs():
    """모든 PDF 다운로드"""
    print(f"\n{'='*60}")
    print(" GlobalRegAI — PDF Bulk Downloader")
    print(f" {len(PDF_CATALOG)} documents to download")
    print(f" Save location: {PDF_DIR.absolute()}")
    print("="*60)

    results = {"success": [], "failed": [], "skipped": []}

    for i, doc in enumerate(PDF_CATALOG, 1):
        path = PDF_DIR / doc["filename"]
        print(f"\n[{i}/{len(PDF_CATALOG)}] {doc['title'][:60]}")

        if path.exists():
            size = path.stat().st_size
            if size > 10000:
                print(f"  SKIP (already exists, {size/1024:.0f} KB)")
                results["skipped"].append(doc["filename"])
                continue

        try:
            r = requests.get(doc["url"], headers=HEADERS, timeout=60, stream=True)
            r.raise_for_status()
            with open(path, "wb") as f:
                size = 0
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    size += len(chunk)
            print(f"  ✓ Downloaded ({size/1024:.0f} KB)")
            results["success"].append(doc["filename"])
            doc["local_path"] = str(path)
            doc["size_bytes"] = size
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            results["failed"].append({"file": doc["filename"], "error": str(e)})

        time.sleep(1)  # 서버 부하 방지

    # 결과 저장
    with open(PDF_DIR / "download_catalog.json", "w", encoding="utf-8") as f:
        json.dump({
            "catalog": PDF_CATALOG,
            "results": results,
            "total": len(PDF_CATALOG),
            "success": len(results["success"]),
            "failed": len(results["failed"]),
            "skipped": len(results["skipped"]),
        }, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f" DOWNLOAD COMPLETE")
    print(f" ✓ Success: {len(results['success'])}")
    print(f" → Skipped: {len(results['skipped'])}")
    print(f" ✗ Failed:  {len(results['failed'])}")
    print(f" Saved: {PDF_DIR.absolute()}")
    print("="*60)
    return results


def ingest_pdfs_to_qdrant():
    """다운로드된 PDF를 Qdrant에 수집"""
    try:
        import pdfplumber
        from data_crawler import ingest_text, setup_qdrant
    except ImportError:
        print("Install: pip install pdfplumber")
        return

    setup_qdrant()
    catalog_file = PDF_DIR / "download_catalog.json"
    if not catalog_file.exists():
        print("Run download_all_pdfs() first")
        return

    with open(catalog_file) as f:
        catalog = json.load(f)

    total = 0
    for doc in catalog.get("catalog", []):
        path = PDF_DIR / doc["filename"]
        if not path.exists():
            continue
        print(f"  Ingesting: {doc['title'][:60]}...")
        try:
            with pdfplumber.open(path) as pdf:
                text = "\n".join(
                    p.extract_text() or ""
                    for p in pdf.pages[:80]
                )
            if len(text) > 200:
                n = ingest_text(text, {
                    "agency": doc["agency"],
                    "category": doc["category"],
                    "title": doc["title"],
                    "source": doc["url"],
                    "type": "official_guidance",
                    "language": doc["language"],
                    "filename": doc["filename"]
                })
                total += n
                print(f"    ✓ {n} chunks")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        time.sleep(0.5)

    print(f"\nTotal PDF chunks ingested: {total}")


if __name__ == "__main__":
    import sys
    if "--ingest" in sys.argv:
        ingest_pdfs_to_qdrant()
    else:
        download_all_pdfs()
