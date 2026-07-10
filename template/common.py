# -*- coding: utf-8 -*-
"""
Biblioteca reaproveitável de geração do Diagnóstico Econômico Financeiro (O2 Inc.)

Extraída do gerador da Fight Analytics. Contém APENAS lógica genérica de
formatação/HTML (replica os number_format do Excel, monta tabelas no estilo
".fin" do design system O2, converte texto em bullets). Nenhum dado ou
conteúdo de cliente vive aqui — isso fica no script de cada projeto
(veja template/build.py e o PLAYBOOK.md).
"""
import openpyxl, datetime, html, re

MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

# ---------- texto ----------
def commafy(t):
    """Troca travessões/hífens usados como conectores por vírgula (mantém faixas –, negativos − e hífens de palavra)."""
    if not t:
        return t
    t = t.replace(' — ', ', ').replace(' – ', ', ').replace(' - ', ', ')
    t = t.replace('—', ', ')
    t = re.sub(r',\s*,', ', ', t)
    return t

def esc(s):
    return html.escape(str(s)).replace('\n', '<br>')

def escp(s):
    """escape + commafy (para prosa/legendas)."""
    return commafy(esc(s))

METRIC = re.compile(r'(R\$\s?\d[\d\.\,]*(?:\s?(?:mil|milhões|bilhões|bi))?|\d[\d\.,]*\s?%|\d[\d\.,]*x\b|\d+\s?a\s?\d+\s?clientes)')

def hl_first(txt):
    """Grifa em verde a primeira métrica (R$, %, x, faixa de clientes) encontrada na frase."""
    m = METRIC.search(txt)
    if not m:
        return txt
    a, b = m.span()
    return txt[:a] + '<span class="hl">' + txt[a:b] + '</span>' + txt[b:]

