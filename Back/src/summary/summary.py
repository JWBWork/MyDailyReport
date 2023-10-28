from pathlib import Path
from dataclasses import dataclass
import openai

# @dataclass
class Summary:
    template_dir = Path(__file__).parent / "templates"

    def load_template(self, template: str):
        template_path = self.template_dir / f"{template}.txt"
        with open(template_path, "r") as template_file:
            template = template_file.read()
        return template 

    def render_template(self, template: str, **kwargs):
        template = self.load_template(template)
        return template.format(**kwargs)

    def get_summary(self, template: str, **kwargs):
        prompt = self.render_template(template, **kwargs)
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0]['message']['content']
