from flask import Flask, render_template, request, redirect, url_for
import random
import datetime
import gspread
from google.oauth2 import service_account

app = Flask(__name__)

# 구글 서비스 계정 키 파일 경로
KEY_FILE = 'C:\\Users\\qwasq\\OneDrive\\바탕 화면\\코딩\\noshoping-388704-cdb766214bbe.json'

def connect_spreadsheet():
    print(KEY_FILE)  # 추가
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    client = gspread.authorize(credentials)
    return client

# 사용자 선택 정보 저장 함수
def save_user_selection(image_name, page_load_time, submission_time):
    client = connect_spreadsheet()
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/10_BAdLhEr_uQsKL7CZTCDq0VEO3f4EllG502M1BuiQ8/edit#gid=0')

    # 시트 1을 가져옵니다
    sheet = spreadsheet.get_worksheet(0)

    sheet.append_row([image_name, str(page_load_time), str(submission_time)])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        page_load_time = datetime.datetime.strptime(request.form['page_load_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        image_checkbox = request.form.getlist('image_checkbox')  # 이미지 체크박스 값 가져오기

        for image_name in image_checkbox:
            save_user_selection(image_name, page_load_time, submission_time)

        return redirect(url_for('thank_you'))

    # GET 요청일 때
    image_names = ['{}.jpg'.format(i) for i in range(1, 101)]  # 이미지 파일명 리스트 초기화
    random.shuffle(image_names)  # 이미지 파일명 리스트를 랜덤하게 섞음
    return render_template('index.html', image_names=image_names)

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
