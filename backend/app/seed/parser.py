import re
from dataclasses import dataclass, field

SOURCE_ID_RE = re.compile(r"(SIH\d{5}|TCOE PS\d{2}|KAG\d{2})")
ENTRY_RE = re.compile(
    r"^(?P<title>.+?)\s*\((?P<paren>[^)]*)\)\."
    r"\s*(?P<src>SIH\d{5}|TCOE PS\d{2}|KAG\d{2})(?:,\s*(?P<org>[^.]+?))?\.\s*(?P<body>.+)$"
)
DATASETS_RE = re.compile(r"datasets?\s*\(([^)]+)\)", re.IGNORECASE)
SENTENCE_SPLIT_RE = re.compile(r"(?<=\.)\s+")

SOURCE_NAME_BY_PREFIX = {"SIH": "Smart India Hackathon 2026", "TCOE PS": "TCOE", "KAG": "Kaggle"}
DEFAULT_EST_HOURS = 40

FIELD_KEYWORDS = [
    ("blockchain", "blockchain"),
    ("distributed systems", "distributed-systems"),
    ("cybersecurity", "cybersecurity"),
    ("cryptography", "cybersecurity"),
    ("computer vision", "computer-vision"),
    ("llm", "nlp-llm"),
    ("document ai", "nlp-llm"),
    ("nlp", "nlp-llm"),
    ("ocr", "computer-vision"),
    ("geospatial", "geospatial"),
    ("optimization", "optimization"),
    ("data engineering", "data-engineering"),
    ("full-stack", "web-fullstack"),
    ("full stack", "web-fullstack"),
    ("web app", "web-fullstack"),
    ("web", "web-fullstack"),
    ("mobile", "mobile"),
    ("iot", "iot-embedded"),
    ("ml", "ml"),
    ("machine learning", "ml"),
]

DOMAIN_KEYWORDS = [
    ("disaster", "disaster-management"),
    ("healthtech", "healthcare"),
    ("healthcare", "healthcare"),
    ("industry 4.0", "industry"),
    ("mining", "industry"),
    ("agri", "agriculture"),
    ("agriculture", "agriculture"),
    ("governance", "governance"),
    ("transport", "transport"),
    ("logistics", "transport"),
    ("climate", "climate"),
    ("education", "education"),
    ("fintech", "fintech"),
    ("payments", "fintech"),
]

TECH_TAG_ALIASES = {
    "ml": "ml",
    "time series": "time-series",
    "explainable ai": "explainable-ai",
    "computer vision": "computer-vision",
    "document ai": "document-ai",
    "rules engine": "rules-engine",
    "data engineering": "data-engineering",
    "full-stack": "fullstack",
    "full stack": "fullstack",
    "real-time": "real-time",
    "distributed systems": "distributed-systems",
    "machine learning": "ml",
    "optimization": "optimization",
    "geospatial": "geospatial",
    "cryptography": "cryptography",
    "blockchain": "blockchain",
    "iot": "iot",
    "mobile": "mobile",
    "ocr": "ocr",
    "nlp": "nlp",
    "llm": "llm",
    "web app": "web",
    "web": "web",
    "tabular": "tabular",
    "routing": "routing",
    "ux": "ux",
}


@dataclass
class ParsedEntry:
    title: str
    tech_paren: str
    source_id: str
    organisation: str
    body: str
    original_text: str
    source_name: str
    tech_part: str
    sector_part: str | None
    ai_fields: list[str] = field(default_factory=list)
    tech_tags: list[str] = field(default_factory=list)
    datasets: list[dict] = field(default_factory=list)
    field: str = "other"
    domain: str = "other"
    difficulty: str = "intermediate"
    est_hours: int = DEFAULT_EST_HOURS


def _is_group_header(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if re.match(r"^projects \d+$", stripped, re.IGNORECASE):
        return True
    if "(" in stripped or SOURCE_ID_RE.search(stripped):
        return False
    return True


def _hits(keyword: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE) is not None


def parse_blocks(text: str) -> list[ParsedEntry]:
    """One entry per line in the source file; group headers and blanks are skipped."""
    entries = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or _is_group_header(stripped):
            continue
        match = ENTRY_RE.match(stripped)
        if match:
            entries.append(_build_entry(match, stripped))
    return entries


def source_name_for(source_id: str) -> str:
    for prefix, name in SOURCE_NAME_BY_PREFIX.items():
        if source_id.startswith(prefix):
            return name
    return "other"


def _build_entry(match: re.Match, original: str) -> ParsedEntry:
    title = match.group("title").strip()
    paren = match.group("paren")
    source_id = match.group("src")
    org = (match.group("org") or "").strip()
    body = match.group("body").strip()

    if "·" in paren:
        tech_part, sector_part = paren.split("·", 1)
        tech_part, sector_part = tech_part.strip(), sector_part.strip()
    else:
        tech_part, sector_part = paren.strip(), None

    ai_fields: list[str] = []
    tech_tags = []
    tech_lower = tech_part.lower()
    for keyword, tag in TECH_TAG_ALIASES.items():
        if _hits(keyword, tech_lower):
            tech_tags.append(tag)
    tech_tags = sorted(set(tech_tags))

    entry_field = "other"
    tech_lower_no_punct = re.sub(r"[+/,]", " ", tech_lower)
    for keyword, value in FIELD_KEYWORDS:
        if _hits(keyword, tech_lower) or _hits(keyword, tech_lower_no_punct):
            entry_field = value
            break
    ai_fields.extend(["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"])

    entry_domain = "other"
    if sector_part:
        sector_lower = sector_part.lower()
        for keyword, value in DOMAIN_KEYWORDS:
            if _hits(keyword, sector_lower):
                entry_domain = value
                break

    difficulty = "beginner" if "small scope" in body.lower() else "intermediate"

    datasets = []
    ds_match = DATASETS_RE.search(body)
    if ds_match:
        names = [n.strip().rstrip(".").strip() for n in ds_match.group(1).split(",")]
        datasets = [{"name": n, "url": None} for n in names if n]
    if not datasets:
        ai_fields.append("datasets")

    first_sentence = SENTENCE_SPLIT_RE.split(body, maxsplit=1)[0].strip()

    return ParsedEntry(
        title=title,
        tech_paren=paren,
        source_id=source_id,
        organisation=org,
        body=body,
        original_text=original,
        source_name=source_name_for(source_id),
        tech_part=tech_part,
        sector_part=sector_part,
        ai_fields=ai_fields,
        tech_tags=tech_tags,
        datasets=datasets,
        field=entry_field,
        domain=entry_domain,
        difficulty=difficulty,
        est_hours=DEFAULT_EST_HOURS,
    )
