from os import read
from flask import Flask, json, jsonify, request, abort, send_file
from pathlib import Path

app = Flask(__name__)

class Anchor:
    def __init__(self, id, image_url, width_cm, height_cm, position, orientation, is_setup, is_origin):
        self.id = id
        self.image_url = image_url
        self.width_cm = width_cm
        self.position = position
        self.height_cm = height_cm
        self.position = position
        self.orientation = orientation
        self.is_setup = is_setup
        self.is_origin = is_origin

    def save(self):
        json_path = Path.cwd() / 'data' / 'anchors' / (self.id + '.json')
        with json_path.open('w') as file:
            json.dump(self.__dict__, file)

@app.route('/anchors')
def get_anchor_list():
    anchor_file_list = (Path.cwd() / 'data' / 'anchors').glob('*.json')
    anchors = []
    for anchor_file in anchor_file_list:
        with anchor_file.open('r') as file:
            anchors.append(Anchor(**json.load(file)))
    return jsonify({
        'anchors': [a.__dict__ for a in anchors]  
    })

@app.route('/create_anchor', methods=['POST'])
def create_anchor():
    anchor = Anchor(**request.get_json())
    anchor.save()
    return jsonify({
        'anchors': [
            anchor.__dict__
        ]
    })

@app.route('/image/<filename>')
def get_image(filename):
    image_path = Path.cwd() / 'data' / 'images' / filename
    return send_file(image_path, mimetype='image/jpeg')




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)

