from jinja2 import Environment, FileSystemLoader
import os 

cwd = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(cwd, 'templates')

class TemplateRenderer:
    def __init__(self) -> None:
        environment = Environment(loader=FileSystemLoader(template_dir))
        environment.lstrip_blocks = True
        environment.trim_blocks = True
        self.email_template = environment.get_template("email.html")

    def render_html(self, data: dict) -> str:
        html = self.email_template.render(data)
        html = html.replace('\n', '') 
        f = open("C:\\Users\\weixzha\\Desktop\\a.html", "w")
        f.write(html)
        f.close()

        return html

