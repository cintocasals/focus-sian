#!/usr/bin/env python3
"""Focus & {S} · acta builder.

Reads a debate folder (meta.json + the phase files) and writes:
  acta.html          standalone page (open it in any browser)
  acta.md            the whole record as one Markdown file
  acta-artifact.html same page without the document skeleton (for hosts that wrap pages), only with --artifact

Usage: python3 build_acta.py <debate folder> [--artifact]
No dependencies beyond the Python 3 standard library.
"""
import html
import json
import os
import re
import sys
from datetime import datetime

# ---------------------------------------------------------------- labels

LABELS = {
    "ca": {
        "eyebrow": "Acta del consell · Focus & {S}",
        "project": "Projecte", "date": "Data", "lang": "Idioma", "mode": "Mode", "status": "Estat",
        "version": "Versió", "open": "Desacords oberts", "signatures": "Signatures",
        "mode_subagents": "Dos agents independents", "mode_single": "Un sol context",
        "single_notice": "Aquest debat s'ha fet en un sol context: les dues estratègies no s'han escrit de manera independent.",
        "status_in-debate": "En debat", "status_awaiting-approval": "Pendent d'aprovació",
        "status_approved": "Aprovada", "status_prompt-delivered": "Prompt lliurat",
        "route": "Full de ruta", "route_note": "Com han arribat a la conclusió, fase per fase.",
        "p0": "Plantejament", "p1": "Preguntes", "p2": "Estratègies", "p3": "Crítica creuada",
        "p4": "Rèplica", "p5": "Estratègia conjunta", "p6": "Aprovació", "p7": "Prompt d'execució",
        "brief": "El plantejament", "context": "Dossier de context", "questions": "Preguntes prèvies",
        "focus": "Focus", "second": "{S}", "focus_sub": "mètode Jobs", "second_sub": "mètode Ohno",
        "critique_by_focus": "Focus critica {S}", "critique_by_second": "{S} critica Focus",
        "rebuttal": "Rèplica i posició revisada", "draft": "Esborrany del moderador",
        "signoff": "Signatura", "final": "Estratègia conjunta", "approval": "Decisió del promotor",
        "prompt": "Prompt d'execució", "review": "Revisió del prompt", "copy": "Copia el prompt",
        "copied": "Copiat", "copy_fail": "Selecciona el text i copia'l a mà",
        "expand": "Obre-ho tot", "collapse": "Tanca-ho tot", "pending": "Pendent",
        "not_run": "No s'ha fet", "read_full": "Llegeix el text sencer", "changes": "Ronda de canvis",
        "previous": "Versió anterior",
        "disclaimer": "Focus i {S} són simulacions inspirades en els mètodes de Steve Jobs i Taiichi Ohno. No són ells i no parlen en nom seu.",
        "footer": "Focus & {S} · el consell de dos · Cinto Casals · SerIA Nativa",
        "generated": "Acta generada el",
    },
    "es": {
        "eyebrow": "Acta del consejo · Focus & {S}",
        "project": "Proyecto", "date": "Fecha", "lang": "Idioma", "mode": "Modo", "status": "Estado",
        "version": "Versión", "open": "Desacuerdos abiertos", "signatures": "Firmas",
        "mode_subagents": "Dos agentes independientes", "mode_single": "Un solo contexto",
        "single_notice": "Este debate se ha hecho en un solo contexto: las dos estrategias no se han escrito de forma independiente.",
        "status_in-debate": "En debate", "status_awaiting-approval": "Pendiente de aprobación",
        "status_approved": "Aprobada", "status_prompt-delivered": "Prompt entregado",
        "route": "Hoja de ruta", "route_note": "Cómo han llegado a la conclusión, fase por fase.",
        "p0": "Planteamiento", "p1": "Preguntas", "p2": "Estrategias", "p3": "Crítica cruzada",
        "p4": "Réplica", "p5": "Estrategia conjunta", "p6": "Aprobación", "p7": "Prompt de ejecución",
        "brief": "El planteamiento", "context": "Dossier de contexto", "questions": "Preguntas previas",
        "focus": "Focus", "second": "{S}", "focus_sub": "método Jobs", "second_sub": "método Ohno",
        "critique_by_focus": "Focus critica a {S}", "critique_by_second": "{S} critica a Focus",
        "rebuttal": "Réplica y posición revisada", "draft": "Borrador del moderador",
        "signoff": "Firma", "final": "Estrategia conjunta", "approval": "Decisión del promotor",
        "prompt": "Prompt de ejecución", "review": "Revisión del prompt", "copy": "Copiar el prompt",
        "copied": "Copiado", "copy_fail": "Selecciona el texto y cópialo a mano",
        "expand": "Abrirlo todo", "collapse": "Cerrarlo todo", "pending": "Pendiente",
        "not_run": "No se ha hecho", "read_full": "Leer el texto completo", "changes": "Ronda de cambios",
        "previous": "Versión anterior",
        "disclaimer": "Focus y {S} son simulaciones inspiradas en los métodos de Steve Jobs y Taiichi Ohno. No son ellos y no hablan en su nombre.",
        "footer": "Focus & {S} · el consejo de dos · Cinto Casals · SerIA Nativa",
        "generated": "Acta generada el",
    },
    "en": {
        "eyebrow": "Council minutes · Focus & {S}",
        "project": "Project", "date": "Date", "lang": "Language", "mode": "Mode", "status": "Status",
        "version": "Version", "open": "Open disagreements", "signatures": "Signatures",
        "mode_subagents": "Two independent agents", "mode_single": "Single context",
        "single_notice": "This debate ran in a single context: the two strategies were not written independently.",
        "status_in-debate": "In debate", "status_awaiting-approval": "Awaiting approval",
        "status_approved": "Approved", "status_prompt-delivered": "Prompt delivered",
        "route": "Route", "route_note": "How they reached the conclusion, phase by phase.",
        "p0": "Brief", "p1": "Questions", "p2": "Strategies", "p3": "Cross-critique",
        "p4": "Rebuttal", "p5": "Joint strategy", "p6": "Approval", "p7": "Execution prompt",
        "brief": "The brief", "context": "Context dossier", "questions": "Questions before analysing",
        "focus": "Focus", "second": "{S}", "focus_sub": "Jobs method", "second_sub": "Ohno method",
        "critique_by_focus": "Focus on {S}", "critique_by_second": "{S} on Focus",
        "rebuttal": "Rebuttal and revised position", "draft": "Moderator's draft",
        "signoff": "Sign-off", "final": "Joint strategy", "approval": "Owner's decision",
        "prompt": "Execution prompt", "review": "Prompt review", "copy": "Copy the prompt",
        "copied": "Copied", "copy_fail": "Select the text and copy it by hand",
        "expand": "Open all", "collapse": "Close all", "pending": "Pending",
        "not_run": "Not run", "read_full": "Read the full text", "changes": "Change round",
        "previous": "Previous version",
        "disclaimer": "Focus and {S} are simulations inspired by the methods of Steve Jobs and Taiichi Ohno. They are not those people and do not speak for them.",
        "footer": "Focus & {S} · the council of two · Cinto Casals · SerIA Nativa",
        "generated": "Minutes built on",
    },
}

