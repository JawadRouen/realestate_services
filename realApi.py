from realestate import *
from flask import Flask, request, make_response, jsonify, json
import io
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


if __name__ == "__main__":
    app.run(debug=True)
