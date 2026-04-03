from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(filename, insights):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("GlamTrends AI Report", styles["Title"]))
    content.append(Spacer(1,20))

    for line in insights:
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1,10))

    doc.build(content)