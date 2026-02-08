import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from database_mysql import insert_project, get_projects

app = Flask(__name__)

# Upload settings (Step 3 CSV)
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.before_request
def log_requests():
    # يطبع كل Request عشان نعرف هل POST يوصل أو لا
    print(f"➡️ {request.method} {request.path}")


@app.route("/")
def landing():
    return render_template("arcane_landing_page.html")


@app.route("/auth")
def auth():
    return render_template("arcane_login_signup.html")


@app.route("/sectors")
def sectors():
    return render_template("arcane_sector_selection.html")


@app.route("/setup")
def setup():
    sector = request.args.get("sector", "")
    return render_template("new_project_setup.html", sector=sector)


@app.route("/save_project", methods=["POST"])
def save_project():
    # استلام البيانات من الفورم
    sector = request.form.get("sector_id")
    name = request.form.get("project_name")
    description = request.form.get("description")
    
    # طباعة للتأكد في التيرمينال
    print(f"📥 استلام: {name} | {sector}")

    try:
        # استدعاء دالة الإدخال من ملف database_mysql
        project_id = insert_project(sector, name, description)
        print(f"✅ تم الحفظ في القاعدة بنجاح! ID: {project_id}")
        
        # التوجيه لصفحة المشاريع لرؤية النتيجة
        return redirect(url_for('projects'))
        
    except Exception as e:
        print(f"❌ خطأ أثناء التخزين: {e}")
        return f"حدث خطأ في قاعدة البيانات: {e}"

    # Step 3: CSV upload (اختياري)
    dataset_path = None
    file = request.files.get("dataset")
    if file and file.filename:
        filename = secure_filename(file.filename)

        # عشان ما يكتب فوق ملف قديم بنفس الاسم
        base, ext = os.path.splitext(filename)
        counter = 1
        final_name = filename
        while os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], final_name)):
            final_name = f"{base}_{counter}{ext}"
            counter += 1

        save_path = os.path.join(app.config["UPLOAD_FOLDER"], final_name)
        file.save(save_path)
        dataset_path = save_path

    # ✅ Insert (يدعم حالتين: insert_project بثلاثة باراميتر أو أربعة)
    try:
        try:
            project_id = insert_project(sector, name, description, dataset_path)
        except TypeError:
            # لو دالتك القديمة ما تدعم dataset_path
            project_id = insert_project(sector, name, description)

        print("✅ Inserted project_id:", project_id)

    except Exception as e:
        print("❌ DB ERROR:", repr(e))
        return f"❌ DB ERROR: {repr(e)}", 500

    return redirect(url_for("workspace", project_id=project_id))


@app.route("/workspace/<int:project_id>")
def workspace(project_id):
    return render_template("arcane_project_workspace.html", project_id=project_id)


@app.route("/projects")
def projects():
    try:
        projects_list = get_projects()
    except Exception as e:
        print("❌ GET_PROJECTS ERROR:", repr(e))
        return f"❌ GET_PROJECTS ERROR: {repr(e)}", 500

    return render_template("projects.html", projects=projects_list)


@app.route("/dashboard")
def dashboard():
    return render_template("arcane_dashboard.html")


@app.route("/dashboard-ar")
def dashboard_ar():
    return render_template("arcane_dashboard_arabic.html")


if __name__ == "__main__":
    app.run(debug=True)