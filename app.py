from flask import Flask, render_template, request, send_file
import qrcode
import os
from io import BytesIO

app = Flask(__name__)

# Rota principal para a interface
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        
        # Gerar QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill="black", back_color="white")
        
        # Salvar o QR Code em memória
        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        
        return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="qrcode.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)