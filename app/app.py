from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

@app.route("/convert_to_pdf", methods=["GET"])
def convert_to_pdf():
    """
    Converts the distraction_analysis.json file into a PDF.
    """
    json_file = "distraction_analysis.json"
    pdf_file = "distraction_analysis.pdf"

    if not os.path.exists(json_file):
        flash("JSON file not found. Please process a video first.")
        return redirect(url_for("results"))

    try:
        # Load JSON data
        with open(json_file, "r") as file:
            data = json.load(file)

        # Create a PDF
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add title
        c.drawString(100, 750, "Distraction Analysis Report")
        c.drawString(100, 735, "-" * 50)

        # Add JSON data to the PDF
        y_position = 700  # Start position for content
        for entry in data:
            timestamp = entry.get("distraction_timestamp", "N/A")
            transcription = entry.get("transcription", "N/A")
            segment_start = entry.get("segment_start", "N/A")
            segment_end = entry.get("segment_end", "N/A")

            text = f"Timestamp: {timestamp:.2f}s\n"
            text += f"  - Transcription: {transcription}\n"
            text += f"  - Segment: {segment_start:.2f}s to {segment_end:.2f}s\n"

            # Add text to PDF, handle page overflow
            for line in text.split("\n"):
                c.drawString(100, y_position, line)
                y_position -= 15
                if y_position < 50:  # Create a new page if space runs out
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = 750

        c.save()
        flash("PDF successfully generated!")
        return send_file(pdf_file, as_attachment=True)
    except Exception as e:
        flash(f"Error while creating PDF: {e}")
        return redirect(url_for("results"))
