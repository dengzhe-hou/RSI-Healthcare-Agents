"""Build the searchable manuscript bibliography without changing the evidence map.

A normal rebuild uses references/references.bib, already in manuscript order.
To refresh from the manuscript, pass --bib references.bib --bbl build/main.bbl.
Only entries cited in the BBL are exported when --bbl is supplied.
"""
from pathlib import Path
import argparse, html, json, re, unicodedata
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'references'


def closing_brace(text, start):
    depth = 0
    for pos in range(start, len(text)):
        if pos and text[pos - 1] == '\\':
            continue
        if text[pos] == '{':
            depth += 1
        elif text[pos] == '}':
            depth -= 1
            if depth == 0:
                return pos
    raise ValueError('Unclosed BibTeX entry or field')


def entries(text):
    result = {}
    for match in re.finditer(r'(?m)^@(\w+)\s*\{\s*([^,\s]+)\s*,', text):
        end = closing_brace(text, text.index('{', match.start()))
        key = match.group(2)
        if key in result:
            raise ValueError('Duplicate bibliography key ' + key)
        fields = {}
        pos = match.end()
        while pos < end:
            while pos < end and (text[pos].isspace() or text[pos] == ','):
                pos += 1
            if pos == end:
                break
            field = re.match(r'(\w+)\s*=\s*', text[pos:end])
            if not field:
                raise ValueError('Cannot parse field in ' + key)
            pos += field.end()
            if text[pos] == '{':
                finish = closing_brace(text, pos)
                value = text[pos + 1:finish]
                pos = finish + 1
            elif text[pos] == '"':
                finish = pos + 1
                while text[finish] != '"' or text[finish - 1] == '\\':
                    finish += 1
                value = text[pos + 1:finish]
                pos = finish + 1
            else:
                finish = text.find(',', pos, end)
                finish = end if finish == -1 else finish
                value = text[pos:finish].strip()
                pos = finish
            fields[field.group(1).lower()] = value
        result[key] = {'fields': fields, 'bibtex': text[match.start():end + 1]}
    return result


def plain(value):
    value = re.sub(r'\\url\{([^}]+)\}', r'\1', value)
    value = re.sub(r'\\(["c])\s*\{?([A-Za-z])\}?',
                   lambda m: unicodedata.normalize('NFC', m[2] + ('\u0308' if m[1] == '"' else '\u0327')), value)
    return re.sub(r'\s+', ' ', value.replace('{', '').replace('}', '').replace('~', ' ')).strip()


def author_names(value):
    depth, start, names = 0, 0, []
    for pos, char in enumerate(value):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
        elif depth == 0 and value[pos:pos + 5] == ' and ':
            names.append(value[start:pos])
            start = pos + 5
    names.append(value[start:])
    result = []
    for name in names:
        name = plain(name)
        if name == 'others':
            result.append('et al.')
        elif ',' in name:
            surname, given = name.split(',', 1)
            result.append(given.strip() + ' ' + surname.strip())
        elif name:
            result.append(name)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bib', type=Path, default=OUT / 'references.bib')
    parser.add_argument('--bbl', type=Path)
    args = parser.parse_args()
    source = entries(args.bib.read_text())
    keys = re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', args.bbl.read_text()) if args.bbl else list(source)
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate citation numbers in bibliography input')
    mapped = {s['key']: s for s in json.loads((ROOT / 'map/data.json').read_text())['studies']}
    records = []
    for number, key in enumerate(keys, 1):
        entry = source[key]
        fields = entry['fields']
        names = author_names(fields.get('author', ''))
        title = plain(fields['title'])
        doi = plain(fields.get('doi', ''))
        url = plain(fields.get('url', ''))
        eprint = plain(fields.get('eprint', ''))
        if doi:
            url = doi if doi.startswith('https://') else 'https://doi.org/' + doi
        elif not url and eprint:
            url = 'https://arxiv.org/abs/' + eprint
        elif not url:
            match = re.search(r'https?://[^\s}]+', fields.get('howpublished', ''))
            url = match[0] if match else mapped.get(key, {}).get('source_url', '')
        venue = plain(fields.get('journal') or fields.get('booktitle') or fields.get('publisher') or '')
        records.append(dict(number=number, key=key, title=title, authors=names,
                            year=plain(fields.get('year', '')), venue=venue, doi=doi,
                            url=url, eprint=eprint, in_evidence_map=key in mapped,
                            bibtex=entry['bibtex']))
    evidence_count = sum(x['in_evidence_map'] for x in records)
    counts = dict(total=len(records), evidence=evidence_count, other=len(records) - evidence_count)
    OUT.mkdir(exist_ok=True)
    (OUT / 'references.bib').write_text('\n\n'.join(r['bibtex'] for r in records) + '\n')
    (OUT / 'references.json').write_text(json.dumps(dict(counts=counts, references=records), ensure_ascii=False, indent=2) + '\n')
    esc = html.escape
    items = []
    for r in records:
        people = r['authors'][:3]
        if len(r['authors']) > 3 and people[-1] != 'et al.':
            people.append('et al.')
        author_text = ' · '.join(people)
        detail = ' · '.join(x for x in [r['year'], r['venue']] if x)
        source = '<a href="' + esc(r['url'], quote=True) + '">Read original ↗</a>' if r['url'] else '<a href="https://scholar.google.com/scholar?q=' + quote(r['title']) + '">Search title ↗</a>'
        evidence = '<a class="evidence-link" href="../map/#' + esc(r['key']) + '">Evidence record ↗</a>' if r['in_evidence_map'] else ''
        search = ' '.join([r['title'], ' '.join(r['authors']), r['year'], r['venue'], r['key']])
        items.append(f'''<li id="{esc(r['key'])}" class="reference" data-scope="{'evidence' if r['in_evidence_map'] else 'other'}" data-search="{esc(search, quote=True)}">
<span class="reference-number">[{r['number']}]</span><article><h2 class="reference-title">{esc(r['title'])}</h2>
<p class="reference-authors">{esc(author_text)}</p><p class="reference-venue">{esc(detail)}</p>
<div class="reference-actions">{source}{evidence}<details><summary>BibTeX</summary><div class="reference-bib"><button type="button" data-copy>Copy</button><pre>{esc(r['bibtex'])}</pre></div></details></div></article></li>''')
    page = (ROOT / 'references/template.html').read_text()
    page = page.replace('<!-- REFERENCES -->', '\n'.join(items))
    for key, value in counts.items():
        page = page.replace('{{' + key + '}}', str(value))
    (OUT / 'index.html').write_text(page)
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
