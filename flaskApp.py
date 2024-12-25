from flask import Flask, render_template, jsonify, request
import langModel

app = Flask(__name__)

@app.route('/',methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/api/function', methods=['POST'])
def call_function():
    text = request.data.decode("utf-8")
    print(text) # Запрос пользователя

    ### Обработка запроса
    result = langModel.query(text)
    return jsonify({ 'message': str(result)})


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = '8080', debug = True)