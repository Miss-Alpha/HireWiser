
import re
import texts
import os.path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from datetime import datetime
from streamlit_extras.stylable_container import stylable_container

pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf')) 

logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img/logo.gif')

# Create PDF Functions
def create_header_style(level):
    """Create and return a header style based on the level."""
    styles = getSampleStyleSheet()
    if level == 1:
        return ParagraphStyle(
            'Header1Style',
            parent=styles['Heading1'],
            fontSize=20,
            fontName='Helvetica-Bold',
            spaceAfter=20,
            spaceBefore=10  
        )
    elif level == 2:
        return ParagraphStyle(
            'Header2Style',
            parent=styles['Heading2'],
            fontSize=14,
            fontName='Helvetica-Bold',
            spaceAfter=18,  
            spaceBefore=8 
        )
    elif level == 3:
        return ParagraphStyle(
            'Header3Style',
            parent=styles['Heading3'],
            fontSize=12,
            fontName='Helvetica-Bold',
            spaceAfter=18,  
            spaceBefore=8 
        )
    return styles['Normal']

def create_paragraph_style():
    """Create and return a normal paragraph style with more line spacing."""
    return ParagraphStyle(
        'Normal',
        fontName='DejaVuSans',
        fontSize=10,
        spaceBefore=12,  
        spaceAfter=12,   
        leading=15       
    )

def format_text(text):
    """Format text to replace '---' with a line break and '**' for bold, '##' for headers."""
    # Replace line breaks
    text = text.replace('---', '<br />')
    # Handle line breaks for specific patterns
    text = re.sub(r'(Question \d+:|Answer: )', r'<br/>\1', text, flags=re.IGNORECASE)
    # Handle bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Handle headers
    text = re.sub(r'##(.*?)\n', lambda match: f"<font size=16><b>{match.group(1)}</b></font>\n", text)
    # Handle numbered lists (e.g., '1.', '2.', etc.)
    text = re.sub(r'(\n|^)(\d+\.)', r'<br/>\2', text)  # Add <br/> before any numbered list
     # Bold numbered chunks ending with a colon (e.g., '1. Cloud Platforms:')
    text = re.sub(r'(\d+\.\s[^:]+:)', r'<b>\1</b>', text)
    # Add line break after each colon
    text = re.sub(r'(:)', r'\1<br/>', text)  
    # Add line break before the word 'Explanation'
    # text = re.sub(r'(\bExplanation\b)', r'<br/><b>\1</b>', text) 
    return text


def add_section(content, header_text, paragraph_text, header_style, paragraph_style):
    """Add a section with a header and paragraph to the content list."""
    header = Paragraph(header_text, header_style)
    formatted_paragraph_text = format_text(paragraph_text)
    paragraph = Paragraph(formatted_paragraph_text, paragraph_style)
    content.extend([header, paragraph])


def add_tips_box(content, tips_text):
    """Add a gray box with helpful tips to the content."""
    formatted_tips_text = format_text(tips_text)
    
    # Create a table with a single cell for the tips text
    tips_data = [[Paragraph(formatted_tips_text, create_paragraph_style())]]
    
    # Create a Table object
    tips_table = Table(tips_data, colWidths=[6.25 * inch])  # Set the width of the box

    # Set the background color to light gray
    tips_table.setStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Add a border around the box
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ])
    
    content.append(tips_table)

def draw_name(canvas, doc, candidate_name, color="#ff5400"):
    """Draw the name at the top of the page with a specified color."""
    canvas.saveState()  # Save the current canvas state
    
    # Set the font and size for the name
    canvas.setFont('Helvetica-Bold', 16)
    
    # Set the font color (using HexColor)
    canvas.setFillColor(HexColor(color))
    
    # Position the name (centered at the top of the page)
    name_x = doc.pagesize[0] / 2  # Horizontal center
    name_y = doc.pagesize[1] - 0.75 * inch  # 0.75 inch from the top
    
    # Draw the name, center-aligned horizontally
    canvas.drawCentredString(name_x, name_y, candidate_name)
    
    canvas.restoreState() # Restore the canvas state after drawing


def draw_logo(canvas, doc, logo_path):
    """Add a logo to the top of the PDF."""
    # Create an Image object with the logo
    logo = Image(logo_path)
    
    # Resize the logo (you can adjust the width and height as needed)
    logo_width = 1.0 * inch  # Adjust the height
    logo_height = 0.9 * inch  # Adjust the width

    # Set the position of the logo (top-right)
    canvas.drawImage(logo_path, doc.pagesize[0] - logo_width - 0.5 * inch, doc.pagesize[1] - logo_height - 0.5 * inch,
                     width=logo_width, height=logo_height)

def draw_footer(canvas, doc):
    """Draw a footer on each page."""
    # Footer text
    footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d')} - Page {doc.page}"
    
    # Set the font and size for the footer
    canvas.setFont('Helvetica', 9)

    # Set the font color to dark gray (using HexColor)
    canvas.setFillColor(HexColor("#4D4D4D"))
    
    # Calculate position from bottom (1 inch from the bottom)
    footer_x = 0.5 * inch
    footer_y = 0.5 * inch
    
    # Draw the footer text on the canvas
    canvas.drawString(footer_x, footer_y, footer_text)

def draw_logo_and_footer(canvas, doc, candidate_name, logo_path):
    """Draw both the logo and the footer on the first page."""
    # Draw name at the top
    draw_name(canvas, doc, candidate_name)
    draw_logo(canvas, doc, logo_path)
    draw_footer(canvas, doc)

def generate_filename(base_name):
    """Generate a filename with the current date and time."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.pdf"


def create_pdf(pdf_filename, sections, logo_path = logo_path, tips_text = texts.tips_text, candidate_name=''):
    """Create a PDF with the given sections."""
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    content = []

    for header_text, paragraph_text in sections:
        header_level = 1 if header_text.startswith("## ") else 2
        header_style = create_header_style(header_level)
        paragraph_style = create_paragraph_style()
        add_section(content, header_text, paragraph_text, header_style, paragraph_style)
    
    # Add helpful tips box at the end 
    add_tips_box(content, tips_text)

    # Build the PDF and apply the logo on the first page using onFirstPage callback
    doc.build(content, onFirstPage=lambda canvas, doc: draw_logo_and_footer(canvas, doc, candidate_name, logo_path), onLaterPages=draw_footer)

