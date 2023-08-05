# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_export2html.ipynb (unless otherwise specified).

__all__ = ['HTMLParseAttrs', 'remove_widget_state', 'upd_metadata', 'hide_cells', 'clean_exports', 'treat_backticks',
           'add_jekyll_notes', 'copy_images', 'adapt_img_path', 'escape_latex', 'collapse_cells', 'remove_hidden',
           'find_default_level', 'add_show_docs', 'remove_fake_headers', 'remove_empty', 'get_metadata',
           'ExecuteShowDocPreprocessor', 'execute_nb', 'cite2link', 'write_tmpl', 'write_tmpls', 'nbdev_exporter',
           'process_cells', 'process_cell', 'convert_nb', 'notebook2html', 'convert_md', 'nb_detach_cells',
           'create_default_sidebar', 'make_sidebar']

# Cell
from .imports import *
from .sync import *
from .export import *
from .export import _mk_flag_re
from .showdoc import *
from .template import *

from html.parser import HTMLParser
from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
from nbconvert import HTMLExporter,MarkdownExporter
import traitlets

# Cell
class HTMLParseAttrs(HTMLParser):
    "Simple HTML parser which stores any attributes in `attrs` dict"
    def handle_starttag(self, tag, attrs): self.tag,self.attrs = tag,dict(attrs)

    def attrs2str(self):
        "Attrs as string"
        return ' '.join([f'{k}="{v}"' for k,v in self.attrs.items()])

    def show(self):
        "Tag with updated attrs"
        return f'<{self.tag} {self.attrs2str()} />'

    def __call__(self, s):
        "Parse `s` and store attrs"
        self.feed(s)
        return self.attrs

# Cell
def remove_widget_state(cell):
    "Remove widgets in the output of `cells`"
    if cell['cell_type'] == 'code' and 'outputs' in cell:
        cell['outputs'] = [l for l in cell['outputs']
                           if not ('data' in l and 'application/vnd.jupyter.widget-view+json' in l.data)]
    return cell

# Cell
# Note: `_re_show_doc` will catch show_doc even if it's commented out etc
_re_show_doc = re.compile(r"""
# Catches any show_doc and get the first argument in group 1
^\s*show_doc # line can start with any amount of whitespace followed by show_doc
\s*\(\s*     # Any number of whitespace, opening (, any number of whitespace
([^,\)\s]*)  # Catching group for any character but a comma, a closing ) or a whitespace
[,\)\s]      # A comma, a closing ) or a whitespace
""", re.MULTILINE | re.VERBOSE)

_re_show_doc_magic = _mk_flag_re(True, 'show_doc', -1,
    "# Catches a cell with %nbdev_show_doc \*\* and get that \*\* in group 1")

_re_hide_input = [
    _mk_flag_re(False, 'export', (0,1),
        "Matches any cell that has `#export in it"),
    _mk_flag_re(False, '(hide_input|hide-input)', 0,
        "Matches any cell that has `#hide_input` or `#hide-input` in it"),
    _mk_flag_re(True, 'export', (0,1),
        "Matches any cell that has `%nbdev_export` in it"),
    _mk_flag_re(True, 'hide_input', 0,
        "Matches any cell that has `%nbdev_hide_input` in it")]

_re_hide_output = [
    _mk_flag_re(False, '(hide_output|hide-output)', 0,
        "Matches any cell that has `#hide_output` or `#hide-output` in it"),
    _mk_flag_re(True, 'hide_output', 0,
        "Matches any cell that has `%nbdev_hide_output` in it")]

# Cell
def upd_metadata(cell, key, value=True):
    "Sets `key` to `value` on the `metadata` of `cell` without replacing metadata"
    cell.setdefault('metadata',{})[key] = value

# Cell
def hide_cells(cell):
    "Hide inputs of `cell` that need to be hidden"
    if check_re_multi(cell, [_re_show_doc, _re_show_doc_magic, *_re_hide_input]): upd_metadata(cell, 'hide_input')
    elif check_re_multi(cell, _re_hide_output): upd_metadata(cell, 'hide_output')
    return cell

