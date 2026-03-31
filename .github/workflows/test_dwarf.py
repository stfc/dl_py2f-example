#!/usr/bin/env python3
import sys, os, re, struct, subprocess
from ctypes import c_bool, c_char_p, c_double, c_float, c_int, c_long, sizeof

DWARF_TO_CTYPE = { 'INTEGER*4': c_int,
                   'INTEGER*8': c_long,
                   'REAL*4'   : c_float,
                   'REAL*8'   : c_double,
                   'LOGICAL*4': c_bool,
                   'LOGICAL*8': c_bool }

def _find_readelf():
    for cmd in ['readelf', 'greadelf']:
        try:
            subprocess.run([cmd, '--version'], capture_output=True)
            return cmd
        except FileNotFoundError:
            continue
    return 'readelf'

def parse_dwarf(libpath, module_name):
    dw         = subprocess.run([_find_readelf(), '-wi', libpath], capture_output=True, text=True)
    types      = {}
    cur_off    = None
    cur_tag    = None
    cur_attr   = {}
    subranges  = []
    in_sub     = False
    for line in dw.stdout.splitlines():
        m = re.match(r'\s*<(\d+)><([0-9a-f]+)>:\s*Abbrev Number:\s*\d+\s*\((\S+)\)', line)
        if m:
            new_tag = m.group(3)
            if new_tag == 'DW_TAG_subrange_type':
                in_sub = True
                continue
            in_sub = False
            if cur_off is not None:
                types[cur_off] = (cur_tag, dict(cur_attr), list(subranges))
            cur_off   = int(m.group(2), 16)
            cur_tag   = new_tag
            cur_attr  = {}
            subranges = []
            continue
        if cur_off is None:
            continue
        m2 = re.match(r'\s+<[0-9a-f]+>\s+(DW_AT_\w+)\s*:\s*(.*)', line)
        if m2:
            ak, av = m2.group(1), m2.group(2).strip()
            if ak == 'DW_AT_count':
                try:    subranges.append(('c', int(av)))
                except: pass
            elif ak == 'DW_AT_lower_bound':
                try:    subranges.append(('l', int(av)))
                except: pass
            elif ak == 'DW_AT_upper_bound':
                try:    subranges.append(('u', int(av)))
                except: pass
            if in_sub:
                continue
            elif ak == 'DW_AT_type':
                tm = re.search(r'<0x([0-9a-f]+)>', av)
                if tm: cur_attr['_type_ref'] = int(tm.group(1), 16)
            elif ak == 'DW_AT_name':
                nm = re.search(r'\):\s*(.+)', av)
                cur_attr['_name'] = nm.group(1).strip() if nm else av
            elif ak == 'DW_AT_byte_size':
                try:    cur_attr['_byte_size'] = int(av)
                except: pass
            elif ak == 'DW_AT_data_member_location':
                try:    cur_attr['_offset'] = int(av)
                except: pass
            elif ak == 'DW_AT_linkage_name':
                nm = re.search(r'\):\s*(.+)', av)
                cur_attr['_linkage'] = nm.group(1).strip() if nm else av
    if cur_off is not None:
        types[cur_off] = (cur_tag, dict(cur_attr), list(subranges))

    def resolve_type(tref, depth=0):
        if depth > 10 or tref not in types:
            return {}
        tag, attr, subs = types[tref]
        if tag == 'DW_TAG_base_type':
            ct = DWARF_TO_CTYPE.get(attr.get('_name', ''))
            return { 'type': ct, 'size': attr.get('_byte_size', 0) } if ct else {}
        elif tag == 'DW_TAG_string_type':
            return { 'type'   : c_char_p,
                     'is_char': True,
                     'length' : attr.get('_byte_size', 1) }
        elif tag == 'DW_TAG_array_type':
            inner = resolve_type(attr.get('_type_ref', 0), depth + 1)
            dims  = []
            lb    = 1
            for kind, val in subs:
                if   kind == 'c': dims.append(val)
                elif kind == 'l': lb = val
                elif kind == 'u': dims.append(val - lb + 1); lb = 1
            if dims:
                inner['ndims'] = len(dims)
                inner['dims']  = tuple(dims)
            return inner
        elif tag == 'DW_TAG_pointer_type':
            inner = resolve_type(attr.get('_type_ref', 0), depth + 1)
            inner['is_pointer'] = True
            return inner
        elif tag == 'DW_TAG_structure_type':
            return { 'type'      : attr.get('_name', ''),
                     'is_derived': True,
                     'size'      : attr.get('_byte_size', 0) }
        return {}

    prefix    = f'{module_name}_mp_'
    variables = {}
    for off, (tag, attr, subs) in types.items():
        if tag == 'DW_TAG_variable':
            lnk = attr.get('_linkage', '')
            if lnk.startswith(prefix):
                vn   = lnk[len(prefix):-1] if lnk.endswith('_') else lnk[len(prefix):]
                tref = attr.get('_type_ref')
                if tref is not None:
                    variables[vn] = resolve_type(tref)

    type_members = {}
    cur_struct   = None
    for off, (tag, attr, subs) in sorted(types.items()):
        if tag == 'DW_TAG_structure_type':
            sname = attr.get('_name', '')
            if sname.startswith('type_') or sname.startswith('TYPE_'):
                cur_struct = sname.lower()
                if cur_struct not in type_members:
                    type_members[cur_struct] = {}
        elif tag == 'DW_TAG_member' and cur_struct:
            mname = attr.get('_name', '').lower()
            tref  = attr.get('_type_ref')
            info  = resolve_type(tref) if tref else {}
            info['offset'] = attr.get('_offset', -1)
            type_members[cur_struct][mname] = info

    return variables, type_members


