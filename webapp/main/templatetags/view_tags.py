from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def pssms_to_js(motifs):
    if len(motifs) == 0:
        return ""
    result = """$(document).ready(function() {
      var alphabet = ['A', 'G', 'C', 'T'];
      var canvasOptions = {
        width: 300,
        height: 200,
        glyphStyle: '20pt Helvetica'
      };
"""
    for i, m in enumerate(motifs):
        rows = [("          [%f, %f, %f, %f]" % (row.a, row.g,
                                                 row.c, row.t))
                for row in m.pssm_set.all().order_by('index')]
        result += """
      var pssm_%d = {
        alphabet: alphabet,
        values: [
""" % i
        result += ",\n".join(rows)
        result += """
        ]
      };
      isblogo.makeLogo('canvas_%d', pssm_%d, canvasOptions);
    });
""" % (i, i)
    return mark_safe(result)

@register.filter
def motif_info(motif):
    print "# assoc genes: ", motif.gene_set.count()
    return "info here"

@register.filter
def format_scientific(d):
    return "%.2e" % d

@register.filter
def hist_to_js(hist_data):
    result = """{
      minValue: %d,
      maxValue: %d,
      refValue: %d,
      values: [%s]
};""" % (hist_data.minval, hist_data.maxval, hist_data.refval,
         ', '.join([str(v) for v in hist_data.data]))
    return mark_safe(result)
