from flask import Flask, redirect, url_for, render_template, request, send_file
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from PIL import ImageFont
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    def setPosSiShape(shape):
        left = shape.left + Inches(0.03)
        top = shape.top + Inches(0.03)
        width = shape.width - Inches(0.05)
        height = shape.height - Inches(0.05)
        posSiShape = {"left" : left, "top" : top, "width" : width, "height" : height}
        return posSiShape
    
    caseNumber = request.form["caseNumber"].upper()
    unitModel = request.form["unitModel"].upper()
    serialNumber = request.form["serialNumber"].upper()
    claimNumber = request.form["claimNumber"].upper()

    prs = Presentation("template.pptx")
    slide = prs.slides[0]

    # # begin to find out name of shape dan type of shape
    # for i, shape in enumerate(slide.shapes):
    #     print(i, "-", shape.name, "-", shape.shape_type, flush=True)
    # # end to find out name of shape dan type of shape

    table = slide.shapes[2].table

    data = [caseNumber, unitModel, serialNumber, claimNumber]

    for row in range(len(data)):
        cell = table.cell(row, 1)
        cell.text = str(data[row])
        p = cell.text_frame.paragraphs[0]
        if not p.runs:
            run = p.add_run()
            run.text = cell.text
        else:
            run = p.runs[0]
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.bold = True

    shape = slide.shapes[0]
    getPosSiShape = setPosSiShape(shape)

    wo = request.files["WO"]
    woStream = BytesIO(wo.read())
    woStream.seek(0)
    slide.shapes.add_picture(woStream, getPosSiShape["left"], getPosSiShape["top"], getPosSiShape["width"], getPosSiShape["height"])

    # begin get all unit photo 
    photoUnitList = request.files.getlist("addPhoto[]")
    infoUnitList = request.form.getlist("addInfo[]")
    SLD_LAYOUT_TITLE_AND_CONTENT = 6
    slideLayout = prs.slide_layouts[SLD_LAYOUT_TITLE_AND_CONTENT]
    row = 1
    slide2 = None
    tempIndex = 0
    slideWidth = 0
    currentIndex = 0
    rectangleShape = None

    for i, (photo, info) in enumerate(zip(photoUnitList, infoUnitList), start=1):
        if photo and photo.filename != "":
            if i == 1:
                photoStream = BytesIO(photo.read())
                getPosSiShape2 = setPosSiShape(slide.shapes[1])
                photoStream.seek(0)
                slide.shapes.add_picture(photoStream, getPosSiShape2["left"], getPosSiShape2["top"], getPosSiShape2["width"], getPosSiShape2["height"])

                if info and any(info):
                    oldPosInfo = setPosSiShape(slide.shapes[3])
                    spTree = slide.shapes._spTree
                    spTree.remove(slide.shapes[3]._element)

                    font = ImageFont.truetype("calibri.ttf", 18)
                    bbox = font.getbbox(info)
                    textWidth = (bbox[2] - bbox[0]) / 96
                    newLeft = oldPosInfo["left"] + (oldPosInfo["width"] - Inches(textWidth)) / 2

                    newShapeInfo = slide.shapes.add_shape(shape.auto_shape_type, newLeft, oldPosInfo["top"], Inches(textWidth), oldPosInfo["height"])
                    newShapeInfo.text = info

                    newShapeInfo.fill.solid()
                    newShapeInfo.fill.fore_color.rgb =RGBColor(255, 255, 255)
                    newShapeInfo.fill.background()

                    line = newShapeInfo.line
                    line.color.rgb = RGBColor(0, 0, 0)
                    line.width = Pt(1)

                    textFrame = newShapeInfo.text_frame
                    p =textFrame.paragraphs[0]
                    run = p.runs[0]
                    run.font.color.rgb = RGBColor(0, 0, 0)

            if i >= 2 and (i - 2) % 4 == 0: 
                slide2 = prs.slides.add_slide(slideLayout)
                slideWidth = prs.slide_width
                currentIndex = len(prs.slides)

            if (currentIndex != tempIndex):
                row = 1
            tempIndex = currentIndex

            cols = 2
            gapY = Inches(1.25)
            margin = Inches(0.3)
            height = Inches(0.5)
            shapeWidth = (slideWidth - (3 * margin)) / 2

            if slide2 is not None:
                row += 1
                col = i % cols
                row2 = row // cols
                x = margin + col * (shapeWidth + margin)
                if row2 == 1:
                    y = Inches(0.2)
                else:
                    y = margin + row2 * (height + gapY)
                rectangleShape = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, shapeWidth, height)

            if rectangleShape is not None:
                rectangleShape.text = info
                testLeft = rectangleShape.left
                testTop = rectangleShape.top
                widthCol0 = Inches(3)
                heightRow0 = rectangleShape.height

            if slide2 is not None:
                slide2.shapes.add_picture(photo, testLeft, testTop + heightRow0, widthCol0, Inches(3))
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

# # begin mengambil nilai apapun dari url ke dalam web
# @app.route("/<name>")  
# def user(name):
#     return f"hello {name}!"
# # end begin mengambil nilai apapun dari url ke dalam web

# @app.route("/admin")
# def admin():
#     return redirect(url_for("user", name = "Dyah")) #hanya redirect halaman biasa

if __name__ == "__main__":
    app.run(debug=True) 