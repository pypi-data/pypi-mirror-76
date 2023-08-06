from structural import report
import util


class Project(object):

    def __init__(self, name="Unnamed Project", number=None, desc=None,
            is_metric=False):
        self.name = name
        self.number = number
        self.desc = desc
        self.calcs = {}
        self.is_metric = is_metric

    def __unicode__(self):
        if self.number is not None:
            return "%s - %s" % (self.number, self.name)
        else:
            return "%s" % (self.name)

    def __str__(self):
        return self.__unicode__()

    def timestamp(self):
        return util.timestamp()

    def _next_name(self, class_name):
        i = 1
        candidate_name = "%s%d" % (class_name, i)
        while candidate_name in list(self.calcs.keys()):
            i = i + 1
            candidate_name = "%s%d" % (class_name, i)
        return candidate_name

    def add_calc(self, calc, name=None):
        "Add a component to a project"
        if name is None:
            name = self._next_name(calc.__class__.__name__)
        calc.name = name
        self._update_calc(calc)
        self.calcs[name] = calc
        return calc

    def del_calc(self, name):
        "Delete a calc"
        if name in self.calcs:
            del self.calcs[name]
            return True
        else:
            return False

    def _update_calc(self, calc):
        attribs = ( )
        calc.project = self
        # Update calc project
        if hasattr(calc, "project"):
            calc.project = self
        for a in attribs:
            if hasattr(calc, a):
                calc.__dict__[a] = self.__dict__[a]

    def recalc(self, calc_name=None):
        "Recalculate all owned calcs"
        if calc_name is not None:
            if calc_name in self.calcs:
                # Recalculate one identified calc
                self._update_calc(self.calcs[calc_name])
                self.calcs[calc_name].recalc()
                return True
            else:
                return False
        else:
            # Recalculate all
            for calc in list(self.calcs.values()):
                self._update_calc(calc)
                calc.recalc()
            return True

    def render(self, template_type="txt"):
        return report.Report(self).render(template_type)


    def write(self, filename, template_type="txt", overwrite=False):
        report.Report(self).write(filename, template_type, overwrite)

