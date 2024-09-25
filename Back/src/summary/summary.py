import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import openai
from loguru import logger


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
        # logger.info(f"Prompt:\n\n{prompt}")

        # TODO put logging path behind env variable?
        prompt_history_dir = Path().resolve() / 'prompt_history'
        prompt_history_dir.mkdir(exist_ok=True)
        prompt_history_path = prompt_history_dir / f"{datetime.now().isoformat()}.txt"
        with open(prompt_history_path, "w+") as prompt_history_file:
            prompt_history_file.write(prompt)

        r = openai.ChatCompletion.create(
            model=os.environ['MODEL_NAME'],
            messages=[{"role": "user", "content": prompt}]
        )

        return r.choices[0]['message']['content']