# Cell
def clean_exports(cell):
    "Remove all flags from code `cell`s"
    if cell['cell_type'] == 'code':
        cell['source'] = split_flags_and_code(cell, str)[1]
    return cell

# Cell
def treat_backticks(cell):
    "Add links to backticks words in `cell`"
    if cell['cell_type'] == 'markdown': cell['source'] = add_doc_links(cell['source'])
    return cell

# Cell
_re_nb_link = re.compile(r"""
# Catches any link to a local notebook and keeps the title in group 1, the link without .ipynb in group 2
\[          # Opening [
([^\]]*)    # Catching group for any character except ]
\]\(        # Closing ], opening (
([^http]    # Catching group that must not begin by html (local notebook)
[^\)]*)     # and containing anything but )
.ipynb\)    # .ipynb and closing )
""", re.VERBOSE)

# Cell
_re_block_notes = re.compile(r"""
# Catches any pattern > Title: content with title in group 1 and content in group 2
^\s*>\s*     # > followed by any number of whitespace
([^:]*)      # Catching group for any character but :
:\s*         # : then any number of whitespace
([^\n]*)     # Catching group for anything but a new line character
(?:\n|$)     # Non-catching group for either a new line or the end of the text
""", re.VERBOSE | re.MULTILINE)

# Cell
def _to_html(text):
    return text.replace("'", "&#8217;")

# Cell
def add_jekyll_notes(cell):
    "Convert block quotes to jekyll notes in `cell`"
    styles = Config().get('jekyll_styles', 'note,warning,tip,important').split(',')
    def _inner(m):
        title,text = m.groups()
        if title.lower() not in styles: return f"> {title}:{text}"
        return '{% include '+title.lower()+".html content=\'"+_to_html(text)+"\' %}"
    if cell['cell_type'] == 'markdown':
        cell['source'] = _re_block_notes.sub(_inner, cell['source'])
    return cell

# Cell
_re_image = re.compile(r"""
# Catches any image file used, either with `![alt](image_file)` or `<img src="image_file">`
^(!\[           #   Beginning of line (since re.MULTILINE is passed) followed by ![ in a catching group
[^\]]*          #   Anything but ]
\]\()           #   Closing ] and opening (, end of the first catching group
([^\)]*)        #   Catching block with any character but )
(\))            #   Catching group with closing )
|               # OR
^(<img\ [^>]*>)  #   Catching group with <img some_html_code>
""", re.MULTILINE | re.VERBOSE)

_re_image1 = re.compile(r"^<img\ [^>]*>", re.MULTILINE)

# Cell
def _img2jkl(d, h, jekyll=True):
    if not jekyll: return '<img ' + h.attrs2str() + '>'
    if 'width' in d: d['max-width'] = d.pop('width')
    if 'src' in d:   d['file'] = d.pop('src')
    return '{% include image.html ' + h.attrs2str() + ' %}'

# Cell
def _is_real_image(src):
    return not (src.startswith('http://') or src.startswith('https://') or src.startswith('data:image/'))

# Cell
def copy_images(cell, fname, dest, jekyll=True):
    "Copy images referenced in `cell` from `fname` parent folder to `dest` folder"
    def _rep_src(m):
        grps = m.groups()
        if grps[3] is not None:
            h = HTMLParseAttrs()
            dic = h(grps[3])
            src = dic['src']
        else:
            cap = re.search(r'(\s"[^"]*")', grps[1])
            if cap is not None:
                grps = (grps[0], re.sub(r'\s"[^"]*"', '', grps[1]), cap.groups()[0] + grps[2], grps[3])
            src = grps[1]
        if _is_real_image(src):
            os.makedirs((Path(dest)/src).parent, exist_ok=True)
            shutil.copy(Path(fname).parent/src, Path(dest)/src)
            src = Config().doc_baseurl + src
        if grps[3] is not None:
            dic['src'] = src
            return _img2jkl(dic, h, jekyll=jekyll)
        else:  return f"{grps[0]}{src}{grps[2]}"
    if cell['cell_type'] == 'markdown': cell['source'] = _re_image.sub(_rep_src, cell['source'])
    return cell

