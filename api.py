import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import *
from test2 import process_image
from algo.algo import Algo
from PIL import Image

app = Flask(__name__)
CORS(app)

model = None

@app.route('/status', methods=['GET'])
def status():

    return jsonify({"result": "ok"})

@app.route('/image', methods=['POST'])
def predict_image():
    file = request.files['files']
    filename = file.filename
    file.save(os.path.join('images',filename))
    orig_image = Image.open(f'images/{filename}')
    new_image = orig_image.transpose(method=Image.FLIP_TOP_BOTTOM)
    new_image = new_image.transpose(method=Image.FLIP_LEFT_RIGHT)
    new_image.save(f"images/{filename}")
    image_id = process_image(f"images/{filename}")
    result = {
        "image_id": image_id
    }

    return jsonify(result)


@app.route('/path',methods=['POST'])
def get_pathing():
    # take in 'done' signal from pi
    # proceed to next action
    # row, column, direction (take from android bluetooth)
    # this api gives next action
    #message = request.data["algo"]
    #message = jsonify(request.data)
    algo = Algo()
    # ['SF090']
    commands = algo.run_task1(request.form.get('algo'))
    result = {
        "commands":commands
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)