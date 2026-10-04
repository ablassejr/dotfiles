"""Report projections from validated evidence artifacts."""

import html

from .storage import write


def display(value):
    return "Unknown" if value is None else str(value)


def surface_svg(result):
    surfaces = result.get("conceptual_surface", [])
    if not surfaces and result.get("plan"):
        surfaces = [{"candidate_id": card["candidate_id"], "vector": {
            name: {"before": len(v["before"]), "after": len(v["after"])}
            for name, v in card["surface"].items()}}
            for card in result["plan"]["assessment"]["candidates"] if card["disposition"] != "REJECTED"]
    height = 128 + sum(58 + 34 * len(x["vector"]) for x in surfaces)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Declared conceptual surface</title>',
           '<desc id="desc">Before and after counts for each conceptual dimension. These are analyst declarations.</desc>',
           f'<rect width="900" height="{height}" rx="16" fill="#eef2f1"/>',
           '<g font-family="system-ui,sans-serif" fill="#183c43">',
           '<text x="28" y="40" font-size="23" font-weight="700">Declared conceptual surface</text>',
           '<text x="28" y="68" font-size="14">Each dimension stands on its own. Counts do not establish preservation.</text>']
    y = 108
    if not surfaces:
        svg.append('<text x="28" y="108" font-size="16">No target surface has been characterized.</text>')
    for surface in surfaces:
        svg.append(f'<text x="28" y="{y}" font-size="16" font-weight="600">{html.escape(surface["candidate_id"])}</text>')
        y += 32
        peak = max([1, *[max(v["before"], v["after"]) for v in surface["vector"].values()]])
        for name, value in surface["vector"].items():
            svg.append(f'<text x="28" y="{y + 8}" font-size="14">{html.escape(name.replace("_", " "))}</text>')
            for offset, key, color in ((0, "before", "#90a5aa"), (10, "after", "#087e78")):
                svg.append(f'<rect x="265" y="{y - 8 + offset}" width="{400 * value[key] / peak:.1f}" height="8" rx="3" fill="{color}"/>')
            svg.append(f'<text x="700" y="{y + 8}" font-size="14">{value["before"]} before / {value["after"]} after</text>')
            y += 34
        y += 26
    return "".join([*svg, "</g></svg>"])


