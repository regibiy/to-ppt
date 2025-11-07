from flask import Flask, redirect, url_for, render_template, request, send_file

from pptx import Presentation
from pptx.util import Inches
from tempfile import NamedTemporaryFile

app = Flask(__name__)

@app.route("/")
def home():
    # if request.method == "POST":
    #     caseNumber = request.form["caseNumber"]
    #     return redirect(url_for("generate", dataCaseNumber = caseNumber))
    # else:
    return render_template("index.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")

@app.route("/generate", methods=["POST"])
def generate():
    caseNumber = request.form["caseNumber"]
    wo = request.files["WO"]
    return wo
    # wo = request.files["WO"]
    # prs = Presentation("template.pptx")
    # slide = prs.slides[0]
    # table = slide.shapes[0].table
    # table.cell(0,1).text = caseNumber

    # with NamedTemporaryFile(delete=False, suffix=".jpeg") as img_temp:
    #     wo.save(img_temp.name)

    # slide.shapes.add_picture(img_temp.name, Inches(1), Inches(3), width=Inches(3), height=Inches(2))

    # tmp = NamedTemporaryFile(delete=False, suffix=".pptx")
    # prs.save(tmp.name)

    # return send_file(
    #     tmp.name,
    #     as_attachment=True,
    #     download_name = f"{caseNumber}.pptx",
    #     mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    # )

    # return f"<h1>{caseNumber}</h1>"

#mengambil nilai apapun dari url ke dalam web
@app.route("/<name>")  
def user(name):
    return f"hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name = "Dyah")) #hanya redirect halaman biasa

if __name__ == "__main__":
    app.run(debug=True) 