from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "secret123"  # required for flashing messages

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"zip"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # create the folder if it doesn't exist

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            flash("File uploaded successfully!")
            return redirect(url_for("upload"))

        flash("Invalid file type. Only .zip files are allowed.")
        return redirect(request.url)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)