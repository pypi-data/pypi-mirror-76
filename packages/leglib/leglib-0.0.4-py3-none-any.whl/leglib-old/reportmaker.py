import jinja2
from jinja2 import Template
from leglib import fmt
from leglib import latex
from jinja2.utils import contextfunction
import numbers
import math

searchpath = ["./", "/media/family/GoogleOne/Tools/"]


def _get_context(locals, names):
    name_set = set(locals.keys()).intersection(names)
    context = dict.fromkeys(name_set, 0.0)
    for k in context.keys():
        if type(locals[k]) == float:
            context[k] = fmt.SigdigFloat(locals[k])
        else:
            context[k] = locals[k]
    return context


def make_report(locals, names, template_filename):
    context = _get_context(locals, names)
    make_report_from_context(context, template_filename)


def fixed3(value):
    return fmt.fixed(value, 3)


@contextfunction
def formula(context, answervar, eq, units=""):
    #import pdb; pdb.set_trace()

    vars = [symb for symb in list(context.keys()) if len(
        symb) <= 4 and isinstance(context[symb], numbers.Number)]
    latex_vars = []
    vars.sort(key=len, reverse=True)  # sorts by descending length
    eq0 = eq
    latex_answervar = answervar
    for var in vars:
        if len(var) == 1:
            latex_vars.append((var, var))
        elif len(var) == 2:
            newvar = "%s_%s" % (var[0], var[1])
            latex_vars.append((var, newvar))
        else:
            newvar = "%s_{%s}" % (var[0], var[1:])
            latex_vars.append((var, newvar))
        if answervar == var:
            latex_answervar = newvar
    for lv in latex_vars:
        name = lv[1]
        val = fmt.sigdig(context[lv[0]], 4)
        eq = eq.replace(name, "(%s)" % val)
    eq = "$" + latex_answervar + " = " + eq0 + " = " + eq + \
        " = %s$ " % fmt.sigdig(context[answervar], 3) + units
#    import pdb; pdb.set_trace()
    return eq


def make_report_from_context(context, template_filename):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(
        loader=templateLoader, comment_start_string="<!--", comment_end_string="-->")
    templateEnv.globals.update(f=formula)
    templateEnv.filters["s"] = fmt.sigdig
    templateEnv.filters["f"] = fmt.fixed
    templateEnv.filters["f3"] = fixed3
    templateEnv.filters["i"] = fmt.integer
    templateEnv.filters["in"] = fmt.inches_decimal
    templateEnv.filters["int"] = int
    template = templateEnv.get_template(template_filename)
    outputText = template.render(context)
    print(outputText)