# Cell
def _relative_to(path1, path2):
    p1,p2 = Path(path1).absolute().parts,Path(path2).absolute().parts
    i=0
    while i <len(p1) and i<len(p2) and p1[i] == p2[i]: i+=1
    p1,p2 = p1[i:],p2[i:]
    return os.path.sep.join(['..' for _ in p2] + list(p1))

# Cell
def adapt_img_path(cell, fname, dest, jekyll=True):
    "Adapt path of images referenced in `cell` from `fname` to work in folder `dest`"
    def _rep(m):
        gps = m.groups()
        if gps[0] is not None:
            start,img,end = gps[:3]
            if not (img.startswith('http:/') or img.startswith('https:/')):
                img = _relative_to(fname.parent/img, dest)
            return f'{start}{img}{end}'
        else:
            h = HTMLParseAttrs()
            dic = h(gps[3])
            if not (dic['src'].startswith('http:/') or dic['src'].startswith('https:/')):
                dic['src'] = _relative_to(fname.parent/dic['src'], dest)
            return _img2jkl(dic, h, jekyll=jekyll)
    if cell['cell_type'] == 'markdown': cell['source'] = _re_image.sub(_rep, cell['source'])
    return cell

# Cell
_re_latex = re.compile(r'^(\$\$.*\$\$)$', re.MULTILINE)

# Cell
def escape_latex(cell):
    if cell['cell_type'] != 'markdown': return cell
    cell['source'] = _re_latex.sub(r'{% raw %}\n\1\n{% endraw %}', cell['source'])
    return cell

# Cell
_re_cell_to_collapse_closed = [
    _mk_flag_re(False, '(collapse|collapse_hide|collapse-hide)', 0,
        "Matches any cell with #collapse or #collapse_hide"),
    _mk_flag_re(True, 'collapse_input', 0,
        "Matches any cell with %nbdev_collapse_input")]

_re_cell_to_collapse_open = [
    _mk_flag_re(False, '(collapse_show|collapse-show)', 0,
        "Matches any cell with #collapse_show"),
    _mk_flag_re(True, r'collapse_input[ \t]+open', 0,
        "Matches any cell with %nbdev_collapse_input open")]

_re_cell_to_collapse_output = [
    _mk_flag_re(False, '(collapse_output|collapse-output)', 0,
        "Matches any cell with #collapse_output"),
    _mk_flag_re(True, 'collapse_output', 0,
        "Matches any cell with %nbdev_collapse_output")]

# Cell
def collapse_cells(cell):
    "Add a collapse button to inputs or outputs of `cell` in either the open or closed position"
    if check_re_multi(cell, _re_cell_to_collapse_closed): upd_metadata(cell,'collapse_hide')
    elif check_re_multi(cell, _re_cell_to_collapse_open): upd_metadata(cell,'collapse_show')
    elif check_re_multi(cell, _re_cell_to_collapse_output): upd_metadata(cell,'collapse_output')
    return cell

# Cell
_re_hide = [
    _mk_flag_re(False, 'hide', 0, 'Matches any cell with #hide'),
    _mk_flag_re(True, 'hide', 0, 'Matches any cell with %nbdev_hide')]
_re_all_flag = ReTstFlags(True)
_re_cell_to_remove = [
    _mk_flag_re(False, '(default_exp|exporti)', (0,1),
        'Matches any cell with #default_exp or #exporti'),
    _mk_flag_re(True, '(default_export|export_internal)', (0,1),
        'Matches any cell with %nbdev_default_export or %nbdev_export_internal')]
