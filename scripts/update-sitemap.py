#!/usr/bin/env python3
"""Generate the static sitemap from canonical links; --check detects stale files."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ORIGIN = "https://rolatools.com"
NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


class PageMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            directives = attrs.get("content", "").lower().replace(",", " ").split()
            self.noindex |= "noindex" in directives or "none" in directives


def sitemap_xml(root):
    urls = set()
    for page in sorted(root.rglob("*.html")):
        if any(part.startswith(".") or part in {"scripts", "tests"}
               for part in page.relative_to(root).parts[:-1]):
            continue
        metadata = PageMetadata()
        metadata.feed(page.read_text(encoding="utf-8"))
        if metadata.noindex:
            continue
        if len(metadata.canonicals) != 1:
            raise ValueError(f"{page.relative_to(root)}: expected one canonical link or robots noindex")
        url = metadata.canonicals[0]
        parsed = urlsplit(url)
        if (f"{parsed.scheme}://{parsed.netloc}" != ORIGIN or not parsed.path
                or parsed.query or parsed.fragment or len(url) >= 2048
                or any(character.isspace() for character in url)):
            raise ValueError(f"{page.relative_to(root)}: invalid canonical URL: {url}")
        relative_path = unquote(parsed.path).lstrip("/")
        target = (root / relative_path / "index.html" if parsed.path.endswith("/")
                  else root / relative_path).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            raise ValueError(f"{page.relative_to(root)}: canonical target does not exist: {url}")
        urls.add(url)
    if not urls:
        raise ValueError("No indexable public pages found")
    ET.register_namespace("", NAMESPACE)
    document = ET.Element(f"{{{NAMESPACE}}}urlset")
    for url in sorted(urls):
        entry = ET.SubElement(document, f"{{{NAMESPACE}}}url")
        ET.SubElement(entry, f"{{{NAMESPACE}}}loc").text = url
    ET.indent(document, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(document, encoding="unicode") + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail instead of writing an outdated sitemap")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        content = sitemap_xml(root)
        path = root / "sitemap.xml"
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise ValueError("sitemap.xml is outdated; run python3 scripts/update-sitemap.py")
            if f"Sitemap: {ORIGIN}/sitemap.xml" not in (root / "robots.txt").read_text(encoding="utf-8").splitlines():
                raise ValueError("robots.txt must reference the sitemap")
            print("PASS: sitemap matches public canonical pages and robots.txt references it")
        else:
            path.write_text(content, encoding="utf-8")
            print("Updated sitemap.xml")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
