from typing import List
from io import BytesIO
import os
import sys

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

class TextElement:
    def __init__(self, line: str, x_offset: int, y_offset: int, font_size: int):
        self.line = line            # string
        self.x_offset = x_offset    # int
        self.y_offset = y_offset    # int
        self.font_size = font_size  # int

    def __repr__(self):
        return (f"TextElement(line='{self.line}', x={self.x_offset}, y={self.y_offset}, "
                f"font_size={self.font_size})")


# def generate_certificate(elements: List[TextElement], input_pdf, out_dir):
#     pdf_reader = PdfReader(input_pdf)
#     pdf_writer = PdfWriter()

#     # Create a BytesIO buffer to store the overlay
#     packet = BytesIO()
#     canvas_obj = canvas.Canvas(packet)

def resource_path(relative_path):
    # Get the absolute path to the resource when bundled by PyInstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def generate_kpk_cert(input_pdf, out_dir, name_obj: TextElement, num_obj: TextElement):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    name_dat = name_obj.line
    numurs = num_obj.line

    # Access the first page
    page = pdf_reader.pages[0]

    page_width = int(page.mediabox.width)
    page_height = int(page.mediabox.height)

    # Create a BytesIO buffer to store the overlay
    packet = BytesIO()
    canvas_obj = canvas.Canvas(packet)

    custom_font_path = resource_path(os.path.join("assets", "Marcellus-Regular.ttf"))
    pdfmetrics.registerFont(TTFont('Marcellus', custom_font_path))

    # Set font and size
    font_name = "Marcellus"
    font_size_name = name_obj.font_size
    font_size_nr = num_obj.font_size
    canvas_obj.setFont(font_name, font_size_name)
    canvas_obj.setFillColorRGB(0, 0, 0)

    numurs = f'Nr. {numurs}'
    # Calculate string widths
    str_len = canvas_obj.stringWidth(name_dat, font_name, font_size_name)
    num_len = canvas_obj.stringWidth(numurs, font_name, font_size_nr)
    # Calculate positions for the name and number
    x_name = ((page_width / 2) - int(str_len / 2)) + name_obj.x_offset # 50
    y_name = (page_height / 2) + name_obj.y_offset # 500 = 842/2 + 79
    x_nr = ((page_width / 2) - int(num_len / 2)) + num_obj.x_offset # 50
    y_nr = (page_height / 2) + num_obj.y_offset # 555 = 842/2 + 84

    print(f'name coordinates: x={x_name}, y={y_name}, width={font_size_name}')
    print(f'number coordinates: x={x_nr}, y={y_nr}, width={font_size_nr}')

    # Draw the name on the template
    canvas_obj.drawString(x_name, y_name, name_dat)
    canvas_obj.setFont(font_name, font_size_nr)
    canvas_obj.drawString(x_nr, y_nr, numurs)
    canvas_obj.save()
    packet.seek(0)

    # Merge the overlay with the certificate
    overlay_reader = PdfReader(packet)
    overlay_page = overlay_reader.pages[0]
    page.merge_page(overlay_page)
    pdf_writer.add_page(page)

    # Add remaining pages without modification
    for page in pdf_reader.pages[1:]:
        pdf_writer.add_page(page)

    # Write the final output to a new PDF
    output_path = os.path.join(out_dir, f"{name_dat}.pdf")
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)
      
    print(f'Certificate Completed! {name_dat}')
      


# generate_cert("template.pdf", "Jānim Bērziņam", "KPK-2024-10/409")