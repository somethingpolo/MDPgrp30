import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import *
from test2 import process_image
from algo.algo import Algo
from PIL import Image
<<<<<<< Updated upstream
from PIL import Image, ImageDraw
=======
from imutils import paths
import numpy as np
import imutils
import cv2
>>>>>>> Stashed changes

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
    file.save(os.path.join('images', filename))
    orig_image = Image.open(f'images/{filename}')
    new_image = orig_image.transpose(method=Image.FLIP_TOP_BOTTOM)
    new_image = new_image.transpose(method=Image.FLIP_LEFT_RIGHT)
<<<<<<< Updated upstream
    # inference the image
    image_label, image_bbox = process_image(f"images/{filename}")
    viz_result = draw_box(new_image, image_label, image_bbox)
    viz_result.save(f"images/{filename}")
    result = {
        "image_id": image_label
    }
=======
    new_image.save(f"images/{filename}")
    image_id = process_image(f"images/{filename}")
    result = {"image_id": image_id}
>>>>>>> Stashed changes

    return jsonify(result)


@app.route('/path', methods=['POST'])
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
    result = {"commands": commands}
    return jsonify(result)


@app.route('/stitch', methods=['GET'])
def stitch_images():
    # grab the paths to the input images and initialize our images list
    print("[stitch] loading images...")
    image_folder = sorted(list(paths.list_images("images")))
    images = []
    index = 0
    # loop over the image paths, load each one, and add them to our
    # images to stitch list
    for image in image_folder:
        target = Image.open(image)
        images.append({f"img{index+1}": target, "size": target.size})
        index += 1
    total_width = 0
    heights = []
    for i in range(len(images)):
        heights.append(images[i]["size"][1])
    total_height = max(heights)
    for image in images:
        total_width += image.get('size')[0]
    stitched = Image.new('RGB', (total_width, total_height))
    index = 0
    width = 0
    for image in images:
        stitched.paste(im=image[f"img{index+1}"], box=(width,0))
        width += image.get('size')[0]
        index += 1
    stitched.save("images/stitched.jpg")
    return "okay"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