_re_default_cls_lvl = [
    _mk_flag_re(False, 'default_cls_lvl', 1, "Matches any cell with #default_cls_lvl"),
    _mk_flag_re(True, 'default_class_level', 1, "Matches any cell with %nbdev_default_class_level"),
]

# Cell
def remove_hidden(cells):
    "Remove in `cells` the ones with a flag `#hide`, `#default_exp`, `#default_cls_lvl` or `#exporti`"
    def _hidden(cell):
        "Check if `cell` should be hidden"
        if check_re_multi(cell, _re_hide, code_only=False): return True
        if check_re_multi(cell, [_re_all_flag, *_re_cell_to_remove, *_re_default_cls_lvl]): return True
        return False
    return [c for c in cells if not _hidden(c)]

# Cell
def find_default_level(cells):
    "Find in `cells` the default class level."
    for cell in cells:
        tst = check_re_multi(cell, _re_default_cls_lvl)
        if tst: return int(tst.groups()[0])
    return 2

# Cell
_re_export = _mk_flag_re(False, "exports?", (0,1),
    "Matches any line with #export or #exports with or without module name")
_re_export_magic = _mk_flag_re(True, "export(|_and_show)", (0,1),
    "Matches any line with %nbdev_export or %nbdev_export_and_show with or without module name")

# Cell
def _show_doc_cell(name, cls_lvl=None):
    return {'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': f"show_doc({name}{'' if cls_lvl is None else f', default_cls_level={cls_lvl}'})"}

def add_show_docs(cells, cls_lvl=None):
    "Add `show_doc` for each exported function or class"
    res, documented, documented_wild = [], [], []
    for cell in cells:
        m = check_re_multi(cell, [_re_show_doc, _re_show_doc_magic])
        if not m: continue
        if m.re is _re_show_doc:
            documented.append(m.group(1))
        else:
            names, wild_names, kwargs = parse_nbdev_show_doc(m.group(1))
            documented.extend(names)
            documented_wild.extend(wild_names)

    def _documented(name):
        if name in documented: return True
        # assume that docs will have been shown for all members of everything in documented_wild
        if name.rfind('.') != -1 and name[0:name.rfind('.')] in documented_wild: return True

    for cell in cells:
        res.append(cell)
        if check_re_multi(cell, [_re_export, _re_export_magic]):
            for n in export_names(cell['source'], func_only=True):
                if not _documented(n): res.append(_show_doc_cell(n, cls_lvl=cls_lvl))
    return res

# Cell
_re_fake_header = re.compile(r"""
# Matches any fake header (one that ends with -)
\#+    # One or more #
\s+    # One or more of whitespace
.*     # Any char
-\s*   # A dash followed by any number of white space
$      # End of text
""", re.VERBOSE)

# Cell
def remove_fake_headers(cells):
    "Remove in `cells` the fake header"
    return [c for c in cells if c['cell_type']=='code' or _re_fake_header.search(c['source']) is None]

# Cell
def remove_empty(cells):
    "Remove in `cells` the empty cells"
    return [c for c in cells if len(c['source']) >0]

# Cell
_re_title_summary = re.compile(r"""
# Catches the title and summary of the notebook, presented as # Title > summary, with title in group 1 and summary in group 2
^\s*       # Beginning of text followe by any number of whitespace
\#\s+      # # followed by one or more of whitespace
([^\n]*)   # Catching group for any character except a new line
\n+        # One or more new lines
>[ ]*       # > followed by any number of whitespace
([^\n]*)   # Catching group for any character except a new line
""", re.VERBOSE)

_re_title_only = re.compile(r"""
# Catches the title presented as # Title without a summary
^\s*       # Beginning of text followe by any number of whitespace
\#\s+      # # followed by one or more of whitespace
([^\n]*)   # Catching group for any character except a new line
(?:\n|$)    # New line or end of text
""", re.VERBOSE)

