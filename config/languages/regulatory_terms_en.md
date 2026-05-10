# GlobalRegAI — English Regulatory Terminology
# Agencies: FDA (US) · EMA (EU) · TGA (Australia) · Health Canada · ISO/ICH

---

## PRIMARY REGULATORY AGENCIES

| Agency | Country/Region | Full Name | Website |
|--------|---------------|-----------|---------|
| FDA | USA | Food and Drug Administration | fda.gov |
| EMA | EU | European Medicines Agency | ema.europa.eu |
| CDRH | USA | Center for Devices and Radiological Health (FDA) | fda.gov/medical-devices |
| CDER | USA | Center for Drug Evaluation and Research (FDA) | fda.gov/drugs |
| TGA | Australia | Therapeutic Goods Administration | tga.gov.au |
| Health Canada | Canada | Health Canada — Medical Devices | canada.ca/health-canada |
| MHRA | UK | Medicines and Healthcare products Regulatory Agency | gov.uk/mhra |
| ANVISA | Brazil | Agência Nacional de Vigilância Sanitária | gov.br/anvisa |

---

## MEDICAL DEVICES

### Classification (US FDA)
| Class | Risk | Pathway |
|-------|------|---------|
| Class I | Low | 510(k) exempt or 510(k) |
| Class II | Moderate | 510(k) Premarket Notification |
| Class III | High | PMA (Premarket Approval) |

### Classification (EU MDR 2017/745)
| Class | Risk | Conformity Assessment |
|-------|------|----------------------|
| Class I | Low | Self-declaration |
| Class IIa | Medium-low | Notified Body audit |
| Class IIb | Medium-high | Notified Body full QA |
| Class III | High | Notified Body design dossier |

### Key Terms
| Term | Definition | Regulation |
|------|-----------|-----------|
| 510(k) | Premarket notification — substantial equivalence | 21 CFR Part 807 |
| PMA | Premarket Approval — clinical evidence required | 21 CFR Part 814 |
| De Novo | Novel low-to-moderate risk device pathway | 21 CFR Part 860 |
| Technical File | Design & development documentation | EU MDR Annex II |
| DHF | Design History File | 21 CFR 820.30 |
| DMR | Device Master Record | 21 CFR 820.181 |
| DHR | Device History Record | 21 CFR 820.184 |
| GSPR | General Safety and Performance Requirements | EU MDR Annex I |
| UDI | Unique Device Identification | 21 CFR Part 830 |
| PMS | Post-Market Surveillance | EU MDR Article 83-86 |
| MDR (reporting) | Medical Device Report | 21 CFR Part 803 |
| EUDAMED | European Database on Medical Devices | EU MDR Article 33 |

### Required Documents — FDA 510(k)
1. Device description and intended use
2. Predicate device comparison (substantial equivalence)
3. Performance testing (bench, biocompatibility, software)
4. Labeling (proposed)
5. 510(k) summary or statement
6. Biocompatibility data (ISO 10993)
7. Software documentation (if applicable — IEC 62304)
8. Sterility data (if applicable)

---

## PHARMACEUTICALS / DRUGS

### Submission Types
| Submission | Description | Regulation |
|-----------|-------------|-----------|
| NDA | New Drug Application — new molecule | 21 CFR Part 314 |
| ANDA | Abbreviated NDA — generic drug | 21 CFR Part 314 |
| BLA | Biologics License Application | 21 CFR Part 601 |
| IND | Investigational New Drug Application | 21 CFR Part 312 |
| MAA | Marketing Authorization Application (EU) | EC Regulation 726/2004 |

