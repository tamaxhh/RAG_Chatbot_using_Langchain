from reportlab.pdfgen import canvas

def export_to_pdf(content: str, filename: str):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, content)
    c.save()

def export_to_md(content: str, filename: str):
    with open(filename, 'w') as f:
        f.write(content)