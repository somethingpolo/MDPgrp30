import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import *
from test2 import process_image
from algo.algo import Algo
from PIL import Image
from PIL import Image, ImageDraw

app = Flask(__name__)
CORS(app)


def draw_box(image, label, bbox):
    x1, y1, x2, y2 = bbox
    draw = ImageDraw.Draw(image)
    # add label
    font_size = 18  # You can adjust the size as needed
    font = ImageFont.truetype("Arial Bold.ttf", font_size)
    # Calculate text size

    # Calculate text position to be above the bounding box
    text_x = x1
    text_y = y1 - font_size - 5  # Adjust the 5 pixels offset as needed

    # Draw the label above the bounding box
    draw.text((text_x, text_y), label, fill="red", font=font)
    # add bbox
    draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

    return image


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
    # inference the image
    image_label, image_bbox = process_image(f"images/{filename}")
    viz_result = draw_box(new_image, image_label, image_bbox)
    viz_result.save(f"images/{filename}")
    result = {
        "image_id": image_label
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