# ---------------------------------------------------------------- markdown

def _inline(text):
    """Escape and render inline Markdown. Input is raw text."""
    codes = []

    def keep_code(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                  lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (m.group(2).replace('"', "%22"), m.group(1)),
                  text)
    text = re.sub(r"(?<![\w\"'>/])(https?://[^\s<)]+)",
                  lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (m.group(1), m.group(1)), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w])_(?!\s)(.+?)(?<!\s)_(?![\w])", r"<em>\1</em>", text)
    text = re.sub(r"\[(F\+G|F\+S|F|G|S)\](?!\()", lambda m: '<span class="tag tag-%s">%s</span>' % (
        {"F": "f", "G": "g", "S": "g", "F+G": "fg", "F+S": "fg"}[m.group(1)], m.group(1)), text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: "<code>%s</code>" % html.escape(codes[int(m.group(1))], quote=False), text)
    return text


def md_to_html(md, shift=0):
    """Small Markdown renderer: headings, paragraphs, lists (nested), quotes, tables, code, rules."""
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    para = []

    def flush_para():
        if para:
            out.append("<p>%s</p>" % _inline(" ".join(s.strip() for s in para)))
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_para()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append('<div class="scroll"><pre><code>%s</code></pre></div>' % html.escape("\n".join(buf), quote=False))
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para()
            level = min(6, len(m.group(1)) + shift)
            out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2).strip()), level))
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            flush_para()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>%s</blockquote>" % md_to_html("\n".join(buf), shift))
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            flush_para()
            def cells(row):
                row = row.strip()
                if row.startswith("|"):
                    row = row[1:]
                if row.endswith("|"):
                    row = row[:-1]
                return [c.strip() for c in row.split("|")]
            head = cells(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            t = ['<div class="scroll"><table><thead><tr>']
            t += ["<th>%s</th>" % _inline(c) for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in r))
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue

        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            flush_para()
            items = []
            while i < len(lines):
                l = lines[i]
                mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", l)
                if mm:
                    indent = len(mm.group(1).replace("\t", "    "))
                    items.append([indent, "ol" if mm.group(2)[0].isdigit() else "ul", mm.group(3)])
                    i += 1
                elif l.strip() and items and (l.startswith("  ") or l.startswith("\t")) and not l.strip().startswith(("|", "#", ">")):
                    items[-1][2] += " " + l.strip()
                    i += 1
                else:
                    break
            out.append(_render_list(items))
            continue

        para.append(line)
        i += 1

    flush_para()
    return "\n".join(out)


