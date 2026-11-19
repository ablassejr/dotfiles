"""Shared issue and pull-request content contract for supported publication adapters."""

from html import unescape
from html.parser import HTMLParser
import re
from urllib.parse import urlsplit, urlunsplit

from .client import RuntimeFailure

POLICY = "self-contained-issue-design-proposal-only-v1"


def normalized_url(value):
    parts = urlsplit(unescape(value).strip())
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), parts.path, parts.query, "")
    )


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        self.urls.extend(
            value for key, value in attrs if key in {"href", "src"} and value
        )


def references(text, literal_examples=False):
    if literal_examples:
        text = re.sub(r"(?ms)^\s{0,3}(`{3,}|~{3,})[^\n]*\n.*?^\s{0,3}\1\s*$", "", text)
        text = re.sub(r"(`+).*?\1", "", text, flags=re.S)
    parser = Links()
    parser.feed(text)
    urls = parser.urls
    urls += re.findall(r"!?\[[^\]\n]*\]\(\s*<?([^\s)>]+)", text)
    urls += re.findall(r"(?m)^\s{0,3}\[(?!\^)[^\]\n]+\]:\s*<?([^\s>]+)", text)
    urls += re.findall(r"(?:[A-Za-z][A-Za-z0-9+.-]*://|www\.)[^\s<>\[\]\"'`]+", text)
    return {url.rstrip(".,;:!?)") for url in urls}


def operational_link(url, pull_request=False):
    parts = urlsplit(url)
    if pull_request and parts.scheme == "https" and parts.hostname == "github.com":
        if re.fullmatch(
            r"/[^/]+/[^/]+/(?:issues/\d+|commit/[0-9a-fA-F]+|actions/runs/\d+(?:/job/\d+)?)/?",
            parts.path,
        ):
            return True
    return parts.scheme == "https" and (
        parts.hostname == "linear.app"
        and re.match(r"/[^/]+/issue/[^/]+", parts.path)
        or parts.hostname == "github.com"
        and re.match(r"/[^/]+/[^/]+/pull/\d+(?:/|$)", parts.path)
    )


def validate_content(content, *, pull_request=False):
    errors = []
    code = "invalid_pr_content" if pull_request else "invalid_issue_content"
    label = "pull request" if pull_request else "issue"

    def error(path, message):
        errors.append({"code": code, "path": path, "message": message})

    if not isinstance(content, dict):
        raise RuntimeFailure(code, f"Supply the {label}-facing content object.")
    for name in content.keys() - {
        "title",
        "body",
        "design_proposal_url",
        "comments",
        "document_attachments",
        "native_associations",
    }:
        error(
            name,
            f"Use the declared {label}-facing content fields; retain other metadata outside this envelope.",
        )
    for name in ("title", "body"):
        if not isinstance(content.get(name), str) or not content[name].strip():
            error(name, f"Supply substantive {label} text that stands on its own.")
    proposal = content.get("design_proposal_url")
    allowed = None
    if proposal is not None:
        try:
            parts = urlsplit(proposal) if isinstance(proposal, str) else None
            if (
                not parts
                or parts.scheme != "https"
                or not parts.netloc
                or parts.username
                or parts.password
            ):
                raise ValueError()
            allowed = normalized_url(proposal)
        except ValueError:
            error(
                "design_proposal_url",
                "Identify the actual design proposal with its HTTPS URL, or use null.",
            )
    native_urls = set()
    associations = content.get("native_associations", [])
    if not isinstance(associations, list):
        error("native_associations", "Supply native provider associations as kind and HTTPS URL objects.")
    else:
        for i, association in enumerate(associations):
            location = f"native_associations[{i}]"
            if (
                not isinstance(association, dict)
                or set(association) != {"kind", "url"}
                or association.get("kind") not in ("issue", "pull_request", "commit", "diff", "ci")
            ):
                error(location, "Identify the native issue, pull_request, commit, diff, or ci association.")
                continue
            url = association.get("url")
            try:
                parts = urlsplit(url) if isinstance(url, str) else None
                if not parts or parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
                    raise ValueError()
                native_urls.add(normalized_url(url))
            except ValueError:
                error(location + ".url", "Supply the association's credential-free HTTPS URL.")
    texts = [(name, content.get(name, "")) for name in ("title", "body")]
    comments = content.get("comments", [])
    if not isinstance(comments, list) or any(not isinstance(c, str) for c in comments):
        error(
            "comments", "Supply the workflow-authored comments as an array of strings."
        )
    else:
        texts.extend((f"comments[{i}]", c) for i, c in enumerate(comments))
    attachments = content.get("document_attachments", [])
    if not isinstance(attachments, list):
        error(
            "document_attachments",
            "Supply document attachments as an array of title and URL objects.",
        )
    else:
        for i, attachment in enumerate(attachments):
            path = f"document_attachments[{i}]"
            if (
                not isinstance(attachment, dict)
                or not isinstance(attachment.get("url"), str)
                or not isinstance(attachment.get("title"), str)
                or set(attachment) != {"title", "url"}
            ):
                error(path, "Supply the document title and URL.")
                continue
            try:
                matches = allowed and normalized_url(attachment["url"]) == allowed
            except ValueError:
                matches = False
            if not matches:
                error(
                    path,
                    f"The design proposal is the only document that may be attached to a {label}.",
                )
            texts.append((path + ".title", attachment.get("title", "")))
    for path, text in texts:
        if not isinstance(text, str):
            error(path, f"Use text for {label}-facing prose.")
            continue
        for url in references(text, literal_examples=pull_request):
            try:
                permitted = (
                    normalized_url(url) == allowed
                    or normalized_url(url) in native_urls
                    or operational_link(url, pull_request)
                    or url.startswith("#")
                )
            except ValueError:
                permitted = False
            if not permitted:
                error(
                    path,
                    f"Move the document reference {url!r} into the design proposal.",
                )
    if errors:
        raise RuntimeFailure(
            code,
            f"The {label} content violates the shared writing contract.",
            errors,
        )
    return {
        "policy": (
            "self-contained-pr-design-proposal-only-v1" if pull_request else POLICY
        ),
        "reference_check": "passed",
        "editorial_review": "required",
    }


def plan_content(issue):
    return {
        key: issue[key]
        for key in (
            "title",
            "body",
            "design_proposal_url",
            "comments",
            "document_attachments",
            "native_associations",
        )
        if key in issue
    }
