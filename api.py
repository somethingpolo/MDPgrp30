import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import *
from test2 import process_image
from algo.algo import Algo
from PIL import Image
from mmdet.apis import inference_detector, init_detector
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
CORS(app)


classes = ['0_Bulls Eye', '11_1', '12_2', '13_3', '14_4', '15_5', '16_6', '17_7',
            '18_8', '19_9', '20_A', '21_B', '22_C', '23_D', '24_E', '25_F', '26_G',
            '27_H', '28_S', '29_T', '30_U', '31_V', '32_W', '33_X', '34_Y', '35_Z',
            '36_Up', '37_Down', '38_Right', '39_Left', '40_Stop']

# load model
config = './configs/mdp/mdpv30.py'
checkpoint = './work_dirs/mdpv30/epoch_300.pth'
model = init_detector(config, checkpoint, device='cpu')

def draw_box(image, result):
    x1, y1, x2, y2 = result.pred_instances.bboxes[0] 
    label = classes[result.pred_instances.labels[0]]
    draw = ImageDraw.Draw(image)
    draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
    draw.text((x1, y1 - 10), label, fill="red")
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
    result = inference_detector(model, new_image)
    viz_result = draw_box(new_image, result)
    viz_result.save(f"images/{filename}")
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
