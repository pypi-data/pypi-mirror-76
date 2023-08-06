from filters import dim, distance, fixed, length, ft_in, mult, sigdig
from filters import ft_in_from_ft, distance_from_ft, check
from jinja2 import Environment
from jinja2 import FileSystemLoader
import os


class Report:

    def __init__(self, member):
        self.member = member

    def render(self, template_type="txt"):
        base_path = os.path.split(os.path.abspath(__file__))[0]
        template_path = os.path.join(base_path, "templates/%s" % template_type)
        loader = FileSystemLoader(template_path)
        env = Environment(loader=loader)
        env.filters["dim"] = dim
        env.filters["distance"] = distance
        env.filters["distance_from_ft"] = distance_from_ft
        env.filters["fixed"] = fixed
        env.filters["ft_in"] = ft_in
        env.filters["ft_in_from_ft"] = ft_in_from_ft
        env.filters["length"] = length
        env.filters["mult"] = mult
        env.filters["sigdig"] = sigdig
        env.filters["check"] = check
        template_filename = r"%s.%s" % (self.member.__class__.__name__, template_type)
        template = env.get_template(template_filename)
        return template.render(m=self.member)

    def write(self, filename, template_type="txt", overwrite=False):
        if os.path.exists(filename) and not overwrite:
            raise IOError("File %s exists.  Set overwrite=True to over-write.")
        with open(filename, "wt") as f:
            f.write(self.render(template_type))
            f.close()

