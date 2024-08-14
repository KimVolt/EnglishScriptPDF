from flask import Flask
import json

from modules import init_routes

app = Flask(__name__)

# 라우트 초기화
init_routes(app)

if __name__ == '__main__':
    with open('chat_data.json', 'w') as file:
        json.dump({}, file)
    app.run(debug=True)
