# coding: utf-8

import time
import io
from calendar import monthrange
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

__all__ = ['reicept', 'reicept_with_default']


def reicept(stream, reicept_info):
    #load params
    signature = reicept_info['signature']
    leaser_name= reicept_info['leaser_name']
    leaser_address= reicept_info['leaser_address']
    signature_city= reicept_info['signature_city']
    roomer_name= reicept_info['roomer_name']
    flat_address= reicept_info['flat_address']
    flat_number= reicept_info['flat_number']
    price= reicept_info['price']
    charges= reicept_info['charges']
    full_price= reicept_info['full_price']
    month= reicept_info['month']
    year= reicept_info['year']
    start_day= reicept_info['start_day']
    end_day= reicept_info['end_day']
    
    months = ["Janvier", "Février", "Mars", "Avril", "Mai","Juin", "Juillet", "Aout",\
                "Septembre", "Octobre", "Novembre", "Decembre"]
    start_date      = "/".join(map(lambda x: str(x), [start_day, month, year]))
    end_date        = "/".join(map(lambda x: str(x), [end_day, month, year]))
    month_and_year  = "-".join([months[month-1], str(year)])
    
    doc = SimpleDocTemplate(stream,pagesize=letter,\
                        rightMargin=72,leftMargin=72,\
                        topMargin=72,bottomMargin=18)
                        
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    
    Story=[]
    #title
    title = Paragraph('<para alignment="center">QUITTANCE DE LOYER</para>',styles['Heading1'])
    Story.append(title)
    Story.append(Spacer(1, 8))  
    Story.append(Paragraph('<para alignment="center">%s</para>' % month_and_year, styles["Heading1"]))
    Story.append(Spacer(1, 50))
    ptext = u'<font size=12>Nous soussignés, %s, propriétaires du logement situé au %s - Appartement n°%s, donné en location à \
    %s, déclarons avoir reçu de celle-ci à titre de loyer et charges \
    pour la période du %s au %s la somme de %s lui en donnons quittance.</font>' % (leaser_name, flat_address, flat_number, roomer_name,start_date, end_date, full_price)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = u'<font size=12>Cette somme se répartit de la façon suivante : %s de loyer et %s de charges.</font>' % (price,charges)
                                                                                                    
    
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 30))
    ptext = u'<font size=12>Fait à %s, le  %s</font>' % (signature_city,time.strftime('%d/%m/%Y'))
     
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))     
    #add signature 
    im = Image(signature)
    im.hAlign = 'RIGHT'
    Story.append(im)
    doc.build(Story)
    pdf_out = stream.getvalue()
    stream.close()
    return pdf_out#.encode('latin-1')


def reicept_with_default(stream, reicept_info):
    #manage default value for the first day
    if reicept_info['start_day'] == '':
        reicept_info['start_day'] = 1
        
    #manage default value for the last day    
    if reicept_info['end_day'] == '':
        _,reicept_info['end_day'] = monthrange(reicept_info['year'],reicept_info['month'])
        
    return reicept(stream, reicept_info)

    