def render(run, result):
    write(run, "result.json", result)
    mass = result.get("code_mass", {})
    esc = lambda x: html.escape(display(x), quote=True)
    keys = ("before", "after", "net", "added", "removed", "ratio", "ratio_kind", "ratio_status", "validated_removal_credit")
    lines = ["# Local simplification", "", "**" + result["verdict"] + "**", "",
             "Run: `" + str(result.get("run_id", "unavailable")) + "`", "",
             "This is a local advisory result. Semantic declarations and actual check execution are reported separately.", "",
             "## Maintained code", "", "| Measure | Value |", "|---|---:|",
             *[f"| {key} | {display(mass.get(key))} |" for key in keys], ""]
    body = [f'<p class="eyebrow">LOCAL SIMPLIFICATION / {esc(result.get("stage", "EVIDENCE CHECK"))}</p>',
            f'<h1>{esc(result["verdict"])}</h1>',
            '<p>Required behavior, maintained code, and conceptual ownership are evaluated together.</p>',
            f'<p class="meta">{esc(result.get("run_id", "Run identity unavailable"))}</p>',
            '<h2>Maintained code</h2><table><thead><tr><th>Measure</th><th>Value</th></tr></thead><tbody>',
            *[f'<tr><td>{esc(key.replace("_", " "))}</td><td>{esc(mass.get(key))}</td></tr>' for key in keys], '</tbody></table>']
    if result.get("historical_only"):
        notice = "The measurements and logs describe the captured snapshots only. Current evidence validation failed; no current removal credit is assigned."
        lines[6:6] = [notice, ""]
        body.insert(3, '<p><strong>' + notice + '</strong></p>')
    if result.get("ratio_exception"):
        explanation = result["ratio_exception"]["reason"]
        lines.extend(["## Declared ratio exception", "", explanation, ""])
        body.append('<h2>Declared ratio exception</h2><p>' + esc(explanation) + '</p>')
    for title, key in (("Failures", "failures"), ("Remaining evidence", "gaps")):
        if result.get(key):
            lines.extend(["## " + title, "", *["- " + str(x) for x in result[key]], ""])
            body.append(f'<h2>{title}</h2><ul>' + "".join(f'<li>{esc(x)}</li>' for x in result[key]) + '</ul>')
    cards = result.get("responsibilities", [])
    if result.get("plan"):
        cards = [card for card in result["plan"]["assessment"]["candidates"] if card["disposition"] != "REJECTED"]
    if cards:
        lines.extend(["## Responsibility transitions", ""])
        body.append('<h2>Responsibility transitions</h2>')
        for card in cards:
            text = card["responsibility"] or "Responsibility remains uncharacterized"
            lines.extend(["### " + text, "", "Canonical owner: `" + card["target_owner"] + "`", "",
                          "Mechanisms to remove: " + ", ".join(card["remove"]), "", card["rationale"], "",
                          "Rollback: " + card["rollback"], ""])
            body.append(f'<article><h3>{esc(text)}</h3><p>Canonical owner: <code>{esc(card["target_owner"])}</code></p>'
                        f'<p>Mechanisms to remove: {esc(", ".join(card["remove"]))}</p><p>{esc(card["rationale"])}</p>'
                        f'<p><strong>Rollback:</strong> {esc(card["rollback"])}</p></article>')
    if result.get("checks"):
        lines.extend(["## Executed checks", "", "| Check | Snapshot | Result |", "|---|---|---|",
                      *[f"| {x['check_id']} | {x['side']} | {x['status']} |" for x in result["checks"]], ""])
        body.append('<h2>Executed checks</h2>')
        for check in result["checks"]:
            body.append(f'<details><summary>{esc(check["check_id"])} / {esc(check["side"])}: {esc(check["status"])}</summary>'
                        f'<pre>{esc(check.get("log", check.get("reason", "No log")))}</pre></details>')
    svg = surface_svg(result)
    write(run, "responsibility-map.svg", svg.encode(), raw=True)
    body.extend(['<h2>Conceptual surface</h2>', svg,
                 '<p class="meta">Analyst declarations and executed checks have different evidentiary roles. '
                 'A local pass applies to the declared, exercised contract and does not establish CI or deployment status.</p>'])
    for surface in result.get("conceptual_surface", []):
        lines.extend(["## Conceptual surface: " + surface["candidate_id"], "",
                      "Declared by the analyst; no aggregate complexity score is inferred.", "",
                      *[f"- {name}: {v['before']} before / {v['after']} after" for name, v in surface["vector"].items()], ""])
    write(run, "simplification-report.md", ("\n".join(lines) + "\n").encode(), raw=True)
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Local simplification</title><style>
body{margin:3rem auto;max-width:68rem;padding:0 2rem;background:#faf9f5;color:#183c43;font:16px/1.65 system-ui}
h1{font-size:3.5rem;line-height:1.1;margin:.4rem 0}h2{margin-top:2.5rem}h3{margin-top:0}
.eyebrow{font-size:.78rem;letter-spacing:.14em;font-weight:700}.meta{font-size:.85rem;overflow-wrap:anywhere;color:#586f73}
table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:.6rem 1rem;border-bottom:1px solid #d9e1dc}th{background:#eef2f1}
article{background:white;border:1px solid #d9e1dc;border-radius:12px;padding:1.3rem;margin:1rem 0}
code,pre{overflow-wrap:anywhere;white-space:pre-wrap}details{border-bottom:1px solid #d9e1dc;padding:.6rem 0}
summary{cursor:pointer}svg{width:100%;height:auto}li{margin:.45rem 0}
</style><body>''' + "".join(body) + '</body></html>'
    write(run, "simplification-report.html", page.encode(), raw=True)
