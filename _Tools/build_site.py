from __future__ import annotations

import html
import re
from collections import deque
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_HTML = ROOT_DIR / "docs" / "index.html"
OUTPUT_README = ROOT_DIR / "docs" / "README.md"
START_DOC = Path("README.md")

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+\.md(?:#[^)]+)?)\)", re.IGNORECASE)
HTML_ATTR_URL_RE = re.compile(r"(?P<attr>\b(?:src|href)\s*=\s*)(?P<quote>[\"'])(?P<url>[^\"']+)(?P=quote)", re.IGNORECASE)


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("/")


def split_hash(target: str) -> str:
    return target.split("#", 1)[0]


def is_external_url(url: str) -> bool:
  return bool(re.match(r"^(?:[a-z]+:)?//|^(?:data:|mailto:|javascript:|#)", url.strip(), re.IGNORECASE))


def resolve_repo_path(current_doc: Path, target: str) -> str:
  cleaned = normalize_path(split_hash(target)).strip()
  if not cleaned:
    return normalize_path(str(current_doc))

  root_candidate = ROOT_DIR / cleaned
  if root_candidate.exists():
    return normalize_path(cleaned)

  resolved = (current_doc.parent / cleaned).resolve().relative_to(ROOT_DIR.resolve())
  return normalize_path(str(resolved))


def rewrite_markdown_html_tag_paths(markdown: str, current_doc: Path) -> str:
  def _replace(match: re.Match[str]) -> str:
    attr = match.group("attr")
    quote = match.group("quote")
    raw_url = match.group("url").strip()

    if not raw_url or is_external_url(raw_url):
      return match.group(0)

    hash_part = ""
    if "#" in raw_url:
      base, hash_suffix = raw_url.split("#", 1)
      raw_url = base
      hash_part = f"#{hash_suffix}"

    try:
      resolved = resolve_repo_path(current_doc, raw_url)
    except ValueError:
      return match.group(0)

    return f"{attr}{quote}../{resolved}{hash_part}{quote}"

  return HTML_ATTR_URL_RE.sub(_replace, markdown)


def resolve_markdown_path(current_doc: Path, target: str) -> Path:
    clean = normalize_path(split_hash(target)).strip()
    if not clean:
        return current_doc
    return (current_doc.parent / clean).resolve().relative_to(ROOT_DIR.resolve())


def discover_docs(start_doc: Path) -> dict[str, str]:
    docs: dict[str, str] = {}
    queue: deque[Path] = deque([start_doc])
    visited: set[str] = set()

    while queue:
        doc = queue.popleft()
        doc_key = normalize_path(str(doc))
        if doc_key in visited:
            continue
        visited.add(doc_key)

        full_path = ROOT_DIR / doc
        if not full_path.exists():
            continue

        markdown = full_path.read_text(encoding="utf-8", errors="replace")
        markdown = markdown.replace("\ufeff", "")
        markdown = markdown.replace("\ufffd", "—")
        markdown = rewrite_markdown_html_tag_paths(markdown, doc)
        docs[doc_key] = markdown

        for match in LINK_RE.finditer(markdown):
            raw_target = match.group(1).strip()
            if not raw_target:
                continue
            try:
                linked = resolve_markdown_path(doc, raw_target)
            except ValueError:
                continue
            linked_full = ROOT_DIR / linked
            if linked_full.exists() and linked_full.suffix.lower() == ".md":
                queue.append(linked)

    return docs


def markdown_script_tag(path: str, content: str) -> str:
    safe_content = content.replace("</script>", "<\\/script>")
    return f'  <script id="md-{html.escape(path)}" type="text/markdown">{safe_content}</script>'


def build_html(docs: dict[str, str]) -> str:
    scripts = "\n\n".join(markdown_script_tag(path, docs[path]) for path in sorted(docs.keys()))

    template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Public Docs</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f172a;
      --panel: #111827;
      --panel-2: #1f2937;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --accent: #60a5fa;
      --accent-2: #22d3ee;
      --border: #334155;
    }}

    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #f8fafc;
        --panel: #ffffff;
        --panel-2: #f1f5f9;
        --text: #0f172a;
        --muted: #475569;
        --accent: #2563eb;
        --accent-2: #0891b2;
        --border: #cbd5e1;
      }}
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: Inter, Segoe UI, Roboto, system-ui, -apple-system, sans-serif;
      background: radial-gradient(circle at 20% 0%, color-mix(in srgb, var(--accent) 18%, transparent), transparent 45%), var(--bg);
      color: var(--text);
      min-height: 100vh;
    }}

    .layout {{
      display: grid;
      grid-template-columns: 320px 1fr;
      min-height: 100vh;
    }}

    .sidebar {{
      border-right: 1px solid var(--border);
      background: color-mix(in srgb, var(--panel) 92%, transparent);
      backdrop-filter: blur(8px);
      padding: 1rem;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
    }}

    .brand {{
      margin: 0 0 0.25rem;
      font-size: 1.15rem;
      letter-spacing: 0.02em;
    }}

    .hint {{
      margin: 0 0 1rem;
      color: var(--muted);
      font-size: 0.9rem;
    }}

    .nav-list {{
      list-style: none;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }}

    .nav-link {{
      display: block;
      text-decoration: none;
      color: var(--text);
      border: 1px solid var(--border);
      background: var(--panel-2);
      border-radius: 10px;
      padding: 0.55rem 0.65rem;
      padding-left: calc(0.65rem + var(--level, 0) * 0.8rem);
      transition: 120ms ease;
      font-size: 0.95rem;
      overflow-wrap: anywhere;
    }}

    .nav-separator {{
      height: 1px;
      border: 0;
      background: color-mix(in srgb, var(--border) 80%, transparent);
      margin: 0.6rem 0.15rem 0.45rem;
    }}

    .nav-double-separator {{
      border: 0;
      border-top: 3px double color-mix(in srgb, var(--border) 85%, transparent);
      margin: 0.55rem 0.15rem 0.5rem;
    }}

    .nav-link:hover {{
      border-color: var(--accent);
      transform: translateY(-1px);
    }}

    .nav-link.active {{
      background: color-mix(in srgb, var(--accent) 18%, var(--panel-2));
      border-color: var(--accent);
      font-weight: 600;
    }}

    .nav-link.nav-home {{
      background: color-mix(in srgb, var(--accent-2) 20%, var(--panel-2));
      border-color: color-mix(in srgb, var(--accent-2) 60%, var(--border));
      color: var(--text);
      font-weight: 700;
    }}

    .nav-link.nav-home:hover {{
      border-color: var(--accent-2);
      background: color-mix(in srgb, var(--accent-2) 28%, var(--panel-2));
    }}

    .nav-link.nav-home.active {{
      border-color: var(--accent-2);
      background: color-mix(in srgb, var(--accent-2) 34%, var(--panel-2));
      box-shadow: 0 0 0 1px color-mix(in srgb, var(--accent-2) 45%, transparent) inset;
    }}

    .nav-link.itemized {{
      border: none;
      background: transparent;
      border-radius: 0;
      padding-top: 0.35rem;
      padding-bottom: 0.35rem;
      position: relative;
      color: color-mix(in srgb, var(--text) 88%, var(--muted));
    }}

    .nav-link.itemized::before {{
      content: "•";
      position: absolute;
      left: calc(0.25rem + var(--level, 1) * 0.8rem - 0.55rem);
      color: var(--muted);
      font-size: 0.95rem;
      line-height: 1;
      top: 50%;
      transform: translateY(-50%);
    }}

    .nav-link.itemized:hover {{
      border: none;
      transform: none;
      color: var(--accent);
      background: color-mix(in srgb, var(--accent) 10%, transparent);
      border-radius: 8px;
    }}

    .nav-link.itemized.active {{
      border: none;
      background: color-mix(in srgb, var(--accent) 14%, transparent);
      color: var(--accent);
      font-weight: 700;
    }}

    main {{
      padding: 1.5rem;
      min-width: 0;
    }}

    .content-shell {{
      width: min(1150px, 100%);
      margin: 0 auto;
      border: 1px solid var(--border);
      background: color-mix(in srgb, var(--panel) 95%, transparent);
      border-radius: 16px;
      padding: 1.5rem;
      box-shadow: 0 20px 45px color-mix(in srgb, var(--accent) 12%, transparent);
    }}

    .breadcrumbs {{
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 1rem;
      overflow-wrap: anywhere;
    }}

    .md-content h1, .md-content h2, .md-content h3 {{
      line-height: 1.2;
      margin-top: 1.35em;
      margin-bottom: 0.5em;
    }}

    .md-content h1 {{ font-size: 1.9rem; }}
    .md-content h2 {{ font-size: 1.45rem; }}

    .md-content p, .md-content li {{ line-height: 1.6; }}

    .md-content a {{
      color: var(--accent);
      text-decoration: none;
      border-bottom: 1px dashed color-mix(in srgb, var(--accent) 55%, transparent);
    }}

    .md-content a:hover {{
      color: var(--accent-2);
      border-bottom-color: var(--accent-2);
    }}

    .md-content table {{
      border-collapse: collapse;
      width: 100%;
      display: block;
      overflow-x: auto;
      margin: 1rem 0;
      border: 1px solid var(--border);
      border-radius: 10px;
    }}

    .md-content th,
    .md-content td {{
      border: 1px solid var(--border);
      padding: 0.5rem;
      text-align: left;
      vertical-align: top;
      min-width: 110px;
    }}

    .md-content img {{
      max-width: min(100%, 320px);
      height: auto;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--panel-2);
      cursor: zoom-in;
    }}

    .image-lightbox {{
      position: fixed;
      inset: 0;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      background: color-mix(in srgb, #000 75%, transparent);
      z-index: 9999;
    }}

    .image-lightbox.open {{
      display: flex;
    }}

    .image-lightbox img {{
      max-width: min(96vw, 1700px);
      max-height: 92vh;
      width: auto;
      height: auto;
      border-radius: 10px;
      border: 1px solid color-mix(in srgb, var(--border) 70%, #fff 30%);
      box-shadow: 0 18px 40px color-mix(in srgb, #000 45%, transparent);
      background: #111;
    }}

    .image-lightbox-close {{
      position: absolute;
      top: 0.8rem;
      right: 0.9rem;
      border: 1px solid color-mix(in srgb, var(--border) 80%, transparent);
      background: color-mix(in srgb, var(--panel) 85%, transparent);
      color: var(--text);
      border-radius: 8px;
      padding: 0.35rem 0.6rem;
      cursor: pointer;
      font-size: 0.9rem;
    }}

    .cp-details-list {{
      margin: 0.35rem 0 0;
      padding-left: 1.1rem;
    }}

    .cp-details-list li {{
      margin: 0.15rem 0;
    }}

    .cp-date-inline {{
      display: block;
      margin-top: 0.2rem;
      margin-bottom: 0.1rem;
      color: var(--muted);
      font-size: 0.9em;
      font-weight: 500;
      white-space: nowrap;
    }}

    .error {{
      color: #fca5a5;
      border: 1px solid #dc2626;
      background: color-mix(in srgb, #dc2626 15%, transparent);
      border-radius: 10px;
      padding: 0.8rem;
      margin-top: 0.8rem;
    }}

    @media (max-width: 960px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{
        position: static;
        height: auto;
        border-right: none;
        border-bottom: 1px solid var(--border);
      }}
      main {{ padding: 1rem; }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h1 class="brand">Public Repository</h1>
      <p class="hint">Standalone Markdown website</p>
      <ul class="nav-list" id="navList"></ul>
    </aside>

    <main>
      <section class="content-shell">
        <div class="breadcrumbs" id="breadcrumbs"></div>
        <article class="md-content" id="content">Loading...</article>
      </section>
    </main>
  </div>

  <div class="image-lightbox" id="imageLightbox" aria-hidden="true">
    <button class="image-lightbox-close" id="imageLightboxClose" type="button">Close</button>
    <img id="imageLightboxImg" alt="Zoomed image" />
  </div>

__SCRIPTS__

  <script>
    const START_DOC = "README.md";
    const ASSET_PREFIX = "../";
    const navList = document.getElementById("navList");
    const content = document.getElementById("content");
    const breadcrumbs = document.getElementById("breadcrumbs");

    marked.setOptions({
      gfm: true,
      breaks: false,
      mangle: false,
      headerIds: true
    });

    function normalizePath(path) {
      return path.replace(/\\\\/g, "/").replace(/^\.\//, "").replace(/^\//, "");
    }

    function encodePath(path) {
      return path.split("/").map((segment) => encodeURIComponent(segment)).join("/");
    }

    function splitHash(raw) {
      const [pathPart, ...hashParts] = raw.split("#");
      return {
        path: normalizePath(pathPart),
        hash: hashParts.length ? `#${{hashParts.join("#")}}` : ""
      };
    }

    function resolvePath(baseDoc, target) {
      const cleanedTarget = normalizePath(target.split("#")[0]);
      if (!cleanedTarget) return normalizePath(baseDoc);

      const topSegment = cleanedTarget.split("/")[0];
      if (repoTopLevel.has(topSegment)) {
        return cleanedTarget;
      }

      const baseDir = baseDoc.includes("/") ? baseDoc.slice(0, baseDoc.lastIndexOf("/") + 1) : "";
      const resolved = new URL(cleanedTarget, `https://local/${{baseDir}}`).pathname.slice(1);
      return normalizePath(resolved);
    }

    function getEmbeddedDocs() {
      const docs = new Map();
      for (const node of document.querySelectorAll('script[type="text/markdown"][id^="md-"]')) {
        const path = node.id.replace(/^md-/, "");
        docs.set(path, node.textContent || "");
      }
      return docs;
    }

    function extractTitle(markdown, fallbackPath) {
      const heading = markdown.match(/^#\s+(.+)$/m);
      if (heading) return heading[1].trim();
      const base = fallbackPath.split("/").pop() || fallbackPath;
      return base.replace(/\.md$/i, "");
    }

    function findLinkedMarkdown(markdown, currentDoc) {
      const links = [];
      const regex = /\[[^\]]*\]\(([^)]+\.md(?:#[^)]+)?)\)/gi;
      for (const match of markdown.matchAll(regex)) {
        const raw = match[1].trim();
        if (!raw) continue;
        const {{ path }} = splitHash(raw);
        if (!path) continue;
        links.push(resolvePath(currentDoc, path));
      }
      return [...new Set(links)];
    }

    function isExternalUrl(url) {
      return /^(?:[a-z]+:)?\/\//i.test(url) || /^(data:|mailto:|javascript:|#)/i.test(url);
    }

    const docs = getEmbeddedDocs();
    const repoTopLevel = new Set(
      [...docs.keys()]
        .map((path) => path.split("/")[0])
        .filter(Boolean)
    );
    const titles = new Map([...docs.entries()].map(([path, md]) => [path, extractTitle(md, path)]));

    function ensureReachableLinksInNav() {
      const queue = [START_DOC];
      const seen = new Set();
      while (queue.length) {
        const current = queue.shift();
        if (seen.has(current) || !docs.has(current)) continue;
        seen.add(current);
        const md = docs.get(current) || "";
        for (const linked of findLinkedMarkdown(md, current)) {
          if (!seen.has(linked) && docs.has(linked)) queue.push(linked);
        }
      }
      for (const key of [...docs.keys()]) {
        if (!seen.has(key) && key !== START_DOC) {
          docs.delete(key);
          titles.delete(key);
        }
      }
    }

    function prettyName(text) {
      return (text || "").replace(/[_-]/g, " ").trim();
    }

    function getDocLabel(docPath) {
      if (docPath === START_DOC) {
        return titles.get(docPath) || "Home";
      }

      const parts = docPath.split("/");
      const fileName = parts[parts.length - 1] || "";
      if (/^README\.md$/i.test(fileName) && parts.length > 1) {
        return prettyName(parts[parts.length - 2]);
      }

      return titles.get(docPath) || prettyName(fileName.replace(/\.md$/i, ""));
    }

    function isGroupRootDoc(docPath) {
      return /\/README\.md$/i.test(docPath);
    }

    function getGroupRootDoc(groupDocs) {
      const readme = groupDocs.find((path) => isGroupRootDoc(path));
      return readme || groupDocs[0] || "";
    }

    function getTopLevelOrder() {
      const order = [];
      const startDocMarkdown = docs.get(START_DOC) || "";

      for (const linkedPath of findLinkedMarkdown(startDocMarkdown, START_DOC)) {
        const top = linkedPath.split("/")[0];
        if (top && !order.includes(top)) {
          order.push(top);
        }
      }

      for (const path of docs.keys()) {
        if (path === START_DOC) continue;
        const top = path.split("/")[0];
        if (top && !order.includes(top)) {
          order.push(top);
        }
      }

      return order;
    }

    function sortGroupDocs(a, b) {
      const aIsReadme = /\/README\.md$/i.test(a);
      const bIsReadme = /\/README\.md$/i.test(b);
      if (aIsReadme !== bIsReadme) return aIsReadme ? -1 : 1;

      const depthDiff = a.split("/").length - b.split("/").length;
      if (depthDiff !== 0) return depthDiff;

      return getDocLabel(a).localeCompare(getDocLabel(b));
    }

    function buildNav(activeDoc) {
      const groups = new Map();
      for (const path of docs.keys()) {
        if (path === START_DOC) continue;
        const top = path.split("/")[0];
        if (!groups.has(top)) groups.set(top, []);
        groups.get(top).push(path);
      }

      const items = [];
      const homeActive = activeDoc === START_DOC ? "active" : "";
      items.push(`<li><a class="nav-link nav-home ${{homeActive}}" style="--level: 0" href="#${{encodeURIComponent(START_DOC)}}">${{getDocLabel(START_DOC)}} (main)</a></li>`);
      items.push('<li><hr class="nav-double-separator" /></li>');

      let isFirstGroup = true;
      for (const top of getTopLevelOrder()) {
        if (!groups.has(top)) continue;
        if (!isFirstGroup) {
          items.push('<li><hr class="nav-separator" /></li>');
        }
        isFirstGroup = false;

        const groupDocs = groups.get(top).slice().sort(sortGroupDocs);
        const rootDoc = getGroupRootDoc(groupDocs);
        const groupIsActive = activeDoc === rootDoc || activeDoc.startsWith(`${top}/`);

        for (const path of groupDocs) {
          const isRoot = path === rootDoc;
          if (!isRoot && !groupIsActive) continue;

          const active = path === activeDoc ? "active" : "";
          const level = isRoot ? 1 : Math.max(1, path.split("/").length - 2);
          const label = isRoot ? prettyName(top) : getDocLabel(path);
          const itemized = isRoot ? "" : "itemized";
          items.push(`<li><a class="nav-link ${{itemized}} ${{active}}" style="--level: ${{level}}" href="#${{encodeURIComponent(path)}}">${{label}}</a></li>`);
        }
      }

      navList.innerHTML = items.join("");
    }

    function setBreadcrumb(path) {
      breadcrumbs.textContent = path.split("/").join(" / ");
    }

    function buildRenderer(currentDoc) {
      const renderer = new marked.Renderer();

      renderer.link = ({ href, title, tokens }) => {
        const text = marked.Parser.parseInline(tokens);
        if (!href) return text;

        const rawHref = href.trim();
        if (/^https?:\/\//i.test(rawHref)) {
          const ttl = title ? ` title="${{title}}"` : "";
          return `<a href="${{rawHref}}" target="_blank" rel="noopener"${{ttl}}>${{text}}</a>`;
        }

        const {{ path, hash }} = splitHash(rawHref);
        const resolved = resolvePath(currentDoc, path || currentDoc);

        if ((path || "").toLowerCase().endsWith(".md")) {
          const targetDoc = docs.has(resolved) ? `${{resolved}}${{hash}}` : resolved;
          if (docs.has(resolved)) {
            return `<a href="#${{encodeURIComponent(targetDoc)}}">${{text}}</a>`;
          }
          return `<a href="${{ASSET_PREFIX}}${{encodePath(resolved)}}" data-resolved="1">${{text}}</a>`;
        }

        const assetHref = `${{ASSET_PREFIX}}${{encodePath(resolvePath(currentDoc, rawHref))}}`;
        const ttl = title ? ` title="${{title}}"` : "";
        return `<a href="${{assetHref}}" data-resolved="1"${{ttl}}>${{text}}</a>`;
      };

      renderer.image = ({ href, title, text }) => {
        const src = `${{ASSET_PREFIX}}${{encodePath(resolvePath(currentDoc, href || ""))}}`;
        const ttl = title ? ` title="${{title}}"` : "";
        return `<img src="${{src}}" data-resolved="1" alt="${{text || ""}}" loading="lazy"${{ttl}} />`;
      };

      return renderer;
    }

    function rewriteRenderedAssetLinks(rootElement, currentDoc) {
      for (const image of rootElement.querySelectorAll("img[src]")) {
        if (image.dataset.resolved === "1") continue;
        const src = (image.getAttribute("src") || "").trim();
        if (!src || isExternalUrl(src)) continue;
        const resolved = resolvePath(currentDoc, src);
        const finalSrc = `${{ASSET_PREFIX}}${{encodePath(resolved)}}`;
        image.setAttribute("src", finalSrc);
        image.dataset.resolved = "1";
      }

      for (const anchor of rootElement.querySelectorAll("a[href]")) {
        if (anchor.dataset.resolved === "1") continue;
        const href = (anchor.getAttribute("href") || "").trim();
        if (!href || isExternalUrl(href)) continue;
        if (href.startsWith("#")) continue;
        if (/\.md(?:#.*)?$/i.test(href)) continue;
        const resolved = resolvePath(currentDoc, href);
        anchor.setAttribute("href", `${{ASSET_PREFIX}}${{encodePath(resolved)}}`);
        anchor.dataset.resolved = "1";
      }
    }

    function setupImageZoom(rootElement) {
      const lightbox = document.getElementById("imageLightbox");
      const lightboxImg = document.getElementById("imageLightboxImg");
      const lightboxClose = document.getElementById("imageLightboxClose");
      if (!lightbox || !lightboxImg || !lightboxClose) return;

      const closeLightbox = () => {
        lightbox.classList.remove("open");
        lightbox.setAttribute("aria-hidden", "true");
        lightboxImg.removeAttribute("src");
        lightboxImg.removeAttribute("alt");
      };

      if (!lightbox.dataset.bound) {
        lightbox.addEventListener("click", (event) => {
          if (event.target === lightbox) closeLightbox();
        });
        lightboxClose.addEventListener("click", closeLightbox);
        document.addEventListener("keydown", (event) => {
          if (event.key === "Escape") closeLightbox();
        });
        lightbox.dataset.bound = "1";
      }

      for (const image of rootElement.querySelectorAll("img")) {
        if (image.dataset.zoomBound) continue;
        image.dataset.zoomBound = "1";
        image.addEventListener("click", (event) => {
          event.preventDefault();
          event.stopPropagation();
          const src = image.getAttribute("src") || "";
          if (!src) return;
          lightboxImg.setAttribute("src", src);
          lightboxImg.setAttribute("alt", image.getAttribute("alt") || "Zoomed image");
          lightbox.classList.add("open");
          lightbox.setAttribute("aria-hidden", "false");
        });
      }
    }

    function moveCraftProjectDetailsIntoDescription(rootElement, currentDoc) {
      if (!currentDoc.startsWith("Craft-Projects/")) return;

      for (const table of rootElement.querySelectorAll("table")) {
        const headerCells = [...table.querySelectorAll("thead th")];
        if (!headerCells.length) continue;

        const headers = headerCells.map((cell) => (cell.textContent || "").trim().toLowerCase());
        const descIndex = headers.findIndex((name) => name === "description");
        const dateIndex = headers.findIndex((name) => name === "date");
        const detailsIndex = headers.findIndex((name) => name === "details");
        if (descIndex < 0 || dateIndex < 0 || descIndex === dateIndex) continue;

        table.style.tableLayout = "fixed";
        for (const row of table.querySelectorAll("tr")) {
          const cells = [...row.children];
          if (cells.length > descIndex) {
            cells[descIndex].style.width = "33.333%";
            cells[descIndex].style.maxWidth = "33.333%";
          }
        }

        const bodyRows = [...table.querySelectorAll("tbody tr")];
        for (const row of bodyRows) {
          const cells = [...row.querySelectorAll("td")];
          if (cells.length <= Math.max(descIndex, dateIndex)) continue;

          const descCell = cells[descIndex];
          const dateCell = cells[dateIndex];
          const dateText = (dateCell.textContent || "").replace(/\u00a0/g, " ").trim();

          if (dateText) {
            const dateSpan = document.createElement("span");
            dateSpan.className = "cp-date-inline";
            dateSpan.textContent = `<${dateText}>`;

            const detailsList = descCell.querySelector("ul.cp-details-list");
            if (detailsList) {
              detailsList.insertAdjacentElement("beforebegin", dateSpan);
            } else {
              descCell.appendChild(dateSpan);
            }
          }

          if (detailsIndex >= 0 && cells.length > detailsIndex) {
            const detailsCell = cells[detailsIndex];
            const detailsHtml = (detailsCell.innerHTML || "").trim();
            const detailsText = (detailsCell.textContent || "").replace(/\u00a0/g, " ").trim();
            if (detailsHtml && detailsText) {
              let list = descCell.querySelector("ul.cp-details-list");
              if (!list) {
                list = document.createElement("ul");
                list.className = "cp-details-list";
                descCell.appendChild(list);
              }

              const item = document.createElement("li");
              item.innerHTML = detailsHtml;
              list.appendChild(item);
              detailsCell.innerHTML = "";
            }
          }
          dateCell.innerHTML = "";
        }

        const indexesToRemove = [dateIndex, detailsIndex]
          .filter((index) => index >= 0)
          .sort((a, b) => b - a);

        for (const row of table.querySelectorAll("tr")) {
          for (const index of indexesToRemove) {
            const cells = [...row.children];
            if (cells.length > index) {
              cells[index].remove();
            }
          }
        }
      }
    }

    function renderPage() {
      const rawHash = decodeURIComponent(location.hash.replace(/^#/, "")).trim();
      const {{ path, hash }} = splitHash(rawHash || START_DOC);
      const docPath = docs.has(path) ? path : START_DOC;
      const markdown = docs.get(docPath);

      if (!markdown) {
        content.innerHTML = `<div class="error">Document not found: ${{docPath}}</div>`;
        return;
      }

      const renderer = buildRenderer(docPath);
      content.innerHTML = marked.parse(markdown, {{ renderer }});
      rewriteRenderedAssetLinks(content, docPath);
      moveCraftProjectDetailsIntoDescription(content, docPath);
      setupImageZoom(content);
      setBreadcrumb(docPath);
      buildNav(docPath);

      if (hash) {
        requestAnimationFrame(() => {
          const target = document.getElementById(hash.slice(1));
          if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
      }} else {{
        window.scrollTo({ top: 0, behavior: "instant" });
      }}
    }

    ensureReachableLinksInNav();
    renderPage();
    window.addEventListener("hashchange", renderPage);
  </script>
</body>
</html>
'''

    template = template.replace("{{", "{").replace("}}", "}")
    return template.replace("__SCRIPTS__", scripts)


def main() -> None:
    docs = discover_docs(START_DOC)
    output = build_html(docs)
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(output, encoding="utf-8")

    OUTPUT_README.write_text(
        "# Public Docs Site\n\n"
        "This website is generated from the top-level README graph.\n\n"
        "## Build\n\n"
      "Run from repository root:\n\n"
      "- `python _Tools/build_site.py`\n\n"
        "## Open\n\n"
        "- Open `index.html` directly (no local server needed).\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
