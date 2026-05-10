import os
import json
import time
from typing import List, Dict

# Mocking Supabase Client & Embeddings for demonstration of the architecture
class SupabaseMock:
    def table(self, name): return self
    def insert(self, data):
        print(f"✅ Inserted {len(data)} documents into Supabase pgvector.")
        return self
    def execute(self): pass

supabase = SupabaseMock()

# The 17+ Global Regulatory Agencies specified by the user
AGENCIES = [
    {"country": "미국", "agency": "FDA", "category": "All", "url": "https://www.fda.gov/regulatory-information"},
    {"country": "한국", "agency": "MFDS", "category": "All", "url": "https://www.mfds.go.kr/eng"},
    {"country": "중국", "agency": "NMPA", "category": "Pharma, Medical Device, Cosmetics", "url": "http://english.nmpa.gov.cn/index.html"},
    {"country": "일본", "agency": "PMDA", "category": "Pharma, Medical Device", "url": "https://www.pmda.go.jp/english/"},
    {"country": "유럽연합", "agency": "EMA", "category": "Pharma", "url": "https://www.ema.europa.eu/en/documents"},
    {"country": "영국", "agency": "MHRA", "category": "Pharma, Medical Device", "url": "https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency"},
    {"country": "캐나다", "agency": "Health Canada", "category": "All", "url": "https://www.canada.ca/en/health-canada/services/drugs-health-products/medical-devices.html"},
    {"country": "호주", "agency": "TGA", "category": "Pharma, Medical Device", "url": "https://www.tga.gov.au/"},
    {"country": "뉴질랜드", "agency": "Medsafe", "category": "Pharma, Medical Device", "url": "https://www.medsafe.govt.nz/"},
    {"country": "대만", "agency": "TFDA", "category": "All", "url": "https://www.fda.gov.tw/ENG/"},
    {"country": "ASEAN (태국)", "agency": "Thai FDA", "category": "Medical Device", "url": "https://en.fda.moph.go.th/"},
    {"country": "독일", "agency": "BfArM", "category": "Medical Device, Pharma", "url": "https://www.bfarm.de/EN/"},
    {"country": "프랑스", "agency": "ANSM", "category": "Medical Device, Pharma", "url": "https://ansm.sante.fr/"},
    {"country": "대한민국", "agency": "NIDS", "category": "Medical Device", "url": "https://www.nids.or.kr/"},
    {"country": "필리핀", "agency": "FDA CDRRHR", "category": "Medical Device", "url": "https://www.fda.gov.ph/?s=cdrrhr"},
    {"country": "인도네시아", "agency": "MOH", "category": "Pharma, Medical Device", "url": "https://sertifikasialkes.kemkes.go.id/"},
    {"country": "싱가포르", "agency": "HSA", "category": "Medical Device", "url": "https://www.hsa.gov.sg/medical-devices/registration/risk-classification-rule"},
    {"country": "베트남", "agency": "DMEC", "category": "Medical Device", "url": "https://dmec.moh.gov.vn/"},
    {"country": "말레이시아", "agency": "MDA", "category": "Medical Device", "url": "https://portal.mda.gov.my/"}
]

def generate_mock_embedding(text: str) -> List[float]:
    # Simulates generating a 1536-dimensional vector using OpenAI text-embedding-ada-002
    return [0.0] * 1536

def scrape_and_ingest_agency(agency_info: Dict):
    print(f"🔍 Crawling {agency_info['agency']} ({agency_info['country']}) at {agency_info['url']}...")
    time.sleep(1) # Simulate network delay
    
    # Mocking parsed regulatory clauses
    parsed_documents = [
        {
            "agency_name": agency_info['agency'],
            "country": agency_info['country'],
            "category": agency_info['category'],
            "content": f"Sample regulatory clause from {agency_info['agency']} regarding product registration and compliance.",
            "source_url": agency_info['url'],
            "embedding": generate_mock_embedding("Sample regulatory clause")
        }
    ]
    
    # Push to Supabase pgvector
    supabase.table('regulatory_documents').insert(parsed_documents).execute()

def main():
    print("🚀 Starting GlobalRegAI RAG Ingestion Pipeline...")
    print(f"📚 Target Agencies: {len(AGENCIES)}")
    
    for agency in AGENCIES:
        scrape_and_ingest_agency(agency)
        
    print("✅ Ingestion Complete. All 17 global agencies have been vectorized and stored in Supabase pgvector.")

if __name__ == "__main__":
    main()
