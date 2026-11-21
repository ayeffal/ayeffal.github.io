"""Input schema for the vault's site export, schema_version 1.

Contract: design/reply-from-vault-agent.md. Rejects anything unknown or
missing. Error messages name an item index and a field, never a value, so a
report cannot leak titles (decision 0009).
"""

import datetime
import calendar
import re

SCHEMA_VERSION = 1

COMMON_REQUIRED = {"uid", "type", "title", "date", "authors"}
COMMON_OPTIONAL = {"date_precision"}

PUBLICATION_REQUIRED = {"pub_type", "pub_status"}
PUBLICATION_OPTIONAL = {
    "article_kind", "venue", "doi", "volume", "pages",
    "preprint_url", "open_copy_url", "open_copy_kind",
}
COMMUNICATION_REQUIRED = {"meeting", "format"}
COMMUNICATION_OPTIONAL = {"abstract_published_in", "url"}

ENUMS = {
    "type": {"publication", "communication"},
    "date_precision": {"month", "year"},
    "pub_type": {"article", "chapter", "book"},
    "article_kind": {"original", "review"},
    "pub_status": {"published", "in-press", "preprint"},
    "open_copy_kind": {"preprint", "accepted-manuscript"},
    "format": {"poster", "oral", "lecture"},
}
URL_FIELDS = {"preprint_url", "open_copy_url", "url"}
# Fields that must not appear on a preprint (venue is hidden on purpose).
PREPRINT_FORBIDDEN = {"venue", "doi", "volume", "pages", "open_copy_url", "open_copy_kind"}

UID_RE = re.compile(r"^r-[a-z0-9]{8}$")
URL_RE = re.compile(r"^https?://\S+$")


class ExportError(Exception):
    """The export does not match schema version 1."""


def _valid_date(s):
    try:
        return datetime.date.fromisoformat(s) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s) else None
    except ValueError:
        return None


def _check_item(i, item, errors):
    where = f"items[{i}]"
    if not isinstance(item, dict):
        errors.append(f"{where}: not a mapping")
        return None
    itype = item.get("type")
    if itype == "publication":
        required = COMMON_REQUIRED | PUBLICATION_REQUIRED
        allowed = required | COMMON_OPTIONAL | PUBLICATION_OPTIONAL
    elif itype == "communication":
        required = COMMON_REQUIRED | COMMUNICATION_REQUIRED
        allowed = required | COMMON_OPTIONAL | COMMUNICATION_OPTIONAL
    else:
        errors.append(f"{where}.type: missing or unknown")
        return None

    for f in sorted(required - item.keys()):
        errors.append(f"{where}.{f}: required field missing")
    for f in sorted(item.keys() - allowed):
        errors.append(f"{where}.{f}: unknown field for {itype}")

    for f, v in item.items():
        if f not in allowed:
            continue
        if f == "authors":
            if not (isinstance(v, list) and v and all(isinstance(a, str) and a.strip() for a in v)):
                errors.append(f"{where}.authors: must be a non-empty list of strings")
            continue
        if not isinstance(v, str) or not v.strip():
            errors.append(f"{where}.{f}: must be a non-empty string (quote it in YAML)")
            continue
        if f in ENUMS and v not in ENUMS[f]:
            errors.append(f"{where}.{f}: unknown value")
        elif f == "uid" and not UID_RE.match(v):
            errors.append(f"{where}.uid: does not match r-[a-z0-9]{{8}}")
        elif f in URL_FIELDS and not URL_RE.match(v):
            errors.append(f"{where}.{f}: must be an http(s) URL")
        elif f == "doi" and (v.lower().startswith(("http", "doi:")) or "doi.org" in v.lower()):
            errors.append(f"{where}.doi: must be the bare DOI")

    # date and date_precision
    d = item.get("date")
    if isinstance(d, str):
        parsed = _valid_date(d)
        if parsed is None:
            errors.append(f"{where}.date: must be a valid YYYY-MM-DD")
        else:
            prec = item.get("date_precision")
            last_day = calendar.monthrange(parsed.year, parsed.month)[1]
            if prec == "month" and parsed.day != last_day:
                errors.append(f"{where}.date: precision month needs the last day of the month")
            if prec == "year" and (parsed.month, parsed.day) != (12, 31):
                errors.append(f"{where}.date: precision year needs 31 December")

    if itype == "publication":
        is_article = item.get("pub_type") == "article"
        if is_article and "article_kind" not in item:
            errors.append(f"{where}.article_kind: required for an article")
        if not is_article and "article_kind" in item:
            errors.append(f"{where}.article_kind: only allowed for an article")
        status = item.get("pub_status")
        if status == "preprint":
            for f in sorted(PREPRINT_FORBIDDEN & item.keys()):
                errors.append(f"{where}.{f}: not allowed on a preprint")
            if "preprint_url" not in item:
                errors.append(f"{where}.preprint_url: required on a preprint")
        elif status in ENUMS["pub_status"]:
            if "venue" not in item:
                errors.append(f"{where}.venue: required unless preprint")
            if "preprint_url" in item:
                errors.append(f"{where}.preprint_url: only allowed on a preprint")
        if ("open_copy_url" in item) != ("open_copy_kind" in item):
            errors.append(f"{where}: open_copy_url and open_copy_kind go together")

    return item.get("uid") if isinstance(item.get("uid"), str) else None


def validate_export(data):
    """Return a list of error strings; empty means valid."""
    errors = []
    if not isinstance(data, dict):
        return ["top level: not a mapping"]
    version = data.get("schema_version")
    if isinstance(version, bool) or version != SCHEMA_VERSION:
        # Stop here: any other version may mean a different shape.
        return [f"schema_version: expected {SCHEMA_VERSION}"]
    for k in sorted(data.keys() - {"schema_version", "items"}):
        errors.append(f"top level: unknown key {k}")
    items = data.get("items")
    if not isinstance(items, list):
        errors.append("items: must be a list (an empty export is `items: []`)")
        return errors
    seen = set()
    for i, item in enumerate(items):
        uid = _check_item(i, item, errors)
        if uid is not None:
            if uid in seen:
                errors.append(f"items[{i}].uid: duplicate")
            seen.add(uid)
    return errors


def load_export(path):
    """Read and validate the export file. Raise ExportError on any problem."""
    import yaml  # PyYAML: the only third-party dependency

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    errors = validate_export(data)
    if errors:
        raise ExportError("\n".join(errors))
    return data["items"]