def run_test(libpath, modpath):
    module_name = os.path.splitext(os.path.basename(modpath))[0]
    sys.path.insert(0, os.path.join(os.path.dirname(libpath), '..', '..'))
    from dl_py2f import dl_f2py
    lib    = dl_f2py.DL_DL(libpath)
    parsed = lib.parseModule(modpath)
    if parsed is None:
        print('\nparseModule returned None — skipping DWARF comparison')
        return 0
    dwarf_vars, dwarf_types = parse_dwarf(libpath, module_name)

    nerrors = 0
    npass   = 0

    print('\n=== Module-level variable types ===')
    for vn, dinfo in sorted(dwarf_vars.items()):
        pinfo = parsed.get(vn)
        if not isinstance(pinfo, dict):
            continue
        dtype = dinfo.get('type')
        ptype = pinfo.get('_type')
        if dtype and ptype:
            if isinstance(dtype, str):
                if isinstance(ptype, str) and ptype == dtype:
                    npass += 1
            elif dtype == ptype:
                npass += 1
            else:
                print(f'  FAIL type: {vn}: parser={ptype.__name__ if hasattr(ptype,"__name__") else ptype}'
                      f'  DWARF={dtype.__name__}')
                nerrors += 1
        if dinfo.get('is_pointer') and not pinfo.get('_is_pointer'):
            print(f'  FAIL ptr:  {vn}: parser missing _is_pointer (DWARF says POINTER)')
            nerrors += 1
        elif dinfo.get('is_pointer') and pinfo.get('_is_pointer'):
            npass += 1
        if dinfo.get('is_char') and not pinfo.get('_is_char'):
            print(f'  FAIL char: {vn}: parser missing _is_char (DWARF says CHARACTER)')
            nerrors += 1
        elif dinfo.get('is_char') and pinfo.get('_is_char'):
            npass += 1
            dl = dinfo.get('length')
            pl = pinfo.get('_length')
            if dl and pl and dl != pl:
                print(f'  FAIL len:  {vn}: parser _length={pl}  DWARF length={dl}')
                nerrors += 1
            elif dl and pl:
                npass += 1
        ddims = dinfo.get('dims')
        pdims = pinfo.get('_dim')
        if ddims and pdims:
            if tuple(ddims) == tuple(pdims):
                npass += 1
            else:
                print(f'  FAIL dims: {vn}: parser={pdims}  DWARF={ddims}')
                nerrors += 1
        elif ddims and not pdims:
            print(f'  FAIL dims: {vn}: parser missing dims  DWARF={ddims}')
            nerrors += 1

    print('\n=== Type member byte offsets ===')
    parsed_types = {}
    for k, v in parsed.items():
        if isinstance(v, dict) and v.get('_is_derived'):
            parsed_types[k] = v

    for tname, members in sorted(dwarf_types.items()):
        pt = parsed_types.get(tname, {})
        if not pt:
            continue
        for mname, dinfo in sorted(members.items()):
            pm = pt.get(mname)
            if not isinstance(pm, dict):
                continue
            doff = dinfo.get('offset', -1)
            poff = pm.get('_offset', -1)
            if doff >= 0 and poff >= 0:
                if doff == poff:
                    npass += 1
                else:
                    print(f'  FAIL offset: {tname}.{mname}: parser={poff}  DWARF={doff}')
                    nerrors += 1

    print(f'\n{"="*50}')
    print(f'  PASSED: {npass}')
    print(f'  FAILED: {nerrors}')
    print(f'{"="*50}')
    return nerrors


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <libexample.so> <yourmodule.mod>')
        sys.exit(1)
    sys.exit(run_test(sys.argv[1], sys.argv[2]))
