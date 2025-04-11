from flask import Flask
from handlers import router
import asyncio
from parse.parse_files import Parser
from filereader import FrameJson


app = Flask(__name__)

app.register_blueprint(blueprint=router, url_prefix='/router')

app.static_folder = 'media/static'
app.template_folder = 'templates'

async def main():
    frame_json = FrameJson()
    frame_json.from_excel()
    parser = Parser()
    results = await parser.parser_data()
    for result in results:
        print(result)

if __name__ == '__main__':
  app.run(debug=True)
  asyncio.run(main())