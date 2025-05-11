from flask import Flask, request, render_template_string
import asyncio
import trafilatura
from playwright.async_api import async_playwright
from openai import OpenAI
import os

app = Flask(__name__)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
USER_AGENT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"de\">
<head>
    <meta charset=\"UTF-8\">
    <title>Paywall Remover</title>
</head>
<body style=\"font-family:Arial; padding: 30px\">
    <h1>AI Paywall-Umgehung</h1>
    <form method=\"post\">
        <label for=\"url\">Artikel-URL:</label><br>
        <input type=\"text\" name=\"url\" style=\"width: 60%; padding: 8px\" required>
        <button type=\"submit\">Analysieren</button>
    </form>
    <hr>
    %s
</body>
</html>
"""

async def render_and_extract(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(user_agent=USER_AGENT)
        page = await context.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(3000)
        html = await page.content()
        await browser.close()
        return trafilatura.extract(html, include_comments=False)

async def gpt_summary(text):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Fasse folgenden Artikel strukturiert zusammen (HTML mit h2, p, ul):\n\n{text}"}
        ]
    )
    return response.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            content = asyncio.run(render_and_extract(url))
            html_output = asyncio.run(gpt_summary(content))
            return render_template_string(HTML_TEMPLATE % html_output)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE % f"<p style='color:red'>Fehler: {str(e)}</p>")
    return render_template_string(HTML_TEMPLATE % "")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
