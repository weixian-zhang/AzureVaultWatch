from jinja2 import Environment, FileSystemLoader
import os 
from opentelemetry.trace import Tracer

cwd = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(cwd, 'templates')

class TemplateRenderer:
    def __init__(self, otel_tracer: Tracer) -> None:
        self.otel_tracer = otel_tracer
        environment = Environment(loader=FileSystemLoader(template_dir))
        environment.lstrip_blocks = True
        environment.trim_blocks = True
        self.email_template = environment.get_template("email.html")

    def render_html(self, data: dict) -> str:
        
        with self.otel_tracer.start_as_current_span('TemplateRenderer.render_html') as cs:
            html = self.email_template.render(data)
            html = html.replace('\n', '')

            cs.add_event('finish TemplateRenderer.render_html')

            return html
    


        

