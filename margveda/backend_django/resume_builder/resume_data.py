"""
ATS keyword banks, resume templates, and industry skill data.
"""

# Industry-specific ATS keywords
ATS_KEYWORDS = {
    "technology": [
        "python", "java", "javascript", "react", "node.js", "sql", "aws", "docker",
        "kubernetes", "git", "agile", "scrum", "rest api", "microservices", "ci/cd",
        "machine learning", "data structures", "algorithms", "system design", "linux",
        "typescript", "next.js", "postgresql", "mongodb", "redis", "elasticsearch",
    ],
    "data_science": [
        "python", "r", "machine learning", "deep learning", "tensorflow", "pytorch",
        "pandas", "numpy", "scikit-learn", "tableau", "power bi", "sql", "spark",
        "hadoop", "statistics", "data visualization", "nlp", "computer vision",
        "regression", "classification", "clustering", "feature engineering",
    ],
    "finance": [
        "financial modelling", "excel", "valuation", "dcf", "merger", "acquisition",
        "financial analysis", "accounting", "tally", "gst", "audit", "taxation",
        "cfa", "ca", "mba finance", "bloomberg", "ifrs", "risk management",
        "portfolio management", "equity research", "credit analysis",
    ],
    "marketing": [
        "digital marketing", "seo", "sem", "google analytics", "social media",
        "content marketing", "email marketing", "crm", "salesforce", "hubspot",
        "brand management", "market research", "consumer insights", "campaign",
        "roi", "a/b testing", "conversion rate", "lead generation", "copywriting",
    ],
    "hr": [
        "talent acquisition", "recruitment", "onboarding", "hris", "payroll",
        "performance management", "employee engagement", "training", "development",
        "labour law", "compensation", "benefits", "org design", "hr analytics",
        "succession planning", "diversity", "inclusion", "workday", "sap hr",
    ],
    "design": [
        "figma", "adobe xd", "sketch", "illustrator", "photoshop", "after effects",
        "user research", "wireframing", "prototyping", "usability testing",
        "ui design", "ux design", "design thinking", "information architecture",
        "typography", "visual design", "interaction design", "design systems",
    ],
    "general": [
        "leadership", "communication", "teamwork", "problem solving", "analytical",
        "project management", "stakeholder management", "presentation", "ms office",
        "time management", "critical thinking", "adaptability", "collaboration",
    ],
}

# Action verbs for strong bullet points
STRONG_ACTION_VERBS = [
    "Achieved", "Accelerated", "Built", "Created", "Delivered", "Designed",
    "Developed", "Drove", "Engineered", "Enhanced", "Executed", "Generated",
    "Implemented", "Improved", "Increased", "Launched", "Led", "Managed",
    "Optimised", "Reduced", "Scaled", "Spearheaded", "Streamlined", "Transformed",
]

WEAK_PHRASES = [
    "responsible for", "worked on", "helped with", "was part of", "assisted in",
    "duties included", "tried to", "participated in", "involved in",
]

# Resume section types with metadata
RESUME_SECTIONS = {
    "personal_info": {"label": "Personal Information", "required": True, "weight": 15},
    "summary": {"label": "Professional Summary", "required": True, "weight": 15},
    "experience": {"label": "Work Experience", "required": False, "weight": 30},
    "education": {"label": "Education", "required": True, "weight": 20},
    "skills": {"label": "Skills", "required": True, "weight": 15},
    "projects": {"label": "Projects", "required": False, "weight": 10},
    "certifications": {"label": "Certifications", "required": False, "weight": 8},
    "achievements": {"label": "Achievements & Awards", "required": False, "weight": 7},
    "languages": {"label": "Languages", "required": False, "weight": 5},
}

RESUME_TEMPLATES = [
    {
        "id": "modern_clean",
        "name": "Modern Clean",
        "description": "Clean two-column layout with blue accents. Best for tech roles.",
        "is_premium": False,
        "preview_color": "#4F46E5",
    },
    {
        "id": "professional",
        "name": "Professional Classic",
        "description": "Traditional single-column format. Preferred by BFSI and consulting firms.",
        "is_premium": False,
        "preview_color": "#1F2937",
    },
    {
        "id": "creative",
        "name": "Creative Bold",
        "description": "Bold header with accent colours. Great for design and marketing roles.",
        "is_premium": True,
        "preview_color": "#7C3AED",
    },
    {
        "id": "minimal",
        "name": "Minimal Elegant",
        "description": "Minimalist design with elegant typography. Ideal for management roles.",
        "is_premium": True,
        "preview_color": "#059669",
    },
]

# Common ATS-unfriendly formatting patterns
ATS_FORMAT_ISSUES = {
    "tables": "Tables can confuse ATS parsers. Use plain text lists instead.",
    "images": "Profile photos and image-based content are ignored by ATS systems.",
    "headers_footers": "Information in headers/footers may not be read by ATS.",
    "columns": "Multi-column layouts can cause ATS misreading. Single column preferred.",
    "special_chars": "Special characters like ✓, ●, ► may not parse correctly.",
}
