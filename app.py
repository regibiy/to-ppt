from flask import Flask, redirect, url_for, render_template, request, send_file
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches
from PIL import ImageFont

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")

@app.route("/generate", methods=["POST"])
def generate():
    def setPosSiShape(shape):
        # begin get position and size shape
        left = shape.left + Inches(0.03)
        top = shape.top + Inches(0.03)
        width = shape.width - Inches(0.05)
        height = shape.height - Inches(0.05)
        posSiShape = {
            "left" : left,
            "top" : top,
            "width" : width,
            "height" : height
        }
        return posSiShape
        # end begin get position and size shape
    
    caseNumber = request.form["caseNumber"]
    wo = request.files["WO"]

    # open template and set which slide
    prs = Presentation("template.pptx")
    slide = prs.slides[0]

    # begin to find out name of shape dan type of shape
    # for i, shape in enumerate(slide.shapes):
    #     print(i, "-", shape.name, "-", shape.shape_type, flush=True)
    # end to find out name of shape dan type of shape

    # determine the first shape
    table = slide.shapes[0].table
    table.cell(0,1).text = caseNumber

    # determine the second shape
    shape = slide.shapes[1]
    getPosSiShape = setPosSiShape(shape)
    
    woStream = BytesIO(wo.read())
    woStream.seek(0)
    slide.shapes.add_picture(woStream, getPosSiShape["left"], getPosSiShape["top"], getPosSiShape["width"], getPosSiShape["height"])

    # begin get all unit photo 
    photoUnitList = request.files.getlist("addPhoto[]")
    infoUnitList = request.form.getlist("addInfo[]")
    for i, (photo, info) in enumerate(zip(photoUnitList, infoUnitList), start=1):
        if photo and photo.filename != "":
            if i == 1:
                photoStream = BytesIO(photo.read())
                getPosSiShape2 = setPosSiShape(slide.shapes[2])
                photoStream.seek(0)
                slide.shapes.add_picture(photoStream, getPosSiShape2["left"], getPosSiShape2["top"], getPosSiShape2["width"], getPosSiShape2["height"])

                oldPosInfo = setPosSiShape(slide.shapes[3])
                spTree = slide.shapes._spTree
                spTree.remove(slide.shapes[3]._element)

                font = ImageFont.truetype("arial.ttf", 18)
                bbox = font.getbbox(info)
                textWidth = (bbox[2] - bbox[0]) / 96
                newLeft = oldPosInfo["left"] + (oldPosInfo["width"] - Inches(textWidth)) / 2
                
                newShapeInfo = slide.shapes.add_shape(shape.auto_shape_type, newLeft, oldPosInfo["top"], Inches(textWidth), oldPosInfo["height"])
                newShapeInfo.text = info
            else:
                prs.slides.add_slide(prs.slide_layouts[1])
    # end get all unit photo

    pptStream = BytesIO()
    prs.save(pptStream)
    pptStream.seek(0)

    return send_file(
        pptStream,
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