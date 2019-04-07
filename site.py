from flask import Flask, render_template, redirect
from flask_flatpages import FlatPages
from flaskext.markdown import Markdown
from flask.ext.assets import Environment as AssetManager
from flask_frozen import Freezer


# configuration
DEBUG = False
ASSETS_DEBUG = DEBUG
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'pages'
FREEZER_RELATIVE_URLS = True


app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)
markdown_manager = Markdown(app, extensions=['fenced_code'], output_format='html5',)
asset_manager = AssetManager(app)

@app.route('/')
def index():
    return render_template('index.html', pages=pages)

@app.route('/<path:path>/')
def page(path):
    return pages.get_or_404(path).html

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        app.debug = False
        asset_manager.config['ASSETS_DEBUG'] = False
        freezer.freeze()
    elif len(sys.argv) > 1 and sys.argv[1] == "serve":
        freezer.serve()
    else:
        app.run(port=8000)