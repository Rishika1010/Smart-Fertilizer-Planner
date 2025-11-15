from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from io import BytesIO
import csv
from fertilizers.models import FertilizerRecommendation


@login_required
def recommendation_detail(request, pk):
    recommendation = get_object_or_404(FertilizerRecommendation, pk=pk, user=request.user)
    items = recommendation.items.all()
    
    context = {
        'recommendation': recommendation,
        'items': items,
    }
    return render(request, 'reports/recommendation_detail.html', context)


@login_required
def recommendation_history(request):
    recommendations = FertilizerRecommendation.objects.filter(user=request.user)
    
    # Filter by parcel if provided
    parcel_id = request.GET.get('parcel')
    if parcel_id:
        recommendations = recommendations.filter(parcel_id=parcel_id)
    
    context = {
        'recommendations': recommendations,
    }
    return render(request, 'reports/recommendation_history.html', context)


@login_required
def export_pdf(request, pk):
    recommendation = get_object_or_404(FertilizerRecommendation, pk=pk, user=request.user)
    items = recommendation.items.all()
    
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=6,
    )
    
    # Title
    story.append(Paragraph("Fertilizer Recommendation Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Parcel Information
    story.append(Paragraph("Parcel Information", heading_style))
    parcel_data = [
        ['Parcel Name:', recommendation.parcel.name],
        ['Location:', recommendation.parcel.location],
        ['Area:', f"{recommendation.parcel.area_hectares} hectares"],
        ['Crop:', recommendation.parcel.crop.name if recommendation.parcel.crop else 'N/A'],
        ['Soil Type:', recommendation.parcel.get_soil_type_display()],
    ]
    parcel_table = Table(parcel_data, colWidths=[2*inch, 4*inch])
    parcel_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(parcel_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Soil Test Data
    story.append(Paragraph("Soil Test Data", heading_style))
    soil_data = [
        ['Parameter', 'Value', 'Unit'],
        ['Nitrogen', f"{recommendation.soil_nitrogen_ppm:.2f}", "ppm"],
        ['Phosphorus', f"{recommendation.soil_phosphorus_ppm:.2f}", "ppm"],
        ['Potassium', f"{recommendation.soil_potassium_ppm:.2f}", "ppm"],
        ['pH Level', f"{recommendation.soil_ph:.2f}", ""],
    ]
    soil_table = Table(soil_data, colWidths=[2*inch, 2*inch, 2*inch])
    soil_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(soil_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Nutrient Requirements
    story.append(Paragraph("Nutrient Requirements", heading_style))
    req_data = [
        ['Nutrient', 'Required (kg)', 'Soil Available (kg)', 'Deficit (kg)', 'Recommended (kg)'],
        ['Nitrogen', f"{recommendation.crop_nitrogen_requirement:.2f}", 
         f"{recommendation.soil_nitrogen_ppm * 1.95:.2f}", 
         f"{recommendation.nitrogen_needed_kg:.2f}", f"{recommendation.nitrogen_needed_kg:.2f}"],
        ['Phosphorus', f"{recommendation.crop_phosphorus_requirement:.2f}",
         f"{recommendation.soil_phosphorus_ppm * 1.95:.2f}",
         f"{recommendation.phosphorus_needed_kg:.2f}", f"{recommendation.phosphorus_needed_kg:.2f}"],
        ['Potassium', f"{recommendation.crop_potassium_requirement:.2f}",
         f"{recommendation.soil_potassium_ppm * 1.95:.2f}",
         f"{recommendation.potassium_needed_kg:.2f}", f"{recommendation.potassium_needed_kg:.2f}"],
    ]
    req_table = Table(req_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    req_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(req_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Recommended Fertilizers
    story.append(Paragraph("Recommended Fertilizers", heading_style))
    if items:
        fert_data = [['Fertilizer', 'Quantity', 'Unit', 'Cost (USD)']]
        for item in items:
            fert_data.append([
                item.fertilizer.name,
                f"{item.quantity:.2f}",
                item.unit,
                f"${item.cost:.2f}"
            ])
        
        fert_table = Table(fert_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
        fert_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(fert_table)
    else:
        story.append(Paragraph("No fertilizers recommended.", styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Total Cost
    story.append(Paragraph(f"<b>Estimated Total Cost: ${recommendation.estimated_total_cost:.2f}</b>", 
                          ParagraphStyle('TotalStyle', parent=styles['Normal'], fontSize=12)))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Notes
    if recommendation.notes:
        story.append(Paragraph("Notes", heading_style))
        story.append(Paragraph(recommendation.notes, styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Generated on: {recommendation.generated_at.strftime('%Y-%m-%d %H:%M:%S')}", 
                          styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    # Get the value of the BytesIO buffer
    buffer.seek(0)
    
    # Create response
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fertilizer_recommendation_{recommendation.pk}.pdf"'
    return response


@login_required
def export_csv(request, pk):
    recommendation = get_object_or_404(FertilizerRecommendation, pk=pk, user=request.user)
    items = recommendation.items.all()
    
    # Create HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="fertilizer_recommendation_{recommendation.pk}.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    writer.writerow(['Fertilizer Recommendation Report'])
    writer.writerow([])
    writer.writerow(['Parcel Information'])
    writer.writerow(['Parcel Name', recommendation.parcel.name])
    writer.writerow(['Location', recommendation.parcel.location])
    writer.writerow(['Area (hectares)', recommendation.parcel.area_hectares])
    writer.writerow(['Crop', recommendation.parcel.crop.name if recommendation.parcel.crop else 'N/A'])
    writer.writerow(['Soil Type', recommendation.parcel.get_soil_type_display()])
    writer.writerow([])
    
    writer.writerow(['Soil Test Data'])
    writer.writerow(['Nitrogen (ppm)', recommendation.soil_nitrogen_ppm])
    writer.writerow(['Phosphorus (ppm)', recommendation.soil_phosphorus_ppm])
    writer.writerow(['Potassium (ppm)', recommendation.soil_potassium_ppm])
    writer.writerow(['pH Level', recommendation.soil_ph])
    writer.writerow([])
    
    writer.writerow(['Nutrient Requirements'])
    writer.writerow(['Nutrient', 'Required (kg)', 'Deficit (kg)', 'Recommended (kg)'])
    writer.writerow(['Nitrogen', recommendation.crop_nitrogen_requirement, 
                    recommendation.nitrogen_needed_kg, recommendation.nitrogen_needed_kg])
    writer.writerow(['Phosphorus', recommendation.crop_phosphorus_requirement,
                    recommendation.phosphorus_needed_kg, recommendation.phosphorus_needed_kg])
    writer.writerow(['Potassium', recommendation.crop_potassium_requirement,
                    recommendation.potassium_needed_kg, recommendation.potassium_needed_kg])
    writer.writerow([])
    
    writer.writerow(['Recommended Fertilizers'])
    writer.writerow(['Fertilizer', 'Quantity', 'Unit', 'Cost (USD)'])
    for item in items:
        writer.writerow([item.fertilizer.name, item.quantity, item.unit, item.cost])
    
    writer.writerow([])
    writer.writerow(['Estimated Total Cost (USD)', recommendation.estimated_total_cost])
    writer.writerow(['Generated on', recommendation.generated_at.strftime('%Y-%m-%d %H:%M:%S')])
    
    if recommendation.notes:
        writer.writerow([])
        writer.writerow(['Notes', recommendation.notes])
    
    return response

