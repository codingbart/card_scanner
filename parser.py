import re
from typing import Dict

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(r'(?:\+\d[\d\s\-]{8,14}|\b\d{3}[\s\-]?\d{3}[\s\-]?\d{3}\b|\b\d{2}[\s\-]\d{3}[\s\-]\d{2}[\s\-]\d{2}\b)')
URL_RE = re.compile(r'(?:https?://)?(?:www\.)?[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?')

POSITION_KEYWORDS = [
    'ceo', 'cto', 'cfo', 'coo', 'director', 'manager', 'engineer',
    'developer', 'designer', 'consultant', 'analyst', 'specialist',
    'coordinator', 'president', 'founder', 'partner', 'associate',
    'officer', 'head', 'lead', 'senior', 'junior', 'vp',
    'dyrektor', 'kierownik', 'specjalista', 'prezes', 'inżynier',
    'koordynator', 'konsultant', 'architekt', 'programista',
    'zarządu', 'zarząd', 'wiceprezes', 'członek', 'zastępca',
    'handlowiec', 'przedstawiciel', 'doradca', 'ekspert',
]

COMPANY_SUFFIXES = [
    'sp. z o.o.', 'sp.z o.o.', 'sp. z o. o.', 's.a.', 'sp.j.', 'sp.k.',
    'ltd', 'llc', 'inc', 'corp', 'gmbh', 'ag',
    'group', 'grupa', 'holdings', 'solutions', 'consulting',
    'technologies', 'services', 'company',
]

# Words that indicate a line is NOT a person's name
NON_NAME_INDICATORS = [
    '@', 'www.', 'http', '.pl', '.com', '.eu', '.net',
    'tel', 'fax', 'mob', 'nip', 'regon', 'krs',
    'ul.', 'al.', 'os.', 'pl.',
]


def _is_name_line(line: str) -> bool:
    """Check if a line looks like a person's name."""
    words = line.split()
    if not (2 <= len(words) <= 3):
        return False
    lower = line.lower()
    # Skip lines with non-name indicators
    if any(ind in lower for ind in NON_NAME_INDICATORS):
        return False
    # Skip lines matching company or position patterns
    if any(suf in lower for suf in COMPANY_SUFFIXES):
        return False
    if any(kw in lower for kw in POSITION_KEYWORDS):
        return False
    # Skip lines with digits
    if any(c.isdigit() for c in line):
        return False
    # Each word should be mostly letters and start with uppercase
    for w in words:
        letters = [c for c in w if c.isalpha()]
        if len(letters) < 2:
            return False
        if not w[0].isupper():
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

    # 2) Phone — look for line that contains mostly digits
    for i, line in enumerate(lines):
        if i in used_lines:
            continue
        m = PHONE_RE.search(line)
        if m:
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

    # 7) Fallback company — first remaining unused line that isn't a short word
    if not result['company']:
        for i, line in enumerate(lines):
            if i in used_lines:
                continue
            result['company'] = line
            break

    return result