_re_properties = re.compile(r"""
^-\s+      # Beginnig of a line followed by - and at least one space
(.*?)      # Any pattern (shortest possible)
\s*:\s*    # Any number of whitespace, :, any number of whitespace
(.*?)$     # Any pattern (shortest possible) then end of line
""", re.MULTILINE | re.VERBOSE)

_re_mdlinks = re.compile(r"\[(.+)]\((.+)\)", re.MULTILINE)

# Cell
def _md2html_links(s):
    'Converts markdown links to html links'
    return _re_mdlinks.sub(r"<a href='\2'>\1</a>", s)

# Cell
def get_metadata(cells):
    "Find the cell with title and summary in `cells`."
    for i,cell in enumerate(cells):
        if cell['cell_type'] == 'markdown':
            match = _re_title_summary.match(cell['source'])
            if match:
                cells.pop(i)
                attrs = {k:v for k,v in _re_properties.findall(cell['source'])}
                return {'keywords': 'fastai',
                        'summary' : _md2html_links(match.groups()[1]),
                        'title'   : match.groups()[0],
                        **attrs}
            elif _re_title_only.search(cell['source']) is not None:
                title = _re_title_only.search(cell['source']).groups()[0]
                cells.pop(i)
                attrs = {k:v for k,v in _re_properties.findall(cell['source'])}
                return {'keywords': 'fastai',
                        'title'   : title,
                        **attrs}

    return {'keywords': 'fastai',
            'title'   : 'Title'}

# Cell
_re_mod_export = _mk_flag_re(False, "export[s]?", 1,
    "Matches any line with #export or #exports with a module name and catches it in group 1")
_re_mod_export_magic = _mk_flag_re(True, "export(?:|_and_show)", 1,
    "Matches any line with %nbdev_export or %nbdev_export_and_show catching module name in group 1")

def _gather_export_mods(cells):
    res = []
    for cell in cells:
        tst = check_re_multi(cell, [_re_mod_export, _re_mod_export_magic])
        if tst is not None: res.append(tst.groups()[0])
    return res

# Cell
# match any cell containing a zero indented import from the current lib
_re_lib_import = ReLibName(r"^from LIB_NAME\.", re.MULTILINE)
# match any cell containing a zero indented import
_re_import = re.compile(r"^from[ \t]|^import[ \t]", re.MULTILINE)
# match any cell containing a zero indented call to notebook2script
_re_notebook2script = re.compile(r"^notebook2script\(", re.MULTILINE)

# Cell
class ExecuteShowDocPreprocessor(ExecutePreprocessor):
    "An `ExecutePreprocessor` that only executes `show_doc` and `import` cells"
    def preprocess_cell(self, cell, resources, index):
        if not check_re(cell, _re_notebook2script):
            if check_re_multi(cell, [_re_show_doc, _re_show_doc_magic, _re_lib_import.re]):
                return super().preprocess_cell(cell, resources, index)
            elif check_re(cell, _re_import):
                try: return super().preprocess_cell(cell, resources, index)
                except: pass
        return cell, resources

# Cell
def _import_show_doc_cell(mods=None):
    "Add an import show_doc cell."
    source = f"from nbdev.showdoc import show_doc"
    if mods is not None:
        for mod in mods: source += f"\nfrom {Config().lib_name}.{mod} import *"
    return {'cell_type': 'code',
            'execution_count': None,
            'metadata': {'hide_input': True},
            'outputs': [],
            'source': source}

def execute_nb(nb, mod=None, metadata=None, show_doc_only=True):
    "Execute `nb` (or only the `show_doc` cells) with `metadata`"
    mods = ([] if mod is None else [mod]) + _gather_export_mods(nb['cells'])
    nb['cells'].insert(0, _import_show_doc_cell(mods))
    ep_cls = ExecuteShowDocPreprocessor if show_doc_only else ExecutePreprocessor
    ep = ep_cls(timeout=600, kernel_name='python3')
    metadata = metadata or {}
    pnb = nbformat.from_dict(nb)
    ep.preprocess(pnb, metadata)
    return pnb

