from flask import Flask, render_template, request
import base64
import os
import face
import pandas as pd
import shutil

def create_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

create_folder('uploads')

attendance_path = os.path.join('artifacts','attendance.csv')

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/capture',methods=['GET'])
def home():
    return render_template('capture.html')

@app.route('/attendance',methods=['GET'])
def attendance():
    face.take_attendance()
    return render_template('attendance.html')

@app.route('/upload', methods=['POST'])
def upload():
    image_name = request.json['name']
    image_data = request.json['data']
    _, encoded = image_data.split(',', 1)
    binary_data = base64.b64decode(encoded)
    image_path = os.path.join('uploads', image_name + '.jpg')
    with open(image_path, 'wb') as f:
        f.write(binary_data)
    return render_template('capture.html') 

@app.route('/see_details',methods=['GET', 'POST'])
def details():
    print(attendance_path)
    df = pd.read_csv(attendance_path)
    data = []
    for i in range(df.shape[0]):
        name = df['Name'][i]
        time = str(df['Time'][i])
        data.append([name, time])
    print(data)
    return render_template('details.html', results = data , results2 = len(data) )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
