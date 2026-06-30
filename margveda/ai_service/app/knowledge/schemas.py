from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class CareerKnowledge(BaseModel):
    title: str
    domain: str
    description: str
    avg_salary_india: str
    global_salary: Optional[str] = None
    growth_rate: str
    demand: str  # High | Medium | Low
    required_skills: list[str] = Field(default_factory=list)
    key_entrance_exams: list[str] = Field(default_factory=list)
    top_colleges: list[str] = Field(default_factory=list)
    job_roles: list[str] = Field(default_factory=list)
    career_progression: list[str] = Field(default_factory=list)
    work_type: Optional[str] = None  # Office | Remote | Field | Mixed
    state_specific_notes: Optional[str] = None
    source: str = ""
    last_updated: Optional[str] = None


class CollegeKnowledge(BaseModel):
    name: str
    location: str
    state: str
    type: str  # Central/State/Deemed/Private
    tier: str  # Tier-1/2/3
    programs: list[str] = Field(default_factory=list)
    entrance_exams: list[str] = Field(default_factory=list)
    cutoff_general: Optional[str] = None
    cutoff_obc: Optional[str] = None
    cutoff_sc_st: Optional[str] = None
    fees_range: Optional[str] = None
    placement_avg_lpa: Optional[float] = None
    placement_highest_lpa: Optional[float] = None
    top_recruiters: list[str] = Field(default_factory=list)
    hostel_available: bool = True
    naac_grade: Optional[str] = None
    nirf_rank: Optional[int] = None
    website: Optional[str] = None
    source: str = ""


class ScholarshipKnowledge(BaseModel):
    name: str
    provider: str
    type: str  # Merit/Need/Category/Sports/Research
    amount: str
    eligibility_category: list[str] = Field(default_factory=list)  # SC/ST/OBC/EWS/All
    min_marks_percent: Optional[float] = None
    max_family_income: Optional[float] = None
    applicable_states: list[str] = Field(default_factory=list)  # empty = all India
    applicable_streams: list[str] = Field(default_factory=list)
    application_deadline: Optional[str] = None
    documents_required: list[str] = Field(default_factory=list)
    application_url: Optional[str] = None
    renewable: bool = True
    source: str = ""


class ExamKnowledge(BaseModel):
    name: str
    full_name: str
    conducting_body: str
    applicable_for: list[str] = Field(default_factory=list)
    frequency: str  # Annual/Biannual/Monthly
    mode: str  # Online/Offline/Both
    syllabus_topics: list[str] = Field(default_factory=list)
    eligibility: str
    application_month: Optional[str] = None
    exam_month: Optional[str] = None
    result_month: Optional[str] = None
    total_seats: Optional[int] = None
    cutoff_previous: Optional[str] = None
    official_website: Optional[str] = None
    preparation_time_months: Optional[int] = None
    source: str = ""


class FAQKnowledge(BaseModel):
    question: str
    answer: str
    domain: str  # career/college/scholarship/exam/general
    tags: list[str] = Field(default_factory=list)
    upvotes: int = 0
    source: str = ""


class StudentProfile(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    class_grade: Optional[str] = None  # 10/11/12/UG1/UG2/PG
    stream: Optional[str] = None  # Science/Commerce/Arts/PCM/PCB
    board: Optional[str] = None  # CBSE/ICSE/State
    marks_percent: Optional[float] = None
    jee_rank: Optional[int] = None
    neet_score: Optional[int] = None
    category: str = "General"  # General/OBC/SC/ST/EWS
    interests: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    preferred_states: list[str] = Field(default_factory=list)
    preferred_cities: list[str] = Field(default_factory=list)
    budget_annual: Optional[float] = None
    family_income_annual: Optional[float] = None
    target_career: Optional[str] = None
    target_exams: list[str] = Field(default_factory=list)
    psychometric_results: dict = Field(default_factory=dict)
