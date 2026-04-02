import re
from typing import Dict

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(r'[\+]?[\d\s\-\(\)]{7,15}')
URL_RE = re.compile(r'(?:https?://)?(?:www\.)?[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?')

POSITION_KEYWORDS = [
    'ceo', 'cto', 'cfo', 'coo', 'director', 'manager', 'engineer',
    'developer', 'designer', 'consultant', 'analyst', 'specialist',
    'coordinator', 'president', 'founder', 'partner', 'associate',
    'officer', 'head', 'lead', 'senior', 'junior', 'vp',
    'dyrektor', 'kierownik', 'specjalista', 'prezes', 'inżynier',
    'koordynator', 'konsultant', 'architekt', 'programista',
    'zarządu', 'zarząd', 'wiceprezes', 'członek',
]

COMPANY_SUFFIXES = [
    'sp. z o.o.', 'sp.z o.o.', 's.a.', 'sp.j.', 'sp.k.',
    'ltd', 'llc', 'inc', 'corp', 'gmbh', 'ag',
    'group', 'grupa', 'holdings', 'solutions', 'consulting',
    'technologies', 'services', 'company',
]


def _is_name_line(line: str) -> bool:
    """Check if a line looks like a person's name (2-3 alphabetic capitalized words)."""
    words = line.split()
    if not (2 <= len(words) <= 3):
        return False
    lower = line.lower()
    if not all(w.isalpha() and w[0].isupper() for w in words):
        return False
    if any(suf in lower for suf in COMPANY_SUFFIXES):
        return False
    if any(kw in lower for kw in POSITION_KEYWORDS):
        return False
    return True


def parse_card_text(raw_text: str) -> Dict[str, str]:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    result = {
        'name': '', 'surname': '', 'email': '', 'phone': '',
        'company': '', 'position': '', 'website': '',
    }

    used_lines = set()

    # 1) Email
    for i, line in enumerate(lines):
        m = EMAIL_RE.search(line)
        if m:
            result['email'] = m.group()
            used_lines.add(i)
            break

    # 2) Phone
    for i, line in enumerate(lines):
        if i in used_lines:
            continue
        m = PHONE_RE.search(line)
        if m:
            candidate = re.sub(r'[^\d+]', '', m.group())
            if len(candidate) >= 7:
                result['phone'] = m.group().strip()
                used_lines.add(i)
                break

    # 3) Website
    for i, line in enumerate(lines):
        if i in used_lines:
            continue
        m = URL_RE.search(line)
        if m and '@' not in m.group():
            result['website'] = m.group()
            used_lines.add(i)
            break

    # 4) Name/Surname — first unused line that looks like a person's name
    for i, line in enumerate(lines):
        if i in used_lines:
            continue
        if _is_name_line(line):
            words = line.split()
            result['name'] = words[0]
            result['surname'] = ' '.join(words[1:])
            used_lines.add(i)
            break

    # 5) Position (keyword match)
    for i, line in enumerate(lines):
        if i in used_lines:
            continue
        lower = line.lower()
        if any(kw in lower for kw in POSITION_KEYWORDS):
            result['position'] = line
            used_lines.add(i)
            break

    # 6) Company (suffix match)
    for i, line in enumerate(lines):
        if i in used_lines:
            continue
        lower = line.lower()
        if any(suf in lower for suf in COMPANY_SUFFIXES):
            result['company'] = line
            used_lines.add(i)
            break

    # 7) Fallback company — first remaining unused line
    if not result['company']:
        for i, line in enumerate(lines):
            if i in used_lines:
                continue
            result['company'] = line
            break

    return result