### GMP / cGMP Key Terms
| Term | Definition |
|------|-----------|
| cGMP | Current Good Manufacturing Practice — 21 CFR Parts 210/211 |
| QMSR | Quality Management System Regulation (2024 FDA update to QSR) |
| Batch Record | Complete documentation of each production batch |
| OOS | Out of Specification — test result outside acceptance criteria |
| OOT | Out of Trend — statistical trend indicating potential issue |
| CAPA | Corrective and Preventive Action |
| Change Control | Documented process for evaluating and implementing changes |
| Validation | Documented evidence that a process consistently produces expected result |
| Qualification | IQ (Installation), OQ (Operational), PQ (Performance) |
| APR/PQR | Annual Product Review / Product Quality Review |
| SOP | Standard Operating Procedure |
| DMF | Drug Master File |
| CTD | Common Technical Document (ICH M4) |

### ICH Guidelines Reference
| Guideline | Topic |
|-----------|-------|
| ICH Q8 | Pharmaceutical Development |
| ICH Q9 | Quality Risk Management |
| ICH Q10 | Pharmaceutical Quality System |
| ICH Q11 | Development and Manufacture of Drug Substances |
| ICH Q12 | Technical and Regulatory Considerations for Pharmaceutical Product Lifecycle |

---

## COSMETICS

### US FDA (MoCRA 2022)
- **Responsible Person** — US entity responsible for product safety
- **Facility Registration** — mandatory for US cosmetic manufacturers
- **Adverse Event Reporting** — serious adverse events must be reported
- **Safety Substantiation** — adequate evidence for product safety

### EU Cosmetics Regulation (EC) 1223/2009
| Term | Definition |
|------|-----------|
| Responsible Person | EU entity ensuring regulatory compliance |
| Product Information File (PIF) | Technical documentation file |
| Safety Assessment | Evaluation by qualified safety assessor |
| CPNP | Cosmetic Products Notification Portal |
| Annex II | List of prohibited substances |
| Annex III | Restricted substances |
| Annex IV | Permitted colorants |
| Annex V | Permitted preservatives |
| Annex VI | Permitted UV filters |

---

## FOOD

### FDA FSMA (Food Safety Modernization Act)
| Rule | Description |
|------|-------------|
| HARPC | Hazard Analysis and Risk-Based Preventive Controls |
| PCQI | Preventive Controls Qualified Individual |
| Sanitary Transportation | Rules for safe food transport |
| Foreign Supplier Verification | FSVP — verification of imported food |
| Produce Safety Rule | Standards for produce growing/harvesting |

### Key Food Safety Terms
- **HACCP** — Hazard Analysis and Critical Control Points
- **CCP** — Critical Control Point
- **Critical Limit** — boundary that distinguishes safe from unsafe
- **Corrective Action** — action when CCP not met
- **Verification** — confirmation that HACCP system is effective

---

## GMP AUDIT TERMINOLOGY

### Audit Types
| Type | Description | Frequency |
|------|-------------|-----------|
| Internal Audit | Self-inspection of own QMS | Minimum annually |
| Supplier Audit | Assessment of suppliers/CMOs | Risk-based |
| Regulatory Inspection | FDA/EMA/TGA inspection | As scheduled |
| Certification Audit | ISO 13485 / GMP certification | Per certification body |

### Finding Classifications
| Classification | Definition | Response Timeline |
|---------------|-----------|------------------|
| **Critical** | Direct patient safety risk or fraud | 48 hours |
| **Major** | Significant QMS breakdown | 30 calendar days |
| **Minor** | Improvement needed, low risk | 60 calendar days |
| **Observation** | Best practice suggestion | 90 calendar days |

### CAPA Structure (FDA Expectation)
```
1. Problem Description
   - What: specific nonconformance description
   - When: date discovered/occurred
   - Where: specific area/process
   - Extent: how widespread

2. Immediate Containment
   - Actions taken immediately
   - Product disposition if needed

3. Root Cause Analysis
   - Method used (5-Why, Fishbone, FTA)
   - True root cause identified

4. Corrective Actions
   - Actions to fix the root cause
   - Responsible person + due date

5. Preventive Actions
   - Systemic changes to prevent recurrence
   - Training, procedure updates, design changes

6. Effectiveness Check
   - How will you verify the CAPA worked?
   - Metrics and timeline

7. Management Sign-off
```
