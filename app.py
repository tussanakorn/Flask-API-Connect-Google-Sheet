## google sheet
import geopy.distance as ps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("checkname").sheet1

data = sheet.get_all_records()
listdata = pd.DataFrame(data)
print(listdata)

# web service
from flask import Flask , jsonify, request
app = Flask(__name__)

def loadStudent():
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    return listdata

def searchStudent(customer):
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    students = listdata[listdata['customer_id'] == customer ]
    return students

@app.route('/checkStudents' , methods=['GET'])
def CheckStudent():
    try:
        customer = request.args.get('customer_id')
        display_name = request.args.get('p_display_name')
        profile_img = request.args.get('p_profile_img_url')
        Name = request.args.get('Name')
        Nickname = request.args.get('Nickname')
        StudentID = request.args.get('StudentID')
        status = request.args.get('status')
     
        res = loadStudent()
        row = [ customer ,display_name , profile_img  , str(Name), str(Nickname), int(StudentID), str(status)  ]
        index = int(len(res)+2)
        sheet.insert_row(row, index)
        return jsonify({'message' : "เช็คชื่อเรียบร้อยแล้วนะครับ",
                        "name" : display_name,
                        "profile"  : profile_img,
                        "Name"  : Name,
                        "Nickname"  : Nickname,
                        "StudentID"  : StudentID,
                        "status" : status
                        })
    except Exception as e:
        return jsonify({'message' : 'error นะ ลองดูใหม่อีกที'})


if __name__ == '__main__':
    app.run(debug=True)