def to_points(text):
    """Quebra um bloco de texto (célula de planilha) em frases/bullets."""
    t = str(text).replace('\r', '').strip()
    raw = []
    for line in t.split('\n'):
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'^[•▶►•▶\-–]+\s*', '', line).strip()
        for sen in re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ú0-9(“"])', line):
            sen = sen.strip()
            if sen:
                raw.append(sen)
    out = []
    for s in raw:
        if out and len(s) < 28:
            out[-1] = out[-1] + ' ' + s
        else:
            out.append(s)
    return out

def ul_para(text):
    """Célula de texto corrido -> <ul class='plain'> com a 1ª métrica da 1ª frase grifada."""
    pts = to_points(text)
    h = '<ul class="plain">'
    for i, p in enumerate(pts):
        c = commafy(html.escape(p))
        if i == 0:
            c = hl_first(c)
        h += f'<li>{c}</li>'
    return h + '</ul>'

def ul_lines(items):
    """Lista de itens já separados (um por linha) -> <ul class='plain'>."""
    h = '<ul class="plain">'
    for i, it in enumerate(items):
        t = re.sub(r'^[•▶►•▶\-–]+\s*', '', str(it)).strip()
        c = commafy(html.escape(t))
        if i == 0:
            c = hl_first(c)
        h += f'<li>{c}</li>'
    return h + '</ul>'

def render_cur(text):
    """escape + commafy + converte «...» em grifo verde (uso: bullets escritos à mão com «destaque»)."""
    c = commafy(html.escape(str(text)))
    c = c.replace('«', '<span class="hl">').replace('»', '</span>')
    return c

def ul_cur(items):
    """Lista de bullets escritos à mão, usando «...» para marcar o que deve ficar em verde."""
    return '<ul class="plain">' + ''.join('<li>' + render_cur(x) + '</li>' for x in items) + '</ul>'

def cellvals(sheet, col, r0, r1):
    out = []
    for r in range(r0, r1 + 1):
        v = sheet[f"{col}{r}"].value
        if v is not None and str(v).strip():
            out.append(str(v))
    return out

# ---------- números (replica number_format do Excel) ----------
def fnum(x, dec):
    s = f"{abs(x):,.{dec}f}".replace(',', '␟').replace('.', ',').replace('␟', '.')
    return s

def fint(x):
    return f"{round(x):,}".replace(',', '.')

def fmt(cell):
    """Formata uma célula do openpyxl (data_only=True) igual ao number_format do Excel:
    #,##0;(#,##0);"-" , percentuais, 'x', 'dias', datas curtas (mon/aa)."""
    v = cell.value
    if v is None or (isinstance(v, str) and v.strip() == ''):
        return ''
    if isinstance(v, datetime.datetime):
        return f"{MES[v.month - 1]}/{str(v.year)[2:]}"
    if isinstance(v, str):
        return esc(v)
    if not isinstance(v, (int, float)):
        return esc(v)
    nf = cell.number_format or 'General'
    sec0 = nf.split(';')[0]
    negparen = ('(' in nf.replace(sec0, '', 1)) or (';(' in nf) or ('\\(' in nf)
    zerodash = '"-"' in nf
    if v == 0 and zerodash:
        return '–'
    if '%' in nf:
        dec = len(sec0.split('.')[1].split('%')[0]) if '.' in sec0 else 0
        s = fnum(v * 100, dec) + '%'
        return (('(' + s + ')') if negparen else '−' + s) if v < 0 else s
    if '"x"' in nf:
        return fnum(v, 2 if '0.00' in nf else 1) + 'x'
    if '" m"' in nf:
        return fnum(v, 1) + ' m'
    if '" dias"' in nf:
        return fint(v) + ' dias'
    if '#,##0' in nf:
        dec = len(sec0.split('.')[1].replace('"', '').split(')')[0]) if '.' in sec0 else 0
        s = fnum(v, dec)
        return (('(' + s + ')') if negparen else '−' + s) if v < 0 else s
    if nf == '0':
        return ('−' + fint(-v)) if v < 0 else fint(v)
    if nf == '0.0':
        return ('−' if v < 0 else '') + fnum(v, 1)
    if nf == '0.00':
        return ('−' if v < 0 else '') + fnum(v, 2)
    if float(v).is_integer():
        return ('−' + fint(-v)) if v < 0 else fint(v)
    return ('−' if v < 0 else '') + fnum(v, 2)

def fmt_shortdate(cell):
    v = cell.value
    if not isinstance(v, datetime.datetime):
        return fmt(cell)
    return f"{v.day:02d} {MES[v.month - 1]}"

def fmt_fulldate(cell):
    v = cell.value
    if not isinstance(v, datetime.datetime):
        return fmt(cell)
    return f"{v.day:02d}/{v.month:02d}/{v.year}"

def fmt_monyear(cell):
    v = cell.value
    if not isinstance(v, datetime.datetime):
        return fmt(cell)
    return f"{MES[v.month - 1]}/{v.year}"

# ---------- tabelas (design system ".fin") ----------
def rowclass(label, cells):
    """Detecta grupo/subtotal/margem pela convenção de rótulo da planilha O2 ((=), TOTAL, Margem, Consolidado)."""
    lab = (label or '').strip()
    if lab and not [t for t in cells[1:] if t != '']:
        return 'group'
    if lab.startswith('(=)') or lab.upper().startswith('TOTAL') or lab.startswith('Consolidado'):
        return 'subtotal'
    if lab.startswith('Margem'):
        return 'margin'
    return ''

def _tc(i, wrap_cols):
    return ' class="txt"' if i in wrap_cols else ''

def table(headers, rows, wrap_cols=(), green_key=False, key_labels=(), hl_labels=()):
    """Tabela padrão .fin. green_key=True grifa subtotais/RECEITA BRUTA (convenção DRE);
    key_labels grifa linhas específicas em verde (.keyrow); hl_labels grifa em verde-claro (.hlrow,
    usado para linhas que o cliente destacou manualmente e devem permanecer marcadas)."""
    h = '<div class="tbl-wrap"><table class="fin"><thead><tr>'
    for i, head in enumerate(headers):
        h += '<th' + _tc(i, wrap_cols) + '>' + esc(head) + '</th>'
    h += '</tr></thead><tbody>'
    for r in rows:
        cls = rowclass(r[0], r)
        lab = (r[0] or '').strip()
        is_key = (green_key and (cls == 'subtotal' or lab.startswith('RECEITA BRUTA'))) or (key_labels and any(lab.startswith(k) for k in key_labels))
        if is_key:
            cls = (cls + ' keyrow').strip()
        elif hl_labels and any(lab.startswith(k) for k in hl_labels):
            cls = (cls + ' hlrow').strip()
        h += (f'<tr class="{cls}">' if cls else '<tr>')
        for i, cell in enumerate(r):
            h += '<td' + _tc(i, wrap_cols) + '>' + str(cell) + '</td>'
        h += '</tr>'
    return h + '</tbody></table></div>'

def table_h(headers, rows, wrap_cols=(), key_labels=(), risk_labels=()):
    """Tabela larga (.fin.wide2 — muitas colunas, ex.: grade semanal/mensal). risk_labels grifa em vermelho (.riskrow)."""
    h = '<div class="tbl-wrap"><table class="fin wide2"><thead><tr>'
    for i, head in enumerate(headers):
        h += '<th' + _tc(i, wrap_cols) + '>' + esc(head) + '</th>'
    h += '</tr></thead><tbody>'
    for r in rows:
        cls = rowclass(r[0], r)
        lab = (r[0] or '').strip()
        if any(lab.startswith(k) for k in key_labels):
            cls = (cls + ' keyrow').strip()
        if any(lab.startswith(k) for k in risk_labels):
            cls = (cls + ' riskrow').strip()
        h += (f'<tr class="{cls}">' if cls else '<tr>')
        for i, cell in enumerate(r):
            h += '<td' + _tc(i, wrap_cols) + '>' + str(cell) + '</td>'
        h += '</tr>'
    return h + '</tbody></table></div>'

def sheet_rows(wb, name, r0, r1, cols):
    """Lê um bloco de linhas r0..r1 nas colunas indicadas, formatando cada célula com fmt().
    Pula linhas totalmente vazias (linhas de respiro entre blocos na planilha)."""
    s = wb[name]
    out = []
    for r in range(r0, r1 + 1):
        row = [fmt(s[f"{c}{r}"]) for c in cols]
        if any(x != '' for x in row):
            out.append(row)
    return out

# ---------- identificar as abas certas (regra da cor da aba) ----------
def colored_sheets(wb):
    """Lista as abas do workbook que têm cor de aba (tabColor) definida — pela convenção O2,
    são SEMPRE essas (e só essas) as abas de origem do diagnóstico (7.1 DRE, 7.2 DFC, ...).
    Abas de apoio/rascunho (Base, Apoio, Histórico...) ficam sem cor. Retorna [(nome, cor_rgb), ...]."""
    out = []
    for name in wb.sheetnames:
        tc = wb[name].sheet_properties.tabColor
        if tc is not None and getattr(tc, 'rgb', None):
            out.append((name, tc.rgb))
    return out

# ---------- montagem das abas (nav + panes) ----------
class PaneBuilder:
    """Acumula os <button> de navegação e os <section class='pane'> na ordem em que
    são adicionados. Uso: pb = PaneBuilder(); pb.add('dre','7','DRE Gerencial', body_html)"""
    def __init__(self):
        self.navs = []
        self.panes = []

    def add(self, id_, num, label, body):
        self.navs.append(f'      <button data-t="{id_}"><span class="n">{num}</span>{esc(label)}</button>')
        self.panes.append(f'    <section class="pane" id="{id_}">\n{body}\n    </section>')

    def render_navs(self):
        # a primeira aba entra com a classe "active" e o <main> abre com o edit-hint (ver shell.html)
        navs = list(self.navs)
        if navs:
            navs[0] = navs[0].replace('<button data-t=', '<button class="active" data-t=', 1)
        return '\n'.join(navs)

    def render_panes(self):
        panes = list(self.panes)
        if panes:
            panes[0] = panes[0].replace('class="pane"', 'class="pane active"', 1)
        return '\n\n'.join(panes)
