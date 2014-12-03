"""
Directory listing

References:
http://flask.pocoo.org/docs/0.10/quickstart/
http://jinja.pocoo.org/docs/dev/templates/
https://docs.python.org/3/library/os.html
https://docs.python.org/3/library/os.path.html
https://docs.python.org/3/library/stat.html

"""

import os
import os.path as op
import stat

from flask import Flask, url_for, render_template


app = Flask(__name__)


@app.route("/filesystem/")
@app.route("/filesystem/<path:directory>")
def filesystem(directory="/"):
    if op.isdir(directory):
        entries = {}
        for entry in os.listdir(directory):
            d = {}
            d["fullpath"] = fullpath = op.join(directory, entry)
            try:
                s = os.stat(fullpath)
                d["size"] = s.st_size
                d["is_dir"] = stat.S_ISDIR(s.st_mode)
            except OSError:
                app.logger.warning("os.stat failed on file %r", fullpath)

            entries[entry] = d

        return render_template("directory.html", directory=directory, entries=entries)
    else:
        msg = "No such directory as <b>%s</b>!" % directory
        return render_template("error.html", message=msg, directory=directory)


@app.route("/")
def index():
    msg = "Nothing to see here, have a look <a href='%s'>here</a> instead." % url_for("filesystem")
    return render_template("error.html", message=msg)


if __name__ == "__main__":
    app.debug = True
    app.run()