# Cell
_re_cite = re.compile(r"(\\cite{)([^}]*)(})", re.MULTILINE | re.VERBOSE) # Catches citations used with `\cite{}`

# Cell
def _textcite2link(text):
    citations = _re_cite.finditer(text)
    out = []
    start_pos = 0
    for cit_group in citations:
        cit_pos_st =  cit_group.span()[0]
        cit_pos_fin =  cit_group.span()[1]
        out.append(text[start_pos:cit_pos_st])
        out.append('[')
        cit_group = cit_group[2].split(',')
        for i, cit in enumerate(cit_group):
            cit=cit.strip()
            out.append(f"""<a class="latex_cit" id="call-{cit}" href="#cit-{cit}">{cit}</a>""")
            if i != len(cit_group) - 1:
                out.append(',')
        out.append(']')
        start_pos = cit_pos_fin
    out.append(text[start_pos:])
    return ''.join(out)

# Cell
def cite2link(cell):
    '''Creates links from \cite{} to Refenrence section generated by jupyter_latex_envs'''
    if cell['cell_type'] == 'markdown': cell['source'] = _textcite2link(cell['source'])
    return cell

# Cell
def write_tmpl(tmpl, nms, cfg, dest):
    "Write `tmpl` to `dest` (if missing) filling in `nms` in template using dict `cfg`"
    if dest.exists(): return
    vs = {o:cfg.d[o] for o in nms.split()}
    outp = tmpl.format(**vs)
    dest.write_text(outp)

# Cell
def write_tmpls():
    "Write out _config.yml and _data/topnav.yml using templates"
    cfg = Config()
    write_tmpl(config_tmpl, 'user lib_name title copyright description', cfg, cfg.doc_path/'_config.yml')
    write_tmpl(topnav_tmpl, 'host git_url', cfg, cfg.doc_path/'_data'/'topnav.yml')
    write_tmpl(makefile_tmpl, 'nbs_path lib_name', cfg, cfg.config_file.parent/'Makefile')

# Cell
def nbdev_exporter(cls=HTMLExporter, template_file=None):
    cfg = traitlets.config.Config()
    exporter = cls(cfg)
    exporter.exclude_input_prompt=True
    exporter.exclude_output_prompt=True
    exporter.anchor_link_text = ' '
    exporter.template_file = 'jekyll.tpl' if template_file is None else template_file
    exporter.template_path.append(str(Path(__file__).parent/'templates'))
    return exporter

# Cell
process_cells = [remove_fake_headers, remove_hidden, remove_empty]
process_cell  = [hide_cells, collapse_cells, remove_widget_state, add_jekyll_notes, escape_latex, cite2link]

# Cell
_re_digits = re.compile(r'^\d+\S*?_')

# Cell
def _nb2htmlfname(nb_path, dest=None):
    if dest is None: dest = Config().doc_path
    return Path(dest)/_re_digits.sub('', nb_path.with_suffix('.html').name)

# Cell
def convert_nb(fname, cls=HTMLExporter, template_file=None, exporter=None, dest=None):
    "Convert a notebook `fname` to html file in `dest_path`."
    fname = Path(fname).absolute()
    nb = read_nb(fname)
    meta_jekyll = get_metadata(nb['cells'])
    meta_jekyll['nb_path'] = str(fname.relative_to(Config().lib_path.parent))
    cls_lvl = find_default_level(nb['cells'])
    mod = find_default_export(nb['cells'])
    nb['cells'] = compose(*process_cells,partial(add_show_docs, cls_lvl=cls_lvl))(nb['cells'])
    _func = compose(partial(copy_images, fname=fname, dest=Config().doc_path), *process_cell, treat_backticks)
    nb['cells'] = [_func(c) for c in nb['cells']]
    nb = execute_nb(nb, mod=mod)
    nb['cells'] = [clean_exports(c) for c in nb['cells']]
    if exporter is None: exporter = nbdev_exporter(cls=cls, template_file=template_file)
    with open(_nb2htmlfname(fname, dest=dest),'w') as f:
        f.write(exporter.from_notebook_node(nb, resources=meta_jekyll)[0])

