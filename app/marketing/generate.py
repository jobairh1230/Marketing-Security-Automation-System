import requests
from app.marketing.schema import MarketingContent
from app.marketing import load_prompt_yaml, render_user_template
from dotenv import load_dotenv
import os
from app.marketing.generate import generate_marketing_content
from app.marketing.load_prompt_yaml import load_prompt_yaml

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def generate_marketing_content(prompt_file: str, content_type: str, brief: str, audience: str, goal: str, offer: str):
    prompt = load_prompt_yaml(prompt_file)
    sys = prompt["template"]["system"]
    user_tmpl = prompt["template"]["user"]

    user_text = render_user_template(user_tmpl, {
        "brief": brief,
        "audience": audience,
        "goal": goal,
        "offer": offer,
    })

    response = requests.post(
        "https://api-inference.huggingface.co/models/gpt-2",  # example model
        headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        json={"inputs": sys + "\n" + user_text}
    )

    content = response.json()['choices'][0]['text']
    return MarketingContent(content_type=content_type, title=content, body=content, cta="Click here to learn more", risk_flags=["None"])
