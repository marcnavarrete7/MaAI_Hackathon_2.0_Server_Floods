from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "secret123"  # Required for flashing messages

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"zip"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure root folder exists

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    username = request.args.get("username")
    if not username:
        flash("No username provided.")
        return redirect(url_for("home"))

    user_folder = os.path.join(app.config["UPLOAD_FOLDER"], username)
    os.makedirs(user_folder, exist_ok=True)

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(user_folder, file.filename))
            flash("File uploaded successfully!")
            return redirect(url_for("upload", username=username))

        flash("Invalid file type. Only .zip files are allowed.")
        return redirect(request.url)

    # For GET: List user's uploaded files
    user_files = os.listdir(user_folder) if os.path.exists(user_folder) else []
    return render_template("upload.html", user_files=user_files, username=username)

@app.route('/uploads/<username>/<filename>')
def uploaded_file(username, filename):
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], username), filename)

if __name__ == "__main__":
    app.run(debug=True)
