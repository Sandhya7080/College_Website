import json
import os
import uuid
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "owner")
OWNER_PASSWORD = os.environ.get("OWNER_PASSWORD", "Owner@123")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif", "svg"}

DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


DEFAULT_FACULTY = [
    {
        "id": "sample-faculty-1",
        "name": "सुनिता पाटील मॅडम",
        "subject": "मराठी विभाग",
        "description": "विद्यार्थ्यांच्या भाषिक कौशल्यांवर विशेष भर देणाऱ्या अनुभवी शिक्षिका.",
        "photo": "/static/images/faculty-1.svg",
    },
    {
        "id": "sample-faculty-2",
        "name": "राजेश देशमुख सर",
        "subject": "गणित विभाग",
        "description": "सोप्या पद्धतीने संकल्पना समजावून सांगणारे गणित विषयाचे मार्गदर्शक.",
        "photo": "/static/images/faculty-2.svg",
    },
    {
        "id": "sample-faculty-3",
        "name": "माया जाधव मॅडम",
        "subject": "विज्ञान विभाग",
        "description": "प्रयोगशील शिक्षणातून विज्ञानाची आवड निर्माण करणाऱ्या शिक्षिका.",
        "photo": "/static/images/faculty-3.svg",
    },
    {
        "id": "sample-faculty-4",
        "name": "विनोद शिंदे सर",
        "subject": "सामाजिक शास्त्र",
        "description": "इतिहास, भूगोल आणि सामाजिक जाणीव यांचा सुंदर संगम घडवणारे शिक्षक.",
        "photo": "/static/images/faculty-4.svg",
    },
    {
        "id": "sample-faculty-5",
        "name": "प्रिया काळे मॅडम",
        "subject": "इंग्रजी विभाग",
        "description": "आत्मविश्वासाने इंग्रजी बोलणे आणि लिहिणे शिकवणाऱ्या शिक्षिका.",
        "photo": "/static/images/faculty-5.svg",
    },
    {
        "id": "sample-faculty-6",
        "name": "अमोल मोरे सर",
        "subject": "क्रीडा विभाग",
        "description": "क्रीडा, शिस्त आणि आरोग्यदायी जीवनशैलीसाठी विद्यार्थ्यांना प्रेरणा देणारे शिक्षक.",
        "photo": "/static/images/faculty-6.svg",
    },
]

DEFAULT_ALUMNI = [
    {
        "id": "sample-alumni-1",
        "name": "सचिन राऊत",
        "profession": "शेतकरी व उद्योजक",
        "description": "विद्यालयातून घेतलेल्या संस्कारांमुळे समाजात स्वतःची ओळख निर्माण केली.",
        "photo": "/static/images/faculty-2.svg",
    },
    {
        "id": "sample-alumni-2",
        "name": "माजी विद्यार्थी",
        "profession": "सॉफ्टवेअर अभियंता",
        "description": "तंत्रज्ञान क्षेत्रात कार्यरत असलेले विद्यालयाचे माजी विद्यार्थी.",
        "photo": "/static/images/faculty-4.svg",
    },
    {
        "id": "sample-alumni-3",
        "name": "माजी विद्यार्थी",
        "profession": "पोलीस अधिकारी",
        "description": "शिस्त आणि सेवाभाव जपणारे विद्यालयाचे अभिमान.",
        "photo": "/static/images/faculty-6.svg",
    },
]

DEFAULT_SCORES = [
    {
        "id": "sample-score-1",
        "name": "विद्यार्थी नाव",
        "class_name": "इयत्ता १० वी",
        "percentage": "98.20%",
        "rank": "विद्यालय प्रथम",
        "photo": "/static/images/faculty-1.svg",
        "visible": True,
    },
    {
        "id": "sample-score-2",
        "name": "विद्यार्थी नाव",
        "class_name": "इयत्ता १२ वी",
        "percentage": "95.80%",
        "rank": "विज्ञान शाखा",
        "photo": "/static/images/faculty-3.svg",
        "visible": True,
    },
    {
        "id": "sample-score-3",
        "name": "विद्यार्थी नाव",
        "class_name": "इयत्ता १० वी",
        "percentage": "97.10%",
        "rank": "द्वितीय क्रमांक",
        "photo": "/static/images/faculty-5.svg",
        "visible": True,
    },
]


def data_path(collection):
    return DATA_DIR / f"{collection}.json"


def load_items(collection):
    path = data_path(collection)
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_items(collection, items):
    data_path(collection).write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def visible_items(collection, defaults):
    items = [item for item in load_items(collection) if item.get("visible", True)]
    return items or defaults


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_photo(file_storage, fallback=""):
    if not file_storage or not file_storage.filename:
        return fallback
    if not allowed_file(file_storage.filename):
        return fallback
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(UPLOAD_DIR / unique_name)
    return f"/static/uploads/{unique_name}"


