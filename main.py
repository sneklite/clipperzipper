from flask import Flask, render_template, url_for
from clipperzipper import Messages as ClipZip
import logging
import os

app = Flask(__name__)


@app.route('/')
@app.route('/<channel>/<usernames>/<time>/<int:mentions>')
def index(channel=None, usernames=None, time=None, mentions=True):
    logstxt = "Logs should appear here!"
    if channel and usernames and time:
        mmap = {1: True, 0: False}
        if mentions in mmap.keys():
            mentions = mmap[mentions]
        else:
            return render_template('404.html'), 404
        usernames = usernames.split("+")
        logstxt = ClipZip.clipperzipper(channel, usernames, time, mentions)
        if logstxt == "":
            logstxt = "no logs found for this request."
    return render_template("index.html", logstxt=logstxt)


# to deal with cached static css page:
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.errorhandler(404)
def page_not_found(e):
    logging.debug(e)
    return render_template('404.html'), 404

if __name__ == "__main__":
    # runs off port 5000
    app.run(debug=True)
