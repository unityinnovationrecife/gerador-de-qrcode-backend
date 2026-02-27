from flask import Flask, jsonify, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route("/generate_qrcode", methods=["POST"])
def generate_qrcode():
    data = request.json.get("url")
    if not data:
        return jsonify({"error": "URL is required"}), 400

    # Gerar o QR Code
    qr = qrcode.QRCode(
        version=2, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4
        )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="UNIR-qrcode.png")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
