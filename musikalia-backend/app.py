from flask import Flask, request, jsonify
import boto3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Configuración de Wasabi (reemplaza con tus datos reales)
WASABI_ACCESS_KEY = os.getenv("WASABI_ACCESS_KEY")
WASABI_SECRET_KEY = os.getenv("WASABI_SECRET_KEY")
WASABI_BUCKET = os.getenv("WASABI_BUCKET")
WASABI_ENDPOINT = "s3.us-west-1.wasabisys.com"  # puede cambiar según tu región

# Cliente de S3 con Wasabi
s3_client = boto3.client(
    's3',
    endpoint_url=f'https://{WASABI_ENDPOINT}',
    aws_access_key_id=WASABI_ACCESS_KEY,
    aws_secret_access_key=WASABI_SECRET_KEY
)

@app.route('/api/subir-musico', methods=['POST'])
def subir_videos_musico():
    try:
        nombre = request.form.get('nombreArtistico')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        urls = []

        for i in range(5):
            file_key = f"video_{i}"
            if file_key in request.files:
                file = request.files[file_key]
                filename = secure_filename(file.filename)
                s3_key = f"videos/{nombre}_{timestamp}_{i}_{filename}"

                # Subir a Wasabi
                s3_client.upload_fileobj(
                    file,
                    WASABI_BUCKET,
                    s3_key,
                    ExtraArgs={"ContentType": file.content_type}
                )

                # URL pública (solo si el bucket es público)
                url = f"https://{WASABI_BUCKET}.{WASABI_ENDPOINT}/{s3_key}"
                urls.append(url)

        return jsonify({"status": "ok", "videos": urls}), 200

    except Exception as e:
        print("Error en subida:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
