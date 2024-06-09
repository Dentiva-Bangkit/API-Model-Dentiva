from flask import Flask, request, jsonify
from keras.models import load_model
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from io import BytesIO
import google.generativeai as genai
from google.cloud import storage
import uuid
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
genai.configure(api_key= os.getenv('GEMINI_API'))
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(enable_automatic_function_calling=True)
storage_client = storage.Client()
image_bucket = storage_client.get_bucket('dentiva-storage')

def req(y_true, y_pred):
    req = tf.metrics.req(y_true, y_pred)[1]
    tf.keras.backend.get_session().run(tf.local_variables_initializer())
    return req

def predict_image(image_file):
    image = load_img(image_file, target_size=(299, 299))
    image_array = img_to_array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return model.predict(image_array)

label_names = {
    0: 'Karang Gigi', 1: 'Karies', 2: 'Gingivitis',
    3: 'Sariawan', 4: 'Perubahan Warna Gigi',
    5: 'Hipodontia', 6: 'Normal'
}

model = load_model('modeldentiva.h5', custom_objects={'req': req})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            response = jsonify({'message': 'No file part in the request'})
            response.status_code = 400
            return response
        
        file = request.files['file']
        
        if file.filename == '':
            response = jsonify({'message': 'No selected file'})
            response.status_code = 400
            return response

        if file:
            try:
                img_bytes = file.read()
                img_file = BytesIO(img_bytes)
                preds = predict_image(img_file)
                confidence = np.max(preds) * 100
                result = {
                    'tingkat_akurat': f'{confidence:.2f}%',
                    'jenis_penyakit': label_names[np.argmax(preds)],
                }

                filename = f"predictions/{uuid.uuid4()}.jpg"
                blob = image_bucket.blob(filename)
                blob.upload_from_string(img_bytes, content_type=file.content_type)

                response = jsonify(result)
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({'message': f'Error processing image file: {str(e)}'})
                response.status_code = 500
                return response
    
    return 'OK'

@app.route('/suggestion', methods=['POST'])
def suggestion():
    try:
        data = request.get_json()
        disease = data.get('disease')
        responseGemini = chat.send_message(f'Berikan saya saran serta cara penanganan penyakit {disease}')
        return jsonify({'message': f'{responseGemini.text}'})
    except Exception as e:
        response = jsonify({'message': 'Ada kesalahan pada server'})
        response.status_code = 500
        return response

@app.route('/all', methods=['POST'])
def predictAndSuggestion():
    if request.method == 'POST':
        if 'file' not in request.files:
            response = jsonify({'message': 'No file part in the request'})
            response.status_code = 400
            return response
        
        file = request.files['file']
        
        if file.filename == '':
            response = jsonify({'message': 'No selected file'})
            response.status_code = 400
            return response

        if file:
            try:
                img_bytes = file.read()
                img_file = BytesIO(img_bytes)
                preds = predict_image(img_file)
                confidence = np.max(preds) * 100
                result = {
                    'tingkat_akurat': f'{confidence:.2f}%',
                    'jenis_penyakit': label_names[np.argmax(preds)],
                    'saran': chat.send_message(f'Berikan saya saran serta cara penanganan penyakit {label_names[np.argmax(preds)]}').text
                }

                filename = f"predictions/{uuid.uuid4()}.jpg"
                blob = image_bucket.blob(filename)
                blob.upload_from_string(img_bytes, content_type=file.content_type)

                response = jsonify(result)
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({'message': f'Error processing image file: {str(e)}'})
                response.status_code = 500
                return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=(os.environ.get("PORT",8080)))
