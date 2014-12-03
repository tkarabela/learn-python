"""
Regex testing

References:
http://flask.pocoo.org/docs/0.10/quickstart/
http://jinja.pocoo.org/docs/dev/templates/
https://docs.python.org/3/library/re.html

"""

import re
import html

from flask import Flask, request, render_template, url_for


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pattern = request.form["pattern"]
        text = request.form["text"]
        flags = (re.IGNORECASE * ("ignorecase" in request.form)) | \
                (re.MULTILINE * ("multiline" in request.form))

        highlighter = lambda m: "<b>" + html.escape(m.group(0)) + "</b>"
        highlighted_text = re.sub(pattern, highlighter, text, flags=flags)

        return render_template("index.html", show_result=True, pattern=pattern, highlighted_text=highlighted_text, text=text)
    else:
        return render_template("index.html", show_result=False)


if __name__ == "__main__":
    app.debug = True
    app.run()
