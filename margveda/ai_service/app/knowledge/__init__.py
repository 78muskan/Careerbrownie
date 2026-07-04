"""Knowledge base aggregator — all domain records in one place.

Returns unified list of dicts that the RAG pipeline converts to LlamaIndex Documents.

Each record shape::
    {
        "id":       str,   # e.g. "career::software_engineer"
        "text":     str,   # full text for embedding
        "domain":   str,   # career|college|exam|scholarship|salary|skills|timeline|faq|counsellor
        "title":    str,   # display title
        "metadata": dict,  # stored in Qdrant payload alongside the vector
    }
"""
from __future__ import annotations

from app.knowledge.colleges_data import get_college_documents
from app.knowledge.counsellor_data import get_counsellor_documents
from app.knowledge.exams_data import get_exam_documents
from app.knowledge.govt_jobs_data import get_govt_job_documents
from app.knowledge.salaries_data import get_salary_documents
from app.knowledge.scholarships_data import get_scholarship_documents
from app.knowledge.skills_data import get_skills_documents
from app.knowledge.timelines_data import get_timeline_documents
from app.document_loader import load_career_documents, load_faq_documents


def get_all_documents() -> list[dict]:
    """Return every knowledge record across all domains as a flat list of dicts."""
    records: list[dict] = []

    for doc in load_career_documents():
        records.append({"id": doc.id, "text": doc.text, "domain": doc.domain,
                        "title": doc.title, "metadata": doc.metadata})

    for doc in load_faq_documents():
        records.append({"id": doc.id, "text": doc.text, "domain": doc.domain,
                        "title": doc.title, "metadata": doc.metadata})

    records.extend(get_college_documents())
    records.extend(get_exam_documents())
    records.extend(get_scholarship_documents())
    records.extend(get_salary_documents())
    records.extend(get_skills_documents())
    records.extend(get_timeline_documents())
    records.extend(get_counsellor_documents())
    records.extend(get_govt_job_documents())

    return records


def get_domain_stats() -> dict[str, int]:
    from collections import Counter
    return dict(sorted(Counter(r["domain"] for r in get_all_documents()).items()))
