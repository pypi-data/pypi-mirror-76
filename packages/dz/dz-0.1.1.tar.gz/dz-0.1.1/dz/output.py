import json as json_module
import humanize
import tabulate
import sys
tabulate.WIDE_CHARS_MODE = False

GoodStyle = tabulate.TableFormat(
    lineabove=tabulate.Line("", "-", "  ", ""),
    linebelowheader=None,
    linebetweenrows=None,
    linebelow=tabulate.Line("", "-", "  ", ""),
    headerrow=tabulate.DataRow("", "  ", ""),
    datarow=tabulate.DataRow("", "  ", ""),
    padding=0,
    with_header_hide=["lineabove", "linebelow"],
)

class Table():
    fields = []
    byte_fields = []
    default_fields = []
    default_sort = []

    def __init__(self, data):
        self.data = data
    
    def write(self, output = None, sort = None, json = None, **kwargs):
        print_fields = self._parse_fields(output, self.default_fields)
        sort_by = self._parse_fields(sort, self.default_sort)

        data = sorted(self.data, key=lambda x: tuple(x[s] for s in sort_by))
        if json:
            print(json_module.dumps(list(data),indent=2))
            return

        t = []
        for h in data:
            row = []
            for f in print_fields:
                if f in self.byte_fields:
                    row += [humanize.naturalsize(h[f])]
                else:
                    row += [h[f]]
            t += [row]
        print(tabulate.tabulate(t, headers=[hdr.upper() for hdr in print_fields], tablefmt = GoodStyle))

    def _parse_fields(self, fields = None, default = None):
        if not fields:
            return default
        if fields == 'all':
            return self.fields
        fields = fields.split(',')
        fields_set = set(fields)
        choices_set = set(self.fields)
        if not fields_set.issubset(choices_set):
            print("Unknown field(s):", ','.join(fields_set - choices_set))
            sys.exit(-1)
        return fields
