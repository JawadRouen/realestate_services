# coding: utf8
from flask import render_template
#from weasyprint import HTML, CSS


__all__ = ['contract']

def contract(template_name, contract_info):
    html_result = render_template(template_name, **contract_info)
    return html_result





    