def _render_list(items):
    html_out = []
    stack = []  # (indent, tag)
    for indent, tag, text in items:
        while stack and indent < stack[-1][0]:
            html_out.append("</li></%s>" % stack.pop()[1])
        if not stack or indent > stack[-1][0]:
            stack.append((indent, tag))
            html_out.append("<%s><li>%s" % (tag, _inline(text)))
        else:
            html_out.append("</li><li>%s" % _inline(text))
    while stack:
        html_out.append("</li></%s>" % stack.pop()[1])
    return "".join(html_out)

# ---------------------------------------------------------------- page

CSS = r"""
/* Layout: a technical drawing sheet. Title block (cartouche) on top, a dimensioned rail of the eight
   phases, then the phases in order; the two advisors side by side; the joint strategy carries the
   only accent on the page. Identity: SerIA Nativa (bone white, ink, lead grey, oxide 5%). */
:root{
  --bg:#F4F2ED; --fg:#12161A; --muted:#5F666C; --line:#DCD9D2; --grid:#E8E5DE; --accent:#C1440E;
  --surface:#F9F8F4;
  --sans:"IBM Plex Sans","Helvetica Neue",Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0B0E11; --fg:#ECE9E2; --muted:#9AA1A6; --line:#2B3036; --grid:#15191D; --accent:#E2672F;
  --surface:#10141A; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0B0E11; --fg:#ECE9E2; --muted:#9AA1A6; --line:#2B3036; --grid:#15191D; --accent:#E2672F;
  --surface:#10141A; color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:17px;line-height:1.6;
  -webkit-font-smoothing:antialiased;
  background-image:linear-gradient(to right,var(--grid) 1px,transparent 1px),linear-gradient(to bottom,var(--grid) 1px,transparent 1px);
  background-size:52px 52px}
.w{max-width:1180px;margin:0 auto;padding-inline:clamp(16px,4vw,48px);padding-block:40px 64px}
.mono,.label{font-family:var(--mono);text-transform:uppercase;letter-spacing:.14em;font-size:12px;font-weight:500;color:var(--muted)}
h1{font-size:clamp(34px,5.2vw,64px);line-height:1;font-weight:600;letter-spacing:-.02em;margin:12px 0 0;text-wrap:balance}
a{color:inherit;text-underline-offset:3px}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--fg);outline-offset:3px}

/* title block */
.cartouche{margin-top:32px;display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));border:1px solid var(--fg);background:var(--bg)}
.cartouche>div{padding:10px 14px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);min-width:0}
.cartouche .v{font-family:var(--mono);font-size:14px;font-weight:600;font-variant-numeric:tabular-nums;margin-top:2px;overflow-wrap:anywhere}
.cartouche .wide{grid-column:1/-1}
.cartouche .sig{display:flex;gap:24px;flex-wrap:wrap}
.cartouche .sig span{font-family:var(--mono);font-size:13px}
.disclaimer{margin-top:14px;font-size:14px;color:var(--muted);max-width:75ch}
.notice{margin-top:14px;padding:10px 14px;border:1px dashed var(--fg);font-size:15px}

/* rail */
.rail{margin-top:40px;overflow-x:auto}
.rail ol{list-style:none;margin:0;padding:18px 0 0;display:grid;grid-template-columns:repeat(8,minmax(92px,1fr));position:relative;min-width:736px}
.rail ol::before{content:"";position:absolute;left:0;right:0;top:24px;height:1px;background:var(--fg)}
.rail li{position:relative;padding-top:22px}
.rail li::before{content:"";position:absolute;left:0;top:0;width:1px;height:13px;background:var(--fg)}
.rail li .n{font-family:var(--mono);font-size:14px;font-weight:600;font-variant-numeric:tabular-nums}
.rail li .t{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);display:block;line-height:1.35;margin-top:2px}
.rail li.todo .n{color:var(--muted)}
.rail li.todo::before{background:var(--muted)}
.rail li a{text-decoration:none}

/* route table */
.route{margin-top:48px}
.route h2,.phase h2{font-size:clamp(24px,3vw,34px);line-height:1.1;font-weight:600;margin:0;text-wrap:balance}
.route .note{color:var(--muted);margin:6px 0 16px}
.route table{width:100%;border-collapse:collapse;font-size:15px}
.route th,.route td{text-align:left;vertical-align:top;border-top:1px solid var(--line);padding:10px 12px 10px 0}
.route th{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:500;white-space:nowrap}
.route td.who{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap}

/* phases */
.phase{margin-top:72px;scroll-margin-top:24px}
.phase-head{display:flex;gap:18px;align-items:baseline;border-bottom:1px solid var(--fg);padding-bottom:10px}
.phase-head .n{font-family:var(--mono);font-size:14px;font-weight:600;font-variant-numeric:tabular-nums}
.digest{color:var(--muted);margin:12px 0 0;max-width:80ch}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:24px}
.cols>*{min-width:0}
@media (max-width:820px){.cols{grid-template-columns:1fr}}
.doc{border-top:1px solid var(--line);padding-top:14px}
.who{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.who b{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase}
.who i{font-style:normal;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.gloss{margin:8px 0 0;font-size:15px}
.single{margin-top:24px}
details{margin-top:10px}
summary{cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);list-style:none;padding:6px 0}
summary::-webkit-details-marker{display:none}
summary::before{content:"+ ";}
details[open]>summary::before{content:"− ";}
.body{font-size:16px;max-width:75ch}
.body h1,.body h2,.body h3,.body h4,.body h5,.body h6{line-height:1.25;margin:1.4em 0 .4em;text-wrap:balance}
.body h3{font-size:21px;font-weight:600}
.body h4{font-size:17px;font-weight:600}
.body h5,.body h6{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:600}
.body p{margin:.6em 0}
.body ul,.body ol{padding-left:1.3em;margin:.5em 0}
.body li{margin:.2em 0}
.body blockquote{margin:1em 0;padding:2px 0 2px 16px;border-left:1px solid var(--fg)}
.body hr{border:0;border-top:1px solid var(--line);margin:1.6em 0}
.body code{font-family:var(--mono);font-size:.88em;background:var(--surface);padding:1px 4px}
.body pre{background:var(--surface);border:1px solid var(--line);padding:14px;font-size:13px;line-height:1.5;margin:0}
.body pre code{background:none;padding:0}
.scroll{overflow-x:auto;margin:1em 0}
.body table{border-collapse:collapse;font-size:14px;min-width:100%}
.body th,.body td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
.body th{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:600}
.tag{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.06em;border:1px solid var(--fg);padding:0 5px;white-space:nowrap}
.tag-fg{background:var(--fg);color:var(--bg)}

/* the conclusion: the one accent on the page */
.final{margin-top:28px;border-left:3px solid var(--accent);padding:4px 0 4px clamp(16px,3vw,32px)}
.final .label{color:var(--accent)}
.final .body{max-width:80ch}

.prompt-bar{display:flex;gap:12px;align-items:center;margin-top:20px;flex-wrap:wrap}
button{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;background:var(--fg);color:var(--bg);border:0;padding:10px 16px;cursor:pointer}
button.ghost{background:transparent;color:var(--fg);box-shadow:inset 0 0 0 1px var(--fg)}
.toolbar{display:flex;justify-content:flex-end;margin-top:24px}
.empty{color:var(--muted);font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-top:18px}
footer{margin-top:96px;border-top:1px solid var(--fg);padding-top:14px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
"""

