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

    # photoUnitList = request.files.getlist("addPhoto[]")
    # for i, photo in enumerate(photoUnitList, start=1):
    #     if photo and photo.filename != "":
    #          print(f"Gambar ke-{i}: {photo.filename}")
    # return "OK"
    
    # open template and set which slide
    prs = Presentation("template.pptx")
    slide = prs.slides[0]

    # for i, shape in enumerate(slide.shapes):
    #     print(i, "-", shape.name, "-", shape.shape_type)

    # return "OK"
    
    # determine the first shape
    table = slide.shapes[0].table
    table.cell(0,1).text = caseNumber

    # determine the second shape
    shape = slide.shapes[1]

    # begin get position and size shape
    left = shape.left + Inches(0.03)
    top = shape.top + Inches(0.03)
    width = shape.width - Inches(0.05)
    height = shape.height - Inches(0.05)
    # end begin get position and size shape
    
    slide.shapes.add_picture(wo, left, top, width, height)

    # begin insert image
    # with NamedTemporaryFile(delete=False, suffix=".jpeg") as img_temp:
    #     wo.save(img_temp.name)

    # slide.shapes.add_picture(img_temp.name, Inches(1), Inches(3), width=Inches(3), height=Inches(2))
    # end insert image

    tmp = NamedTemporaryFile(delete=False, suffix=".pptx")
    prs.save(tmp.name)

    return send_file(
        tmp.name,
        as_attachment=True,
        download_name = f"{caseNumber}.pptx",
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

# begin mengambil nilai apapun dari url ke dalam web
@app.route("/<name>")  
def user(name):
    return f"hello {name}!"
# end begin mengambil nilai apapun dari url ke dalam web

@app.route("/admin")
def admin():
    return redirect(url_for("user", name = "Dyah")) #hanya redirect halaman biasa

if __name__ == "__main__":
    app.run(debug=True) 