# Cell
def _notebook2html(fname, cls=HTMLExporter, template_file=None, exporter=None, dest=None):
    time.sleep(random.random())
    print(f"converting: {fname}")
    try:
        convert_nb(fname, cls=cls, template_file=template_file, exporter=exporter, dest=dest)
        return True
    except Exception as e:
        print(e)
        return False

# Cell
def notebook2html(fname=None, force_all=False, n_workers=None, cls=HTMLExporter, template_file=None, exporter=None, dest=None):
    "Convert all notebooks matching `fname` to html files"
    if fname is None:
        files = [f for f in Config().nbs_path.glob('*.ipynb') if not f.name.startswith('_')]
    else:
        p = Path(fname)
        files = list(p.parent.glob(p.name))
    if len(files)==1:
        force_all = True
        if n_workers is None: n_workers=0
    if not force_all:
        # only rebuild modified files
        files,_files = [],files.copy()
        for fname in _files:
            fname_out = _nb2htmlfname(Path(fname).absolute(), dest=dest)
            if not fname_out.exists() or os.path.getmtime(fname) >= os.path.getmtime(fname_out):
                files.append(fname)
    if len(files)==0: print("No notebooks were modified")
    else:
        passed = parallel(_notebook2html, files, n_workers=n_workers, cls=cls, template_file=template_file, exporter=exporter, dest=dest)
        if not all(passed):
            msg = "Conversion failed on the following:\n"
            raise Exception(msg + '\n'.join([f.name for p,f in zip(passed,files) if not p]))

# Cell
def convert_md(fname, dest_path, img_path='docs/images/', jekyll=True):
    "Convert a notebook `fname` to a markdown file in `dest_path`."
    fname = Path(fname).absolute()
    if not img_path: img_path = fname.stem + '_files/'
    Path(img_path).mkdir(exist_ok=True, parents=True)
    nb = read_nb(fname)
    meta_jekyll = get_metadata(nb['cells'])
    try: meta_jekyll['nb_path'] = str(fname.relative_to(Config().lib_path.parent))
    except: meta_jekyll['nb_path'] = str(fname)
    nb['cells'] = compose(*process_cells)(nb['cells'])
    nb['cells'] = [compose(partial(adapt_img_path, fname=fname, dest=dest_path, jekyll=jekyll), *process_cell)(c)
                   for c in nb['cells']]
    fname = Path(fname).absolute()
    dest_name = fname.with_suffix('.md').name
    exp = nbdev_exporter(cls=MarkdownExporter, template_file='jekyll-md.tpl' if jekyll else 'md.tpl')
    export = exp.from_notebook_node(nb, resources=meta_jekyll)
    md = export[0]
    for ext in ['png', 'svg']:
        md = re.sub(r'!\['+ext+'\]\((.+)\)', '!['+ext+'](' + img_path + '\\1)', md)
    with (Path(dest_path)/dest_name).open('w') as f: f.write(md)
    if hasattr(export[1]['outputs'], 'items'):
        for n,o in export[1]['outputs'].items():
            with open(Path(dest_path)/img_path/n, 'wb') as f: f.write(o)

# Cell
_re_att_ref = re.compile(r' *!\[(.*)\]\(attachment:image.png(?: "(.*)")?\)')

# Cell
try: from PIL import Image
except: pass # Only required for _update_att_ref

# Cell
_tmpl_img = '<img alt="{title}" width="{width}" caption="{title}" id="{id}" src="{name}">'

