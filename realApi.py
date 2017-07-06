from realestate import *
from flask import Flask, request, make_response, jsonify, json, render_template
import io
import os

app = Flask(__name__)

#curl -H "Content-Type: application/json" -X POST -d "{\"password\":\"xyz\"}"  http://127.0.0.1:5000/gen_reicept
@app.route('/gen_reicept', methods = ['POST'])
def genreicept():
    
    if request.headers['Content-Type'] != 'application/json':
        return "Unsupported Media Type"

    reicept_info = request.json
    
    #build pdf name
    month_and_year  = "_".join([str(reicept_info['month']), str( reicept_info['year'])])
    pdfname = "Appart "+reicept_info['flat_number']+" reicept "+month_and_year+".pdf"

    stream = io.BytesIO()
    pdf_out = reicept_with_default(stream, reicept_info)
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename="+ pdfname
    response.mimetype = 'application/pdf'
    return response

#curl  http://127.0.0.1:5000/gen_contract
@app.route('/gen_contract', methods = ['POST'])
def gencontract():
    if request.headers['Content-Type'] != 'application/json':
        return "Unsupported Media Type"

    contract_info = request.json
    
    #build pdf name
    # pdfname = "Appart "+contract_info['flat_number']+" contract "+contract_info['contract_startdate']\
    # +" "+.contract_info['roomer_name']+".pdf"
    
    return contract("bail_template.html", contract_info)
    #pdf_file = HTML(string=test).write_pdf(stylesheets=[CSS(settings.STATIC_ROOT +  'css/report.css')])
    #pdf_out = make_response(pdf_out)
    #response.headers['Content-Disposition'] = "attachment; filename="+ "pdfname"
    #response.mimetype = 'application/pdf'
    #return response
    

if __name__ == "__main__":
    app.run(debug=True)
