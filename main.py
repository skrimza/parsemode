from flask import Flask
from handlers import router
import asyncio
from parse.parse_files import Parser



app = Flask(__name__)

app.register_blueprint(blueprint=router, url_prefix='/router')

app.static_folder = 'media/static'
app.template_folder = 'templates'

if __name__ == '__main__':
    # Parser().parse_product()
    app.run(debug=True)