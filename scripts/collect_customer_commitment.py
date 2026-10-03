"""Capture one bounded SEC customer-commitment case as unapproved research.

SEC network mode requires an identifying User-Agent, which is never persisted.
The explicit issuer route uses a public metadata feed and its fixed HTML mirror.
Offline mode imports actual captured HTML without claiming remote availability.
Hash-addressed sources and capture records preserve earlier revisions; the root
record is a current view, not a governed Evidence or H1 dataset amendment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


PARSER_VERSION = "1.1.0"
ACCESSION = "0001193125-25-216497"
CIK = "1769628"
BASE_URL = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{ACCESSION.replace('-', '')}/"
DOCUMENT_NAME = "d17274d8k.htm"
INDEX_NAME = f"{ACCESSION}-index.html"
SOURCE_URLS = {"document": BASE_URL + DOCUMENT_NAME, "index": BASE_URL + INDEX_NAME}
ISSUER_FILING_ID = 18796309
ISSUER_DOCUMENT_NAME = "coreweave_openai_20250925_8k_issuer_mirror.html"
ISSUER_FEED_NAME = "issuer_q4_filings_2025.json"
ISSUER_SOURCE_URLS = {
    "document": "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001769628/a5d34350-7a13-4e70-a811-c41398bb7fe9.html",
    "feed": "https://investors.coreweave.com/feed/SECFiling.svc/GetEdgarFilingList?LanguageId=1&exchange=CIK&symbol=0001769628&formGroupIdList=&filingTypeList=8-K&excludeNoDocuments=true&includeHtmlDocument=true&pageSize=-1&pageNumber=0&tagList=&includeTags=true&year=2025&excludeSelection=1",
}
DEFAULT_OUTPUT = Path("data/research/customer_commitments/coreweave_openai_20250923")
MAX_DOCUMENT_BYTES = 1_048_576
DATE_PATTERN = r"[A-Z][a-z]+\s+\d{1,2},\s+\d{4}"
STATUS = "RESEARCH_CANDIDATE_NOT_GOVERNED_EVIDENCE"


class CaptureError(ValueError):
    """A bounded acquisition, source-drift or integrity failure."""

    def __init__(self, message, *, source_url=None, http_status=None):
        super().__init__(message)
        self.source_url = source_url
        self.http_status = http_status


class VisibleHTML(HTMLParser):
    """Keep visible text and links, excluding hidden/script/style content."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    BLOCK = {"br", "p", "div", "tr", "td", "th", "li", "h1", "h2", "h3", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []
        self.parts: list[str] = []
        self.links: list[str] = []
        self.anchors: list[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = dict(attrs)
        hidden = any(flag for _, flag in self.stack) or tag in {"script", "style", "head", "ix:header"}
        hidden = hidden or "hidden" in attributes or attributes.get("aria-hidden") == "true"
        hidden = hidden or bool(re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden)", attributes.get("style", ""), re.I))
        if not hidden:
            if tag in self.BLOCK:
                self.parts.append(" ")
            if tag == "a" and attributes.get("href"):
                self.links.append(attributes["href"])
            for attribute in ("id", "name"):
                if attributes.get(attribute):
                    self.anchors.append(attributes[attribute])
        if tag not in self.VOID:
            self.stack.append((tag, hidden))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag.lower():
                del self.stack[index:]
                break
        if tag.lower() in self.BLOCK:
            self.parts.append(" ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag.lower() not in self.VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if not any(flag for _, flag in self.stack):
            self.parts.append(data)

    @property
    def text(self):
        return " ".join("".join(self.parts).split())


def visible_html(raw: bytes) -> VisibleHTML:
    if not raw or len(raw) > MAX_DOCUMENT_BYTES:
        raise CaptureError("source empty or exceeds the bounded document size")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise CaptureError("source encoding changed; UTF-8 review required") from None
    if not re.search(r"<(?:html|body|p|div|table)\b", text, re.I):
        raise CaptureError("source is not an HTML document")
    parser = VisibleHTML()
    parser.feed(text)
    parser.close()
    return parser


def require(pattern: str, text: str, description: str, flags=0):
    match = re.search(pattern, text, flags)
    if not match:
        raise CaptureError(f"source drift: missing {description}")
    return match


def calendar_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%B %d, %Y").date().isoformat()
    except ValueError:
        raise CaptureError("source drift: unsupported calendar date") from None


def parse_case(document: bytes, index: bytes, *, allow_synthetic=False) -> dict:
    """Extract values from visible anchors; expected values are not supplied."""
    index_html = visible_html(index)
    idx = index_html.text
    if b"SYNTHETIC TEST FIXTURE" in index and not allow_synthetic:
        raise CaptureError("synthetic fixture cannot be imported as a public source capture")
    require(r"Form\s+8-K", idx, "8-K filing-index form")
    require(re.escape(ACCESSION), idx, "target accession")
    require(r"\b0*" + CIK + r"\b", idx, "target CIK")
    if not any(urljoin(SOURCE_URLS["index"], href) == SOURCE_URLS["document"] for href in index_html.links):
        raise CaptureError("source drift: filing index no longer links the target document")
    filing_match = require(r"Filing Date\s+(\d{4}-\d{2}-\d{2})", idx, "index filing date")
    period_match = require(r"Period of Report\s+(\d{4}-\d{2}-\d{2})", idx, "index report period")
    accepted_match = require(r"Accepted\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", idx, "index acceptance timestamp")
    record = extract_document(document, publication_date=filing_match.group(1), report_period=period_match.group(1), accepted_at_source=accepted_match.group(1), allow_synthetic=allow_synthetic)
    record.update({"source_route": "sec", "accession_observed_in_raw_source": True, "source_is_synthetic": record["source_is_synthetic"] or b"SYNTHETIC TEST FIXTURE" in index})
    return record


def parse_issuer_case(document: bytes, feed: bytes, *, allow_synthetic=False) -> dict:
    """Match an issuer metadata row to actual mirrored HTML, never a fake index."""
    if not feed or len(feed) > MAX_DOCUMENT_BYTES:
        raise CaptureError("issuer feed empty or exceeds the bounded document size")
    synthetic_feed = b"SYNTHETIC TEST FIXTURE" in feed
    if synthetic_feed and not allow_synthetic:
        raise CaptureError("synthetic issuer feed cannot be imported as a public source capture")
    try:
        metadata = json.loads(feed.decode("utf-8-sig"))
        rows = metadata["GetEdgarFilingListResult"]
        if not isinstance(rows, list):
            raise TypeError
        selected = [row for row in rows if row.get("FilingId") == ISSUER_FILING_ID]
    except (UnicodeDecodeError, ValueError, KeyError, TypeError, AttributeError):
        raise CaptureError("source drift: issuer feed schema is not the expected filing list") from None
    if len(selected) != 1:
        raise CaptureError("source drift: issuer filing ID is absent or duplicated")
    row = selected[0]
    if row.get("StockExchange") != "CIK" or row.get("FilingTypeMnemonic") != "8-K" or str(row.get("StockSymbol", "")).lstrip("0") != CIK:
        raise CaptureError("source drift: issuer feed form or CIK changed")
    documents = row.get("DocumentList", [])
    if not isinstance(documents, list) or any(not isinstance(entry, dict) for entry in documents):
        raise CaptureError("source drift: issuer document-list schema changed")
    html_entries = [entry for entry in documents if entry.get("DocumentType") == "HTML"]
    if len(html_entries) != 1 or html_entries[0].get("Url") != ISSUER_SOURCE_URLS["document"]:
        raise CaptureError("source drift: issuer feed HTML URL changed or is ambiguous")
    try:
        publication_date = datetime.strptime(row["FilingDate"], "%m/%d/%Y %H:%M:%S").date().isoformat()
    except (KeyError, TypeError, ValueError):
        raise CaptureError("source drift: issuer filing date format changed") from None
    if "d17274d8k_htm" not in [anchor.lower() for anchor in visible_html(document).anchors]:
        raise CaptureError("source drift: issuer mirror main-document anchor changed")
    record = extract_document(document, publication_date=publication_date, report_period=None, accepted_at_source=None, allow_synthetic=allow_synthetic)
    record.update({
        "source_route": "issuer", "accession": None,
        "source_is_synthetic": record["source_is_synthetic"] or synthetic_feed,
        "accession_observed_in_raw_source": False,
        "issuer_filing_id": row["FilingId"],
        "issuer_filing_date_raw": row["FilingDate"],
        "issuer_filing_date_note": "Vendor filing-date clock is not an SEC acceptance or first-availability timestamp; only its calendar date is used",
        "known_at_basis": "Issuer filing feed FilingDate, matched to the 8-K cover; day precision only",
        "accepted_at_timezone_note": "SEC acceptance timestamp is not established by this issuer feed or mirrored document",
        "canonical_sec_reference": {"accession": ACCESSION, "document_url": SOURCE_URLS["document"], "index_url": SOURCE_URLS["index"]},
        "canonical_sec_match_basis": "Manual comparison reported in research: cover dates, named parties, new order form, existing MSA, conditional maximum and term; not an automated accession match",
        "canonical_sec_match_status": "RESEARCH_REFERENCE_REQUIRES_REVIEW_NOT_AUTOMATED_MATCH",
        "sec_raw_byte_identity_verified": False,
        "source_identity_note": "Issuer-hosted filing mirror linked by the issuer's public metadata feed; SEC original/index bytes were not substituted or fabricated",
    })
    return record


def extract_document(document: bytes, *, publication_date: str, report_period: str | None, accepted_at_source: str | None, allow_synthetic=False) -> dict:
    """Shared visible 8-K extraction with route-specific publication metadata."""
    doc = visible_html(document).text
    synthetic = b"SYNTHETIC TEST FIXTURE" in document
    if synthetic and not allow_synthetic:
        raise CaptureError("synthetic fixture cannot be imported as a public source capture")
    item_match = require(r"Item\s*1\.01\s+Entry into a Material Definitive Agreement\.", doc, "visible Item 1.01")
    end_match = require(r"Item\s*9\.01\b", doc[item_match.end():], "Item 9.01 section boundary")
    item_end = item_match.end() + end_match.start()
    item = doc[item_match.end():item_end]
    event = require(r"On\s+(" + DATE_PATTERN + r"),\s+(CoreWeave,\s*Inc\.)", item, "dated supplier agreement")
    customer = require(r"and\s+(OpenAI OpCo,\s*LLC)\s*\(", item, "named customer")
    require(r"entered into a new order form", item, "new order-form event")
    msa = require(r"existing Master Services Agreement.*?dated as of\s+(" + DATE_PATTERN + r")", item, "existing MSA date")
    require(r"access to cloud computing capacity", item, "cloud-capacity scope")
    payment = require(r"Subject to any termination described below and satisfaction of delivery and availability of service requirements,\s+OpenAI has committed to pay the Company\s+up to approximately\s+\$([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)\s+(billion|million)\s+through\s+(" + DATE_PATTERN + r")\s+under the Order Form\.", item, "conditional maximum payment and term")
    require(r"Either party may terminate the MSA\s*\(and any order thereunder\)\s+for cause\.", item, "termination-for-cause rights")
    require(r"does not purport to be complete.*?qualified in its entirety.*?Exhibit\s+10\.1", item, "summary-only exhibit qualification")
    report = require(r"Date of Report\s*\(date of earliest event reported\):\s*(" + DATE_PATTERN + r")\s*\((" + DATE_PATTERN + r")\)", doc, "cover report dates")
    event_date = calendar_date(event.group(1))
    if publication_date != calendar_date(report.group(1)) or event_date != calendar_date(report.group(2)) or (report_period is not None and event_date != report_period):
        raise CaptureError("source drift: cover, index and agreement dates disagree")
    if event_date > publication_date or calendar_date(msa.group(1)) > event_date or calendar_date(payment.group(3)) <= event_date:
        raise CaptureError("source drift: agreement date ordering is inconsistent")
    number = Decimal(payment.group(1).replace(",", ""))
    amount = number * {"billion": Decimal(1_000_000_000), "million": Decimal(1_000_000)}[payment.group(2)]
    if amount <= 0 or amount != amount.to_integral_value():
        raise CaptureError("source drift: maximum amount is not positive whole USD")
    excerpt_match = require(r"availability of service requirements,.*?under the Order Form\.", payment.group(0), "payment excerpt")
    excerpt_start = item_match.end() + payment.start() + excerpt_match.start()

    def span(match, group=0):
        return [item_match.end() + match.start(group), item_match.end() + match.end(group)]

    return {
        "schema_version": "1.0", "parser_version": PARSER_VERSION,
        "case_id": f"coreweave-openai-{event_date}", "accession": ACCESSION, "cik": CIK,
        "status": STATUS, "source_is_synthetic": synthetic,
        "event_kind": "NEW_ORDER_FORM", "stage_family": "demand",
        "stage": "CONDITIONAL_CUSTOMER_COMMITMENT",
        "supplier_legal_name": event.group(2), "customer_legal_name": customer.group(1),
        "scope": "cloud_computing_capacity", "event_date": event_date,
        "publication_date": publication_date, "known_at": publication_date,
        "known_at_precision": "day", "known_at_basis": "SEC filing-index Filing Date; not the event date",
        "accepted_at_source": accepted_at_source, "accepted_at_source_timezone": None,
        "accepted_at_timezone_note": "SEC index does not label a timezone; no UTC conversion made",
        "existing_msa_date": calendar_date(msa.group(1)),
        "commitment_end_date": calendar_date(payment.group(3)),
        "maximum_commitment_usd": int(amount), "currency": "USD",
        "amount_qualifiers": ["UP_TO", "APPROXIMATE", "CONDITIONAL"],
        "amount_basis": "order-form maximum commitment over its term; not annual revenue or cash received",
        "conditions": {"delivery_requirements": True, "service_availability_requirements": True, "termination_rights": True},
        "minimum_purchase_usd": None, "actual_cash_received_usd": None,
        "prepayment_usd": None, "actual_usage": None, "revenue_recognized_usd": None,
        "unknown_reason": "Not established by the bounded Item 1.01 summary; null does not mean zero",
        "summary_only": True, "full_msa_and_redacted_exhibits_reviewed": False,
        "source_original_excerpt": excerpt_match.group(0),
        "locator": {"section": "Item 1.01", "paragraph": "conditional payment commitment", "text_normalization": "HTML entities decoded; visible whitespace collapsed", "visible_text_char_range": [excerpt_start, excerpt_start + len(excerpt_match.group(0))]},
        "field_locators": {"event_date": span(event, 1), "supplier": span(event, 2), "customer": span(customer, 1), "existing_msa_date": span(msa, 1), "maximum_commitment": span(payment, 1), "commitment_end_date": span(payment, 3)},
        "empirical_dataset_admitted": False, "human_evidence_approved": False,
        "predictive_validity_established": False, "automatic_h1_admission": False,
    }


def validate_source_url(url: str, source_route="sec"):
    allowed = SOURCE_URLS if source_route == "sec" else ISSUER_SOURCE_URLS if source_route == "issuer" else {}
    parts = urlsplit(url)
    allowed_hosts = {urlsplit(value).hostname for value in allowed.values()}
    if parts.scheme != "https" or parts.hostname not in allowed_hosts or parts.username or parts.password or parts.port not in (None, 443) or parts.fragment:
        raise CaptureError("only the bounded official HTTPS source route is allowed")
    if url not in allowed.values():
        raise CaptureError("source URL is outside the bounded case")


class BoundedRedirect(HTTPRedirectHandler):
    def __init__(self, source_route="sec"):
        super().__init__()
        self.source_route = source_route

    def redirect_request(self, request, fp, code, message, headers, newurl):
        validate_source_url(newurl, self.source_route)
        return super().redirect_request(request, fp, code, message, headers, newurl)


def fetch_source(url: str, user_agent: str, source_route="sec") -> bytes:
    validate_source_url(url, source_route)
    if source_route == "issuer" and not user_agent:
        user_agent = "sk-public-customer-commitment-research/1.1"
    if not user_agent or len(user_agent.strip()) < 8 or any(ord(char) < 32 for char in user_agent):
        raise CaptureError("network capture requires a valid identifying SEC User-Agent")
    is_feed = url == ISSUER_SOURCE_URLS["feed"]
    request = Request(url, headers={"User-Agent": user_agent, "Accept": "application/json" if is_feed else "text/html", "Accept-Encoding": "identity"})
    try:
        with build_opener(BoundedRedirect(source_route)).open(request, timeout=30) as response:
            validate_source_url(response.geturl(), source_route)
            allowed_types = {"application/json", "text/json", "text/plain"} if is_feed else {"text/html", "application/xhtml+xml"}
            if response.status != 200 or response.headers.get_content_type() not in allowed_types:
                raise CaptureError("official source response was not successful expected-format content")
            raw = response.read(MAX_DOCUMENT_BYTES + 1)
    except HTTPError as error:
        raise CaptureError(f"official source HTTP request failed with status {error.code}; no source capture accepted", source_url=url, http_status=error.code) from None
    except (URLError, TimeoutError, OSError):
        raise CaptureError("official source network request failed; no source capture accepted") from None
    if not raw or len(raw) > MAX_DOCUMENT_BYTES:
        raise CaptureError("source empty or exceeds the bounded document size")
    if not is_feed:
        visible_html(raw)
    return raw


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_directory(path: Path) -> Path:
    if ".." in path.parts:
        raise CaptureError("parent traversal is not allowed in a capture path")
    absolute = path.absolute()
    for candidate in [absolute, *absolute.parents]:
        if candidate.is_symlink() or (hasattr(candidate, "is_junction") and candidate.is_junction()):
            raise CaptureError("capture paths cannot traverse symbolic links or junctions")
    return absolute


def write_immutable(path: Path, raw: bytes):
    safe_directory(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(raw)
    except FileExistsError:
        if path.read_bytes() != raw:
            raise CaptureError("immutable capture artifact differs from its recorded content") from None


def write_current(path: Path, raw: bytes):
    safe_directory(path)
    temporary = path.with_name(path.name + ".tmp")
    write_immutable(temporary, raw)
    temporary.replace(path)


def capture(output_dir: Path, documents: dict[str, bytes], *, mode: str, source_route="sec", allow_synthetic=False, timestamp=None) -> dict:
    output = safe_directory(output_dir)
    if mode not in {"network", "offline_import"}:
        raise CaptureError("unsupported acquisition mode")
    source_urls = SOURCE_URLS if source_route == "sec" else ISSUER_SOURCE_URLS if source_route == "issuer" else {}
    if not source_urls or set(documents) != set(source_urls):
        raise CaptureError("capture source roles disagree with the chosen route")
    record = parse_case(documents["document"], documents["index"], allow_synthetic=allow_synthetic) if source_route == "sec" else parse_issuer_case(documents["document"], documents["feed"], allow_synthetic=allow_synthetic)
    now = timestamp or datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    hashes = {name: sha256(raw) for name, raw in documents.items()}
    capture_id = sha256((PARSER_VERSION + "\n" + source_route + "\n" + "\n".join(hashes[name] for name in source_urls)).encode("ascii"))
    ledger_path = output / "acquisition.json"
    if (output / "record.json").exists() and not ledger_path.exists():
        raise CaptureError("existing record has no capture ledger; refusing to overwrite")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.exists() else {"schema_version": "1.0", "case_id": record["case_id"], "status": STATUS, "captures": [], "current_capture_id": None}
    if ledger.get("case_id") != record["case_id"] or ledger.get("status") != STATUS:
        raise CaptureError("output directory belongs to a different or approved dataset")
    if ledger_path.exists():
        verify_capture(output)
    if any(entry["capture_id"] == capture_id for entry in ledger["captures"]):
        return {"status": "ALREADY_CAPTURED", "capture_id": capture_id, "capture_count": len(ledger["captures"])}
    source_records = []
    for name in source_urls:
        relative = f"sources/{hashes[name]}.{'json' if name == 'feed' else 'html'}"
        write_immutable(output / relative, documents[name])
        role = ("SEC_ARCHIVE_DOCUMENT" if name == "document" else "SEC_FILING_INDEX") if source_route == "sec" else ("ISSUER_HOSTED_FILING_MIRROR" if name == "document" else "ISSUER_FILING_METADATA_FEED")
        source_records.append({"source_id": f"{source_route}-{ACCESSION if source_route == 'sec' else ISSUER_FILING_ID}-{name}", "source_role": role, "source_url": source_urls[name], "source_host": urlsplit(source_urls[name]).hostname, "sha256": hashes[name], "bytes": len(documents[name]), "raw_file": relative, "retrieved_at_utc": now, "retrieval_method": mode, "remote_retrieved_at_utc": now if mode == "network" else None})
    record.update({"capture_id": capture_id, "retrieved_at_utc": now, "retrieval_method": mode, "remote_availability_verified_in_this_run": mode == "network", "sources": source_records, "supersedes_capture_id": ledger["current_capture_id"]})
    if record["source_is_synthetic"]:
        record["remote_availability_verified_in_this_run"] = False
    record_raw = json_bytes(record)
    relative_record = f"captures/{capture_id}/record.json"
    acquisition = {"schema_version": "1.0", "capture_id": capture_id, "parser_version": PARSER_VERSION, "status": STATUS, "source_route": source_route, "retrieval_method": mode, "retrieved_at_utc": now, "source_is_synthetic": record["source_is_synthetic"], "sources": source_records, "record_file": relative_record, "record_sha256": sha256(record_raw)}
    write_immutable(output / relative_record, record_raw)
    write_immutable(output / f"captures/{capture_id}/acquisition.json", json_bytes(acquisition))
    ledger["captures"].append({"capture_id": capture_id, "record_file": relative_record, "acquisition_file": f"captures/{capture_id}/acquisition.json", "record_sha256": sha256(record_raw), "acquisition_sha256": sha256(json_bytes(acquisition)), "retrieved_at_utc": now})
    ledger["current_capture_id"] = capture_id
    output.mkdir(parents=True, exist_ok=True)
    write_current(output / "record.json", record_raw)
    write_current(ledger_path, json_bytes(ledger))
    verify_capture(output)
    return {"status": "CAPTURED", "capture_id": capture_id, "capture_count": len(ledger["captures"])}


def bounded_file(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or path.drive:
        raise CaptureError("capture manifest path escapes the package")
    target = safe_directory(root / path)
    if not target.is_relative_to(root):
        raise CaptureError("capture manifest path escapes the package")
    return target


def verify_capture(output_dir: Path) -> dict:
    output = safe_directory(output_dir)
    ledger = json.loads((output / "acquisition.json").read_text(encoding="utf-8"))
    if ledger.get("status") != STATUS or not ledger.get("captures"):
        raise CaptureError("capture ledger is empty or not candidate research")
    ids = [entry["capture_id"] for entry in ledger["captures"]]
    if len(ids) != len(set(ids)) or ledger["current_capture_id"] not in ids:
        raise CaptureError("capture ledger contains duplicated or dangling revision IDs")
    for entry in ledger["captures"]:
        record_raw = bounded_file(output, entry["record_file"]).read_bytes()
        acquisition_raw = bounded_file(output, entry["acquisition_file"]).read_bytes()
        if sha256(record_raw) != entry["record_sha256"] or sha256(acquisition_raw) != entry["acquisition_sha256"]:
            raise CaptureError("immutable capture record hash mismatch")
        record, acquisition = json.loads(record_raw), json.loads(acquisition_raw)
        if record["capture_id"] != entry["capture_id"] or acquisition["capture_id"] != entry["capture_id"] or record["status"] != STATUS or acquisition["status"] != STATUS or record["case_id"] != ledger["case_id"]:
            raise CaptureError("capture identity or candidate status changed")
        if acquisition["sources"] != record["sources"] or acquisition["record_sha256"] != sha256(record_raw) or acquisition["record_file"] != entry["record_file"] or len(record["sources"]) != 2:
            raise CaptureError("capture acquisition receipt disagrees with its record")
        route = record["source_route"]
        source_urls = SOURCE_URLS if route == "sec" else ISSUER_SOURCE_URLS if route == "issuer" else {}
        if not source_urls or acquisition["source_route"] != route:
            raise CaptureError("capture source route changed")
        documents = {}
        for name, source in zip(source_urls, record["sources"]):
            validate_source_url(source["source_url"], route)
            if source["source_url"] != source_urls[name] or source["source_host"] != urlsplit(source_urls[name]).hostname:
                raise CaptureError("source roles disagree with bounded source URLs")
            raw = bounded_file(output, source["raw_file"]).read_bytes()
            if sha256(raw) != source["sha256"] or len(raw) != source["bytes"]:
                raise CaptureError("raw source content hash mismatch")
            documents[name] = raw
        replay_id = sha256((record["parser_version"] + "\n" + route + "\n" + "\n".join(sha256(documents[name]) for name in source_urls)).encode("ascii"))
        if replay_id != entry["capture_id"]:
            raise CaptureError("capture ID does not match the parser and raw source hashes")
        parsed = parse_case(documents["document"], documents["index"], allow_synthetic=record["source_is_synthetic"]) if route == "sec" else parse_issuer_case(documents["document"], documents["feed"], allow_synthetic=record["source_is_synthetic"])
        for key, value in parsed.items():
            if record.get(key) != value:
                raise CaptureError("record disagrees with deterministic source extraction")
        if entry["capture_id"] == ledger["current_capture_id"] and (output / "record.json").read_bytes() != record_raw:
            raise CaptureError("current record view differs from its immutable capture")
    return {"status": "PASS", "capture_count": len(ids), "evidence_approved": False, "predictive_validity_established": False}


def preserve_failure(output_dir: Path, error: CaptureError, documents: dict[str, bytes], mode: str, source_route="sec"):
    """Keep a failed attempt separate from accepted captures, without identity."""
    output = safe_directory(output_dir)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    receipt = {
        "schema_version": "1.0", "status": "FAILED_NO_ACCEPTED_SOURCE_CAPTURE",
        "attempted_at_utc": now, "retrieval_method": mode, "source_route": source_route,
        "error": str(error), "http_status": error.http_status,
        "failed_source_url": error.source_url, "accepted_record_created": False,
        "sources_obtained_before_failure": [],
    }
    source_urls = SOURCE_URLS if source_route == "sec" else ISSUER_SOURCE_URLS
    for name, raw in documents.items():
        if name not in source_urls or not raw or len(raw) > MAX_DOCUMENT_BYTES:
            continue
        digest = sha256(raw)
        relative = f"sources/{digest}.{'json' if name == 'feed' else 'html'}"
        write_immutable(output / relative, raw)
        receipt["sources_obtained_before_failure"].append({"source_url": source_urls[name], "sha256": digest, "bytes": len(raw), "raw_file": relative, "source_accepted": False})
    write_immutable(output / "acquisition_failures" / f"{uuid.uuid4().hex}.json", json_bytes(receipt))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--source", choices=("sec", "issuer"), default="sec", help="Explicit bounded source route; no automatic fallback")
    parser.add_argument("--source-dir", type=Path, help="Import captured d17274d8k.htm and accession index HTML; no network claim")
    parser.add_argument("--issuer-source-dir", type=Path, help="Import actual issuer_q4_filings_2025.json and issuer mirror HTML; no SEC-index substitution")
    parser.add_argument("--user-agent", help="Identifying SEC User-Agent, or SEC_USER_AGENT environment variable; never stored")
    parser.add_argument("--verify-only", action="store_true", help="Verify saved hashes and replay extraction without network requests")
    args = parser.parse_args(argv)
    documents = {}
    source_route = "issuer" if args.issuer_source_dir else args.source
    mode = "offline_import" if args.source_dir or args.issuer_source_dir else "network"
    try:
        if args.source_dir and (args.issuer_source_dir or source_route != "sec"):
            raise CaptureError("SEC source-dir cannot be mixed with the issuer source route")
        if args.verify_only:
            if args.source_dir or args.issuer_source_dir or args.user_agent:
                raise CaptureError("verify-only does not accept acquisition arguments")
            result = verify_capture(args.output_dir)
        elif args.source_dir or args.issuer_source_dir:
            source = safe_directory(args.issuer_source_dir or args.source_dir)
            files = (("document", DOCUMENT_NAME), ("index", INDEX_NAME)) if source_route == "sec" else (("document", ISSUER_DOCUMENT_NAME), ("feed", ISSUER_FEED_NAME))
            for name, filename in files:
                path = safe_directory(source / filename)
                with path.open("rb") as handle:
                    documents[name] = handle.read(MAX_DOCUMENT_BYTES + 1)
            result = capture(args.output_dir, documents, mode="offline_import", source_route=source_route)
        else:
            user_agent = args.user_agent or (os.environ.get("SEC_USER_AGENT", "") if source_route == "sec" else "")
            source_urls = SOURCE_URLS if source_route == "sec" else ISSUER_SOURCE_URLS
            for name, url in source_urls.items():
                documents[name] = fetch_source(url, user_agent, source_route)
            result = capture(args.output_dir, documents, mode="network", source_route=source_route)
        print(json.dumps(result, sort_keys=True))
        return 0
    except CaptureError as error:
        if not args.verify_only:
            try:
                preserve_failure(args.output_dir, error, documents, mode, source_route)
            except (CaptureError, OSError):
                pass  # Failed or unsafe output paths must not obscure the source failure.
        print(f"Collection failed: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        print("Collection failed: local artifact or JSON integrity error; no source acceptance claimed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