JS = r"""
(function(){
  var btn=document.getElementById('toggleAll');
  if(btn){btn.addEventListener('click',function(){
    var ds=[].slice.call(document.querySelectorAll('main details'));
    var anyClosed=ds.some(function(d){return !d.open});
    ds.forEach(function(d){d.open=anyClosed});
    btn.textContent=anyClosed?btn.dataset.collapse:btn.dataset.expand;
  });}
  var cp=document.getElementById('copyPrompt');
  if(cp){cp.addEventListener('click',function(){
    var raw=document.getElementById('promptRaw');
    var text=raw?JSON.parse(raw.textContent):'';
    var done=function(msg){var s=document.getElementById('copyState');if(s){s.textContent=msg;}};
    try{
      navigator.clipboard.writeText(text).then(function(){done(cp.dataset.ok)},function(){fallback()});
    }catch(e){fallback()}
    function fallback(){
      var box=document.getElementById('promptBody');
      if(box){var r=document.createRange();r.selectNodeContents(box);var sel=window.getSelection();sel.removeAllRanges();sel.addRange(r);}
      done(cp.dataset.fail);
    }
  });}
})();
"""


def read(d, name):
    p = os.path.join(d, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return f.read()
    return None


def esc(s):
    return html.escape(s or "", quote=True)


def doc_block(L, text, who=None, sub=None, gloss=None, open_=False, summary=None):
    if text is None:
        return '<div class="doc"><div class="empty">%s</div></div>' % esc(L["pending"])
    head = ""
    if who:
        head = '<div class="who"><b>%s</b>%s</div>' % (esc(who), ("<i>%s</i>" % esc(sub)) if sub else "")
    g = '<p class="gloss">%s</p>' % _inline(gloss) if gloss else ""
    body = '<div class="body">%s</div>' % md_to_html(text, shift=2)
    return ('<div class="doc">%s%s<details%s><summary>%s</summary>%s</details></div>'
            % (head, g, " open" if open_ else "", esc(summary or L["read_full"]), body))


def build(d, artifact=False):
    meta_raw = read(d, "meta.json")
    meta = json.loads(meta_raw) if meta_raw else {}
    lang = (meta.get("lang") or "en").split("-")[0].lower()
    S = meta.get("summaries", {}) or {}
    legacy = (os.path.exists(os.path.join(d, "02-strategy-gemba.md")) or any(k.endswith("-gemba") for k in S)) \
        and not os.path.exists(os.path.join(d, "02-strategy-sian.md"))
    second = "gemba" if legacy else "sian"
    SN = "Gemba" if legacy else "Sian"
    L = {k: v.replace("{S}", SN) for k, v in LABELS.get(lang, LABELS["en"]).items()}
    title = meta.get("title") or os.path.basename(os.path.abspath(d))
    status = meta.get("status", "in-debate")
    mode = meta.get("mode", "subagents")

    f = {n: read(d, n) for n in [
        "00-brief.md", "00-context.md", "01-questions.md",
        "02-strategy-focus.md", "02-strategy-" + second + ".md",
        "03-critique-by-focus.md", "03-critique-by-" + second + ".md",
        "04-rebuttal-focus.md", "04-rebuttal-" + second + ".md",
        "05-draft-joint.md", "05-signoff-focus.md", "05-signoff-" + second + ".md", "05-joint-strategy.md",
        "06-approval.md", "07-execution-prompt.md", "07-review-focus.md", "07-review-" + second + ".md"]}

    extra = sorted(n for n in os.listdir(d) if re.match(r"^(0[3-5]b-.*|05-joint-strategy-v\d+|06-change-.*)\.md$", n))

    done = {
        0: f["00-brief.md"] is not None,
        1: f["01-questions.md"] is not None and not meta.get("questions_skipped"),
        2: f["02-strategy-focus.md"] is not None or f["02-strategy-" + second + ".md"] is not None,
        3: f["03-critique-by-focus.md"] is not None or f["03-critique-by-" + second + ".md"] is not None,
        4: f["04-rebuttal-focus.md"] is not None or f["04-rebuttal-" + second + ".md"] is not None,
        5: f["05-joint-strategy.md"] is not None,
        6: f["06-approval.md"] is not None,
        7: f["07-execution-prompt.md"] is not None,
    }
    names = [L["p%d" % k] for k in range(8)]

    # ---- header
    created = meta.get("created", "")
    sig = '<span>%s · %s</span><span>%s · %s</span>' % (
        esc(L["focus"]), esc(S.get("5-focus", L["pending"]).split(".")[0][:60]),
        esc(L["second"]), esc(S.get("5-" + second, L["pending"]).split(".")[0][:60]))
    cart = [
        '<div class="wide"><div class="label">%s</div><div class="v">%s</div></div>' % (esc(L["project"]), esc(title)),
        '<div><div class="label">%s</div><div class="v">%s</div></div>' % (esc(L["date"]), esc(created)),
        '<div><div class="label">%s</div><div class="v">%s</div></div>' % (esc(L["status"]), esc(L.get("status_" + status, status))),
        '<div><div class="label">%s</div><div class="v">v%s</div></div>' % (esc(L["version"]), esc(str(meta.get("version", 1)))),
        '<div><div class="label">%s</div><div class="v">%s</div></div>' % (esc(L["mode"]), esc(L["mode_single"] if mode == "single-context" else L["mode_subagents"])),
        '<div><div class="label">%s</div><div class="v">%s</div></div>' % (esc(L["open"]), esc(str(meta.get("open_disagreements", "-")))),
        '<div><div class="label">%s</div><div class="v">%s</div></div>' % (esc(L["lang"]), esc(lang.upper())),
        '<div class="wide"><div class="label">%s</div><div class="v sig">%s</div></div>' % (esc(L["signatures"]), sig),
    ]
    header = ('<header><div class="label">%s</div><h1>%s</h1>%s<div class="cartouche">%s</div>'
              '<p class="disclaimer">%s</p>%s</header>') % (
        esc(L["eyebrow"]), esc(title),
        ('<p class="digest">%s</p>' % _inline(meta["brief_summary"])) if meta.get("brief_summary") else "",
        "".join(cart), esc(L["disclaimer"]),
        ('<p class="notice">%s</p>' % esc(L["single_notice"])) if mode == "single-context" else "")

    # ---- rail
    rail = ['<nav class="rail" aria-label="%s"><ol>' % esc(L["route"])]
    for k in range(8):
        rail.append('<li class="%s"><a href="#f%d"><span class="n">0%d</span><span class="t">%s</span></a></li>'
                    % ("done" if done[k] else "todo", k, k, esc(names[k])))
    rail.append("</ol></nav>")

    # ---- route table
    rows = []
    def row(k, who, key):
        if S.get(key):
            rows.append('<tr><th>0%d · %s</th><td class="who">%s</td><td>%s</td></tr>' % (k, esc(names[k]), esc(who), _inline(S[key])))
    for k in (2, 3, 4, 5):
        row(k, L["focus"], "%d-focus" % k)
        row(k, L["second"], "%d-%s" % (k, second))
    if S.get("5-joint"):
        rows.append('<tr><th>05 · %s</th><td class="who">F + G</td><td><strong>%s</strong></td></tr>' % (esc(names[5]), _inline(S["5-joint"])))
    for k in (6, 7):
        if S.get(str(k)):
            rows.append('<tr><th>0%d · %s</th><td class="who">&nbsp;</td><td>%s</td></tr>' % (k, esc(names[k]), _inline(S[str(k)])))
    route = ""
    if rows:
        route = ('<section class="route"><h2>%s</h2><p class="note">%s</p><div class="scroll"><table>%s</table></div></section>'
                 % (esc(L["route"]), esc(L["route_note"]), "".join(rows)))

    # ---- phases
    P = []
    def phase(k, inner, digest=None):
        P.append('<section class="phase" id="f%d"><div class="phase-head"><span class="n">0%d</span><h2>%s</h2></div>%s%s</section>'
                 % (k, k, esc(names[k]), ('<p class="digest">%s</p>' % _inline(digest)) if digest else "", inner))

    phase(0, '<div class="single">%s%s</div>' % (
        doc_block(L, f["00-brief.md"], L["brief"], open_=True),
        doc_block(L, f["00-context.md"], L["context"]) if f["00-context.md"] else ""))
    phase(1, '<div class="single">%s</div>' % (doc_block(L, f["01-questions.md"], L["questions"], open_=True)
                                               if f["01-questions.md"] else '<div class="empty">%s</div>' % esc(L["not_run"])))
    phase(2, '<div class="cols">%s%s</div>' % (
        doc_block(L, f["02-strategy-focus.md"], L["focus"], L["focus_sub"], S.get("2-focus"), open_=True),
        doc_block(L, f["02-strategy-" + second + ".md"], L["second"], L["second_sub"], S.get("2-" + second), open_=True)))
    phase(3, '<div class="cols">%s%s</div>' % (
        doc_block(L, f["03-critique-by-focus.md"], L["critique_by_focus"], L["focus_sub"], S.get("3-focus")),
        doc_block(L, f["03-critique-by-" + second + ".md"], L["critique_by_second"], L["second_sub"], S.get("3-" + second))))
    phase(4, '<div class="cols">%s%s</div>' % (
        doc_block(L, f["04-rebuttal-focus.md"], L["focus"], L["rebuttal"], S.get("4-focus")),
        doc_block(L, f["04-rebuttal-" + second + ".md"], L["second"], L["rebuttal"], S.get("4-" + second))))
    extra3 = [n for n in extra if n.startswith(("03b-", "04b-", "05b-"))]
    inner5 = ""
    if extra3:
        inner5 += '<div class="single">%s</div>' % "".join(doc_block(L, read(d, n), n) for n in extra3)
    inner5 += '<div class="single">%s</div>' % doc_block(L, f["05-draft-joint.md"], L["draft"])
    inner5 += '<div class="cols">%s%s</div>' % (
        doc_block(L, f["05-signoff-focus.md"], L["focus"], L["signoff"], S.get("5-focus")),
        doc_block(L, f["05-signoff-" + second + ".md"], L["second"], L["signoff"], S.get("5-" + second)))
    if f["05-joint-strategy.md"]:
        inner5 += ('<div class="final"><div class="label">%s · v%s</div><div class="body">%s</div></div>'
                   % (esc(L["final"]), esc(str(meta.get("version", 1))), md_to_html(f["05-joint-strategy.md"], shift=2)))
    prev = [n for n in extra if n.startswith("05-joint-strategy-v")]
    for n in prev:
        inner5 += '<div class="single">%s</div>' % doc_block(L, read(d, n), L["previous"] + " · " + n[18:-3])
    phase(5, inner5, S.get("5-joint"))

    inner6 = '<div class="single">%s</div>' % doc_block(L, f["06-approval.md"], L["approval"], open_=True) if f["06-approval.md"] else '<div class="empty">%s</div>' % esc(L["pending"])
    for n in [x for x in extra if x.startswith("06-change-")]:
        inner6 += '<div class="single">%s</div>' % doc_block(L, read(d, n), L["changes"] + " · " + n[10:-3])
    phase(6, inner6, S.get("6"))

    if f["07-execution-prompt.md"]:
        raw = json.dumps(f["07-execution-prompt.md"]).replace("</", "<\\/")
        inner7 = ('<div class="prompt-bar"><button id="copyPrompt" data-ok="%s" data-fail="%s">%s</button>'
                  '<span id="copyState" class="mono" aria-live="polite"></span></div>'
                  '<script type="application/json" id="promptRaw">%s</script>'
                  '<div class="single"><div class="body" id="promptBody">%s</div></div>'
                  '<div class="cols">%s%s</div>') % (
            esc(L["copied"]), esc(L["copy_fail"]), esc(L["copy"]), raw,
            md_to_html(f["07-execution-prompt.md"], shift=2),
            doc_block(L, f["07-review-focus.md"], L["focus"], L["review"]),
            doc_block(L, f["07-review-" + second + ".md"], L["second"], L["review"]))
    else:
        inner7 = '<div class="empty">%s</div>' % esc(L["pending"])
    phase(7, inner7, S.get("7"))

    toolbar = ('<div class="toolbar"><button class="ghost" id="toggleAll" data-expand="%s" data-collapse="%s">%s</button></div>'
               % (esc(L["expand"]), esc(L["collapse"]), esc(L["expand"])))
    footer = '<footer><span class="label">%s</span><span class="label">%s %s</span></footer>' % (
        esc(L["footer"]), esc(L["generated"]), datetime.now().strftime("%Y-%m-%d %H:%M"))

    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;600&display=swap">')
    content = '<div class="w">%s%s%s%s<main>%s</main>%s</div><script>%s</script>' % (
        header, "".join(rail), route, toolbar, "".join(P), footer, JS)
    head = '<title>%s</title>%s<style>%s</style>' % (esc(title), fonts, CSS)

    page = ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">%s</head><body>%s</body></html>'
            % (lang, head, content))
    with open(os.path.join(d, "acta.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    if artifact:
        with open(os.path.join(d, "acta-artifact.html"), "w", encoding="utf-8") as fh:
            fh.write(head + content)

    # ---- acta.md
    md = ["# %s" % title, "", "> %s" % L["eyebrow"], ">", "> %s · %s · %s" % (created, L.get("status_" + status, status),
          L["mode_single"] if mode == "single-context" else L["mode_subagents"]), ">", "> %s" % L["disclaimer"], ""]
    order = [("00", L["brief"], "00-brief.md"), ("00", L["context"], "00-context.md"), ("01", L["questions"], "01-questions.md"),
             ("02", "%s · %s" % (L["p2"], L["focus"]), "02-strategy-focus.md"), ("02", "%s · %s" % (L["p2"], L["second"]), "02-strategy-" + second + ".md"),
             ("03", L["critique_by_focus"], "03-critique-by-focus.md"), ("03", L["critique_by_second"], "03-critique-by-" + second + ".md"),
             ("04", "%s · %s" % (L["p4"], L["focus"]), "04-rebuttal-focus.md"), ("04", "%s · %s" % (L["p4"], L["second"]), "04-rebuttal-" + second + ".md"),
             ("05", L["draft"], "05-draft-joint.md"), ("05", "%s · %s" % (L["signoff"], L["focus"]), "05-signoff-focus.md"),
             ("05", "%s · %s" % (L["signoff"], L["second"]), "05-signoff-" + second + ".md"), ("05", L["final"], "05-joint-strategy.md"),
             ("06", L["approval"], "06-approval.md"), ("07", L["prompt"], "07-execution-prompt.md"),
             ("07", "%s · %s" % (L["review"], L["focus"]), "07-review-focus.md"), ("07", "%s · %s" % (L["review"], L["second"]), "07-review-" + second + ".md")]
    # extra rounds (re-debate, previous versions, change rounds) go right after their phase
    after = {"05-draft-joint.md": [n for n in extra if n.startswith(("03b-", "04b-", "05b-"))],
             "05-joint-strategy.md": [n for n in extra if n.startswith("05-joint-strategy-v")],
             "06-approval.md": [n for n in extra if n.startswith("06-change-")]}
    for num, name, fn in order:
        if f.get(fn):
            md += ["", "---", "", "## %s · %s" % (num, name), "", f[fn].strip(), ""]
        for n in after.get(fn, []):
            md += ["", "---", "", "## %s · %s" % (n[:2], n[:-3]), "", (read(d, n) or "").strip(), ""]
    with open(os.path.join(d, "acta.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    return os.path.join(d, "acta.html")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    path = build(args[0], artifact="--artifact" in sys.argv)
    print(path)
