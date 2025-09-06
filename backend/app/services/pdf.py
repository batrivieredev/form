from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import json
import os
from datetime import datetime

from ..models import Form, FormResponse, User, Site

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Create custom styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        ))

    def generate_form_response_pdf(self, form: Form, response: FormResponse, user: User, site: Site) -> str:
        """Generate PDF for a form response."""
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getenv("UPLOAD_DIR", "./uploads"), "pdfs")
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"form_response_{response.id}_{timestamp}.pdf"
        filepath = os.path.join(output_dir, filename)

        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Build content
        content = []

        # Add site information
        content.append(Paragraph(site.name, self.styles['CustomTitle']))
        content.append(Spacer(1, 12))

        # Add form title
        content.append(Paragraph(form.title, self.styles['Heading1']))
        if form.description:
            content.append(Paragraph(form.description, self.styles['Normal']))
        content.append(Spacer(1, 12))

        # Add user information
        content.append(Paragraph("User Information", self.styles['SectionHeader']))
        user_info = [
            ["Name:", user.username],
            ["Email:", user.email],
            ["Submission Date:", response.created_at.strftime("%Y-%m-%d %H:%M:%S")]
        ]
        user_table = Table(user_info, colWidths=[100, 400])
        user_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        content.append(user_table)
        content.append(Spacer(1, 20))

        # Add form responses
        content.append(Paragraph("Form Responses", self.styles['SectionHeader']))

        form_fields = json.loads(form.fields)
        form_data = json.loads(response.data)

        response_data = []
        for field in form_fields:
            field_id = field['id']
            field_label = field['label']
            field_value = form_data.get(field_id, '')

            # Format value based on field type
            if field['type'] == 'checkbox':
                field_value = 'Yes' if field_value else 'No'
            elif field['type'] == 'select' and field_value:
                # Get option label from value
                options = {opt['value']: opt['label'] for opt in field.get('options', [])}
                field_value = options.get(field_value, field_value)
            elif isinstance(field_value, (list, dict)):
                field_value = json.dumps(field_value, indent=2)

            response_data.append([field_label + ":", str(field_value)])

        responses_table = Table(response_data, colWidths=[150, 350])
        responses_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        content.append(responses_table)

        # Build PDF
        doc.build(content)
        return filepath

    def generate_responses_summary_pdf(self, form: Form, responses: list[FormResponse], site: Site) -> str:
        """Generate a summary PDF for all responses to a form."""
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getenv("UPLOAD_DIR", "./uploads"), "pdfs")
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"form_summary_{form.id}_{timestamp}.pdf"
        filepath = os.path.join(output_dir, filename)

        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Build content
        content = []

        # Add header information
        content.append(Paragraph(site.name, self.styles['CustomTitle']))
        content.append(Paragraph(form.title, self.styles['Heading1']))
        if form.description:
            content.append(Paragraph(form.description, self.styles['Normal']))
        content.append(Spacer(1, 20))

        # Add summary information
        content.append(Paragraph("Summary Information", self.styles['SectionHeader']))
        summary_data = [
            ["Total Responses:", str(len(responses))],
            ["First Response:", responses[0].created_at.strftime("%Y-%m-%d %H:%M:%S") if responses else "N/A"],
            ["Latest Response:", responses[-1].created_at.strftime("%Y-%m-%d %H:%M:%S") if responses else "N/A"]
        ]
        summary_table = Table(summary_data, colWidths=[150, 350])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        content.append(summary_table)
        content.append(Spacer(1, 20))

        # Process responses
        form_fields = json.loads(form.fields)

        for response in responses:
            content.append(Paragraph(f"Response #{response.id}", self.styles['SectionHeader']))
            response_data = json.loads(response.data)
            table_data = []

            for field in form_fields:
                field_id = field['id']
                field_label = field['label']
                field_value = response_data.get(field_id, '')

                # Format value based on field type
                if field['type'] == 'checkbox':
                    field_value = 'Yes' if field_value else 'No'
                elif field['type'] == 'select' and field_value:
                    options = {opt['value']: opt['label'] for opt in field.get('options', [])}
                    field_value = options.get(field_value, field_value)
                elif isinstance(field_value, (list, dict)):
                    field_value = json.dumps(field_value, indent=2)

                table_data.append([field_label + ":", str(field_value)])

            response_table = Table(table_data, colWidths=[150, 350])
            response_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            content.append(response_table)
            content.append(Spacer(1, 20))

        # Build PDF
        doc.build(content)
        return filepath