def make_item(collection, existing=None):
    existing = existing or {}
    if collection == "faculty":
        item = {
            "id": existing.get("id", uuid.uuid4().hex),
            "name": request.form.get("name", "").strip(),
            "subject": request.form.get("subject", "").strip(),
            "description": request.form.get("description", "").strip(),
            "photo": existing.get("photo", ""),
            "visible": request.form.get("visible", "on") == "on",
            "created_at": existing.get("created_at", datetime.now().isoformat(timespec="seconds")),
        }
    elif collection == "alumni":
        item = {
            "id": existing.get("id", uuid.uuid4().hex),
            "name": request.form.get("name", "").strip(),
            "profession": request.form.get("profession", "").strip(),
            "description": request.form.get("description", "").strip(),
            "photo": existing.get("photo", ""),
            "visible": request.form.get("visible", "on") == "on",
            "created_at": existing.get("created_at", datetime.now().isoformat(timespec="seconds")),
        }
    else:
        item = {
            "id": existing.get("id", uuid.uuid4().hex),
            "name": request.form.get("name", "").strip(),
            "class_name": request.form.get("class_name", "").strip(),
            "percentage": request.form.get("percentage", "").strip(),
            "rank": request.form.get("rank", "").strip(),
            "photo": existing.get("photo", ""),
            "visible": request.form.get("visible", "on") == "on",
            "created_at": existing.get("created_at", datetime.now().isoformat(timespec="seconds")),
        }
    item["photo"] = save_photo(request.files.get("photo"), item["photo"])
    return item


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("owner_logged_in"):
            flash("कृपया आधी owner login करा.")
            return redirect(url_for("owner_login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def home():
    return render_template(
        "index.html",
        alumni=visible_items("alumni", DEFAULT_ALUMNI),
        scores=visible_items("scores", DEFAULT_SCORES),
    )


@app.route("/faculty")
def faculty():
    faculty_items = visible_items("faculty", DEFAULT_FACULTY)
    return render_template("faculty.html", faculty_items=faculty_items)


@app.route("/alumni")
def alumni():
    alumni_items = visible_items("alumni", DEFAULT_ALUMNI)
    return render_template("alumni.html", alumni_items=alumni_items)


@app.route("/share/faculty", methods=["GET", "POST"])
def share_faculty():
    if request.method == "POST":
        item = make_item("faculty")
        item["visible"] = True
        items = load_items("faculty")
        items.insert(0, item)
        save_items("faculty", items)
        flash("शिक्षकांची माहिती सबमिट झाली.")
        return redirect(url_for("share_faculty"))
    return render_template("public_form.html", form_type="faculty")


@app.route("/share/alumni", methods=["GET", "POST"])
def share_alumni():
    if request.method == "POST":
        item = make_item("alumni")
        item["visible"] = True
        items = load_items("alumni")
        items.insert(0, item)
        save_items("alumni", items)
        flash("माजी विद्यार्थ्यांची माहिती सबमिट झाली.")
        return redirect(url_for("share_alumni"))
    return render_template("public_form.html", form_type="alumni")


@app.route("/owner/login", methods=["GET", "POST"])
def owner_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == OWNER_USERNAME and password == OWNER_PASSWORD:
            session["owner_logged_in"] = True
            flash("Owner login यशस्वी झाले.")
            return redirect(url_for("owner_dashboard"))
        flash("Username किंवा password चुकीचा आहे.")
    return render_template(
        "owner_login.html",
        owner_username=OWNER_USERNAME,
    )


@app.route("/owner/logout")
def owner_logout():
    session.clear()
    flash("Logout झाले.")
    return redirect(url_for("owner_login"))


@app.route("/owner")
@login_required
def owner_dashboard():
    faculty_items = load_items("faculty")
    alumni_items = load_items("alumni")
    score_items = load_items("scores")
    return render_template(
        "owner_dashboard.html",
        faculty_items=faculty_items,
        alumni_items=alumni_items,
        score_items=score_items,
        owner_username=OWNER_USERNAME,
    )


@app.route("/owner/<collection>", methods=["GET", "POST"])
@login_required
def owner_manage(collection):
    if collection not in {"faculty", "alumni", "scores"}:
        return redirect(url_for("owner_dashboard"))
    if request.method == "POST":
        item = make_item(collection)
        items = load_items(collection)
        items.insert(0, item)
        save_items(collection, items)
        flash("नवीन माहिती जोडली.")
        return redirect(url_for("owner_manage", collection=collection))
    return render_template(
        "owner_manage.html",
        collection=collection,
        items=load_items(collection),
    )


@app.route("/owner/<collection>/<item_id>/edit", methods=["GET", "POST"])
@login_required
def owner_edit(collection, item_id):
    if collection not in {"faculty", "alumni", "scores"}:
        return redirect(url_for("owner_dashboard"))
    items = load_items(collection)
    item = next((entry for entry in items if entry["id"] == item_id), None)
    if item is None:
        flash("रेकॉर्ड सापडला नाही.")
        return redirect(url_for("owner_manage", collection=collection))
    if request.method == "POST":
        updated = make_item(collection, item)
        for index, entry in enumerate(items):
            if entry["id"] == item_id:
                items[index] = updated
                break
        save_items(collection, items)
        flash("माहिती अपडेट झाली.")
        return redirect(url_for("owner_manage", collection=collection))
    return render_template("owner_edit.html", collection=collection, item=item)


@app.route("/owner/<collection>/<item_id>/delete", methods=["POST"])
@login_required
def owner_delete(collection, item_id):
    if collection not in {"faculty", "alumni", "scores"}:
        return redirect(url_for("owner_dashboard"))
    items = [item for item in load_items(collection) if item["id"] != item_id]
    save_items(collection, items)
    flash("माहिती delete झाली.")
    return redirect(url_for("owner_manage", collection=collection))


if __name__ == "__main__":
    app.run(debug=True)