def _update_att_ref(line, path, img):
    m = _re_att_ref.match(line)
    if not m: return line
    alt,title = m.groups()
    w = img.size[0]
    if alt=='screenshot': w //= 2
    if not title: title = "TK: add title"
    return _tmpl_img.format(title=title, width=str(w), id='TK: add it', name=str(path))

# Cell
def _nb_detach_cell(cell, dest, use_img):
    att,src = cell['attachments'],cell['source']
    mime,img = first(first(att.values()).items())
    ext = mime.split('/')[1]
    for i in range(99999):
        p = dest/(f'att_{i:05d}.{ext}')
        if not p.exists(): break
    img = b64decode(img)
    p.write_bytes(img)
    del(cell['attachments'])
    if use_img:  return [_update_att_ref(o,p,Image.open(p)) for o in src]
    else: return [o.replace('attachment:image.png', str(p)) for o in src]

# Cell
def nb_detach_cells(path_nb, dest=None, replace=True, use_img=False):
    "Export cell attachments to `dest` and update references"
    path_nb = Path(path_nb)
    if not dest: dest = f'{path_nb.stem}_files'
    dest = Path(dest)
    dest.mkdir(exist_ok=True, parents=True)
    j = json.load(path_nb.open())
    atts = [o for o in j['cells'] if 'attachments' in o]
    for o in atts: o['source'] = _nb_detach_cell(o, dest, use_img)
    if atts and replace: json.dump(j, path_nb.open('w'))
    if not replace: return j

# Cell
import time,random,warnings

# Cell
def _leaf(k,v):
    url = 'external_url' if "http" in v else 'url'
    #if url=='url': v=v+'.html'
    return {'title':k, url:v, 'output':'web,pdf'}

# Cell
_k_names = ['folders', 'folderitems', 'subfolders', 'subfolderitems']
def _side_dict(title, data, level=0):
    k_name = _k_names[level]
    level += 1
    res = [(_side_dict(k, v, level) if isinstance(v,dict) else _leaf(k,v))
        for k,v in data.items()]
    return ({k_name:res} if not title
            else res if title.startswith('empty')
            else {'title': title, 'output':'web', k_name: res})

# Cell
_re_catch_title = re.compile('^title\s*:\s*(\S+.*)$', re.MULTILINE)

# Cell
def _get_title(fname):
    "Grabs the title of html file `fname`"
    with open(fname, 'r') as f: code = f.read()
    src =  _re_catch_title.search(code)
    return fname.stem if src is None else src.groups()[0]

# Cell
def create_default_sidebar():
    "Create the default sidebar for the docs website"
    dic = {"Overview": "/"}
    files = [f for f in Config().nbs_path.glob('*.ipynb') if not f.name.startswith('_')]
    fnames = [_nb2htmlfname(f) for f in sorted(files)]
    titles = [_get_title(f) for f in fnames if 'index' not in f.stem!='index']
    if len(titles) > len(set(titles)): print(f"Warning: Some of your Notebooks use the same title ({titles}).")
    dic.update({_get_title(f):f'/{f.stem}' for f in fnames if f.stem!='index'})
    dic = {Config().lib_name: dic}
    json.dump(dic, open(Config().doc_path/'sidebar.json', 'w'), indent=2)

# Cell
def make_sidebar():
    "Making sidebar for the doc website form the content of `doc_folder/sidebar.json`"
    if not (Config().doc_path/'sidebar.json').exists() or Config().custom_sidebar == 'False': create_default_sidebar()
    sidebar_d = json.load(open(Config().doc_path/'sidebar.json', 'r'))
    res = _side_dict('Sidebar', sidebar_d)
    res = {'entries': [res]}
    res_s = yaml.dump(res, default_flow_style=False)
    res_s = res_s.replace('- subfolders:', '  subfolders:').replace(' - - ', '   - ')
    res_s = f"""
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# Instead edit {'../../sidebar.json'}
"""+res_s
    open(Config().doc_path/'_data/sidebars/home_sidebar.yml', 'w').write(res_s)