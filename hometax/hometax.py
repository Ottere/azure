# -*- coding: utf-8 -*-
from urllib.parse import DefragResult
from flask import Flask, render_template, request,redirect, url_for, flash,jsonify, send_file, session,escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,text,update
import json
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql.elements import Null
from werkzeug.utils import secure_filename
import os, sys, re
import random, string
import pymysql
import sqlalchemy 
from itertools import groupby
# from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from urllib.request import urlretrieve

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)
app.secret_key = "Secret Key" #보안키 설정 (암호화)
# 이곳에서 sqlite3 연결
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/hometax.db' # ///뒷 부분은 본인의 db파일 이름을 사용하면 됌. *현재 sqlite3 사용중 -> 추후 mariadb로 변경 예정
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# orm db 선언문1
db = SQLAlchemy(app)
class tblErpTaxBillTrans(db.Model):
    __tablename__="tblErpTaxBillTrans"
    TransSeq=db.Column(db.Integer,primary_key = True)
    FromSaupjaRegNo=db.Column(db.String(20))
    FromSaupjangNo=db.Column(db.String(10))
    FromSaupjaName=db.Column(db.String(30))
    FromDaepyoName=db.Column(db.String(30))
    FromSaupjangAd=db.Column(db.String(100))
    FromUptae=db.Column(db.String(30))
    FromJongmok=db.Column(db.String(30))
    FromEmailAddr1=db.Column(db.String(100))
    ToSaupjaRegNo=db.Column(db.String(20))
    ToSaupjangNo=db.Column(db.String(10))
    ToSaupjaName=db.Column(db.String(30))
    ToDaepyoName=db.Column(db.String(30))
    ToSaupjangAddr=db.Column(db.String(100))
    ToUptae=db.Column(db.String(30))
    ToJongmok=db.Column(db.String(30))
    ToEmailAddr1=db.Column(db.String(100))
    ToEmailAddr2=db.Column(db.String(100))
    HomeTaxApprNo=db.Column(db.String(40))
    RegDate=db.Column(db.String(10))
    AmtUnc=db.Column(db.String(13))
    AmtTax=db.Column(db.String(13))
    EditSayoo=db.Column(db.String(40))
    AmtTot=db.Column(db.String(13))
    AmtCash=db.Column(db.String(13))
    AmtSupyo=db.Column(db.String(13))
    AmtUEum=db.Column(db.String(13))
    AmtMisu=db.Column(db.String(13))
    GubunRequPay=db.Column(db.String(4))
    FlowProcYN=db.Column(db.String(1))
    SyncIndex=db.Column(db.String(20))
    CorpCode=db.Column(db.String(6))
    def __init__(self,TransSeq,FromSaupjaRegNo,FromSaupjangNo,FromSaupjaName,FromDaepyoName,FromSaupjangAd,FromUptae,FromJongmok,FromEmailAddr1,ToSaupjaRegNo,ToSaupjangNo,ToSaupjaName,ToDaepyoName,ToSaupjangAddr,ToUptae,ToJongmok,ToEmailAddr1,ToEmailAddr2,HomeTaxApprNo,RegDate,AmtUnc,AmtTax,EditSayoo,AmtTot,AmtCash,AmtSupyo,AmtUEum,AmtMisu,GubunRequPay,FlowProcYN,SyncIndex,CorpCode):
        self.TransSeq=TransSeq
        self.FromSaupjaRegNo=FromSaupjaRegNo
        self.FromSaupjangNo=FromSaupjangNo
        self.FromSaupjaName=FromSaupjaName
        self.FromDaepyoName=FromDaepyoName
        self.FromSaupjangAd=FromSaupjangAd
        self.FromUptae=FromUptae
        self.FromJongmok=FromJongmok
        self.FromEmailAddr1=FromEmailAddr1
        self.ToSaupjaRegNo=ToSaupjaRegNo
        self.ToSaupjangNo=ToSaupjangNo
        self.ToSaupjaName=ToSaupjaName
        self.ToDaepyoName=ToDaepyoName
        self.ToSaupjangAddr=ToSaupjangAddr
        self.ToUptae=ToUptae
        self.ToJongmok=ToJongmok
        self.ToEmailAddr1=ToEmailAddr1
        self.ToEmailAddr2=ToEmailAddr2
        self.HomeTaxApprNo=HomeTaxApprNo
        self.RegDate=RegDate
        self.AmtUnc=AmtUnc
        self.AmtTax=AmtTax
        self.EditSayoo=EditSayoo
        self.AmtTot=AmtTot
        self.AmtCash=AmtCash
        self.AmtSupyo=AmtSupyo
        self.AmtUEum=AmtUEum
        self.AmtMisu=AmtMisu
        self.GubunRequPay=GubunRequPay
        self.FlowProcYN=FlowProcYN
        self.SyncIndex=SyncIndex
        self.CorpCode=CorpCode

class tblErpTaxBillTransitem(db.Model):
    __tablename__="tblErpTaxBillTransitem"
    TransSeq=db.Column(db.Integer,primary_key = True)
    ItemNo=db.Column(db.Integer,primary_key = True)
    Mm=db.Column(db.String(2))
    Dd=db.Column(db.String(2))
    Pummok=db.Column(db.String(200))
    Spec=db.Column(db.String(20))
    Cnt=db.Column(db.String(50))
    Unc=db.Column(db.String(50))
    Amt=db.Column(db.String(50))
    Tax=db.Column(db.String(50))
    Bogo=db.Column(db.String(200))
    def __init__(self,TransSeq,ItemNo,Mm,Dd,Pummok,Spec,Cnt,Unc,Amt,Tax,Bogo):
        self.TransSeq=TransSeq
        self.ItemNo=ItemNo
        self.Mm=Mm
        self.Dd=Dd
        self.Pummok=Pummok
        self.Spec=Spec
        self.Cnt=Cnt
        self.Unc=Unc
        self.Amt=Amt
        self.Tax=Tax
        self.Bogo=Bogo


@app.route("/hometax") #기본화면
def index():
    all_data = tblErpTaxBillTrans.query.order_by(tblErpTaxBillTrans.RegDate.desc()).all() #현재 DB에 들어있는 데이터를 날짜기준 내림차순으로 가져와서 넘겨줌
    return render_template("list.html",all_data=all_data)

@app.route('/hometax/company',methods=['GET','POST'])
def get_company():
    CompanyNo = request.form['SendNo'] #사업자번호
    print(CompanyNo)
    options=webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path='/home/azure_admin/hometax/chromedriver', options=options) #각자 (경로)/chromedriver.exe하면 됌
    driver.maximize_window() #전체화면으로 실행
    driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초가지 기다린다.
    hometex='https://www.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml' #URL
    driver.get(hometex)

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="textbox81212923"]').click()

    time.sleep(3)

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "txppIframe"))) #로그인화면 iframe
    driver.switch_to.frame(element) #iframe 스위치 (change)

    driver.find_element_by_xpath('//*[@id="sub_a_0108010000"]').click()


    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="bsno"]').send_keys(CompanyNo)
    time.sleep(1)

    Btn=driver.find_element_by_xpath('//*[@id="trigger5"]')
    driver.execute_script("arguments[0].click();",Btn)

    time.sleep(3)
    result_list=[]
    buga = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "grid2_cell_0_1"))).text
    # result_list.append({"buga":buga})
    result_list.append(buga)
    saup = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "grid2_cell_0_0"))).text
    # result_list.append({"saup":saup})
    result_list.append(saup)
    search = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "grid2_cell_0_2"))).text
    # result_list.append({"search":search})
    result_list.append(search)

    result_dict = {i : result_list[i] for i in range(len(result_list))}
    print(result_dict)
    # str(buga),str(saup),str(search)
    json_list = json.dumps(result_list,ensure_ascii=False)
    print(json_list)
    return result_dict


@app.route("/hometax/crawling")
def get_data():
    options=webdriver.ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # chrome 드라이버 chrome 버전에 맞게 다운후 위치변경
    driver = webdriver.Chrome(executable_path='/home/azure_admin/hometax/chromedriver', options=options) #또는 chromedriver.exe 각자 (경로)/chromedriver.exe하면 됌
    driver.maximize_window() #전체화면으로 실행
    driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초가지 기다린다.

    hometex='https://www.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml' #URL
    driver.get(hometex)

    time.sleep(3)

    selecte_box=driver.find_element_by_xpath('//*[@id="textbox81212912"]') #메인화면 로그인 버튼
    selecte_box.click()
    #공동.금융인증서 뜰때까지 대기하고 iframe 접속
    element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "txppIframe"))) #로그인화면 iframe
    driver.switch_to.frame(element) #iframe 스위치 (change)

    time.sleep(2)
    #공동.금융인증서 클릭
    selecte_box=driver.find_element_by_xpath('//*[@id="anchor22"]') #로그인화면 로그인 버튼
    selecte_box.click()
    time.sleep(3)

    # 인증서 선택창 제어
    # 인증서 선택창 iframe 접속
    element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "dscert")))
    driver.switch_to.frame(element)
    # 브라우저 클릭
    time.sleep(3)
    selecte_box=driver.find_element_by_xpath('//*[@id="stg_web_kftc"]').click()
    # 사용할 인증서 내용이 뜰때까지 대기
    element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[9]/div[2]/div[2]/div[1]/div[6]/div/div[2]/div/div[4]/div[2]/div/table/tbody/tr/td")))

    # companyName의 회사 이름을 바꾸면 비밀번호가 바뀜
    companyName='지오유'
    if companyName=='지오유':
        findName='(주)지오유(zioyou)0004681103055148'
        inputPass='!@#ziou1570'
    elif companyName=='이가자연면':
        findName='(주)이가자연면_0001588512'
        inputPass='dlrkaus#357'

    # companyName의 회사 이름을 바꾸게 되면 findName의 이름도 바뀌는데 인증서가 여러가지일때 해당 인증서를 선택
    driver.find_element_by_css_selector('[title^="'+str(findName)+'"]').click()
    # 비밀번호 입력
    selecte_box=driver.find_element_by_xpath('//*[@id="input_cert_pw"]').send_keys(inputPass)
    # 확인 클릭
    selecte_box=driver.find_element_by_xpath('//*[@id="btn_confirm_iframe"]')
    selecte_box.click()
    driver.switch_to.default_content()

    try:
    # 로그인 했을때 팝업 iframe 접속
        element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "UTXPPABB29_iframe")))
        driver.switch_to.frame(element)
        # 닫기 버튼 클릭
        driver.find_element_by_xpath('//*[@id="btnCloseInvtSpec"]').click()
        driver.switch_to.default_content()
    except:
        pass
    time.sleep(1)
    # 조회/발급 버튼이 생길때 까지 대기하다가 클릭
    selecte_box = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="group1300"]')))
    selecte_box.click()
    time.sleep(1)
    # 조회/발급 클릭하고 생기는 iframe 접속
    element = driver.find_element_by_id("txppIframe")
    driver.switch_to.frame(element)
    # 전자(세금) 계산서의 목록조회 클릭
    selecte_box=driver.find_element_by_xpath('//*[@id="sub_a_0104020000"]')
    selecte_box.click()
    time.sleep(1)
    # 목록조회를 클릭하면 나오는 발급목록조회 클릭
    selecte_box=driver.find_element_by_xpath('//*[@id="sub_a_0104020100"]')
    selecte_box.click()
    # iframe 나가기
    driver.switch_to.default_content()
    # 발급목록조회를 클릭했을때 생기는 iframe 접속
    element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'txppIframe')))
    driver.switch_to.frame(element)

    # 조회기간 오른쪽 맨 끝에있는 3개월 클릭
    time.sleep(2)
    selecte_box = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="btnChk3"]')))
    selecte_box.click()
    #조회하기 클릭
    selecte_box=driver.find_element_by_xpath('//*[@id="group1744"]')
    selecte_box.click()
    time.sleep(3)
    # 조회하기를 눌렀을때 아래 나오는 테이블의 목록 테이블의 테이터 가져오기
    all_table_list=driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[3]/div[5]/div/div[2]/div/table/tbody/tr') # 목록 테이블 데이터

    # 목록 리스트 수평 스크롤바를 오른쪽으로 이동
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    datalist = driver.find_element_by_xpath('//*[@id="resultGrid_scrollX_right"]')
    driver.execute_script("arguments[0].scrollBy(1500,0)",datalist)

    # 아래 페이지 넘버 오른쪽 끝에있는 페이지의 총 계수 가져오기
    time.sleep(2)
    number=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[7]/div/div/div[2]/p/span[7]') #페이지 (쪽) 수 가져오기
    divide=int(number.text)//10+2

    # 반복작업을 하기위해 함수 선언 처음에는 여기가 아닌 아래쪽에서 시작 418번줄 for문부터 시작 
    def reply():
        new_data = ''
        for i in range(3,13): # 3~12
            time.sleep(2)
            try:
                liclick=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[7]/div/div/div[1]/ul/li['+str(i)+']') # 1부터 차례대로 시작하여 10쪽이 되면 종료
                print(liclick.text)
                liclick.click()
            except:
                print('done') # 페이지 쪽수가 10번을 넘었을때 return으로 돌아감
                return 'ok'
            for index,value in enumerate(all_table_list, start=1): # 아까 가져온 목록테이블의 개수 가져오기 index에 1부터 차례대로 시작하여 10이되면 종료

                print(index)
                time.sleep(3)
                try:
                    # 맨 위에있는 목록 테이블의 데이터부터 상세보기 클릭
                    element1=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[5]/div/div[2]/div/table/tbody/tr['+str(index)+']/td[25]/span/button') # 해당 리스트의 상세보기 버튼
                    element1.click()
                except:
                    print('doneli') # 완료시 종료
                    return
                time.sleep(3)
                #상세 조회를 눌렀을때 생기는 iframe 접속
                element = driver.find_element_by_id("UTEETBDA38_iframe") # 상세조회 iframe 이동
                driver.switch_to.frame(element)

                
                HomeTaxApprNo=driver.find_element_by_xpath('//*[@id="etanInputboxId"]').get_attribute("value") #승인번호 가져오기
                
                ApprNoData=tblErpTaxBillTrans.query.filter(tblErpTaxBillTrans.HomeTaxApprNo==HomeTaxApprNo).first() # db에 현재 승인번호와 일치하는게 있는지 확인
                print(HomeTaxApprNo,ApprNoData)

                coun=db.session.query(func.max(tblErpTaxBillTrans.TransSeq)).scalar() #TransSeq 필드에 최대값을 가져옴
            
                #######
                # DB에 값이 존재하지 않으면서 새로운 데이터를 받을때 (첫 시도일때)

                if coun==None: # TransSeq 필드에 최대값을 가져왔을떄 아무것도 가져오지 않는다면 db에 데이터가 없는 것이기 때문에 1로 지정하고 시작 TransSeq 필드는 고유 pk값이기 떄문에 중복될수 없음
                    TransSeq=1

                #######
                # DB에 값이 존재하면서 새로운 값을 받을때 (새로운 날짜 업데이트시)

                elif coun is not None: # TransSeq 필드에 기존 값이 존재할때 최대값을 가져온 상태에서 +1해줌으로서 값이 중복이 되지않게 설정 만약 pk값이 중복이 되면 오류 발생
                    TransSeq=coun+1 
                    
                    if ApprNoData is None: # 위에서 승인번호를 사져오고 비교를 했을때 None이 되면 중복되는 승인번호가 없다는 뜻이고 가져온 데이터가 아니기 때문에 pass를 통해 다음 코드에 진입
                        print('pass')
                        pass
                    else:
                        print('break') # None이 아닐때 승인번호 중복값이 있다는 뜻이 되기 때문에 가져온 데이터를 또 가져올수 없으니까 break로 for문 탈출
                        break

                ######
                # 상세보기를 눌렀을때 빨간색 공급자와 파란색 공급받는자의 데이터를 모두 가져옴
                FromSaupjaRegN=driver.find_element_by_xpath('//*[@id="textbox1062"]').text
                FromSaupjangNo=driver.find_element_by_xpath('//*[@id="textbox1063"]').text
                FromSaupjaName=driver.find_element_by_xpath('//*[@id="textbox1065"]').text
                FromDaepyoNam=driver.find_element_by_xpath('//*[@id="textbox1066"]').text
                FromSaupjangAd=driver.find_element_by_xpath('//*[@id="textbox1067"]').text
                FromUptae=driver.find_element_by_xpath('//*[@id="textbox1068"]').text
                FromJongmok=driver.find_element_by_xpath('//*[@id="textbox1069"]').text
                FromEmailAddr1=driver.find_element_by_xpath('//*[@id="textbox1070"]').text
                ToSaupjaRegNo=driver.find_element_by_xpath('//*[@id="textbox1071"]').text
                ToSaupjangNo=driver.find_element_by_xpath('//*[@id="textbox1128"]').text
                ToSaupjaName=driver.find_element_by_xpath('//*[@id="textbox1073"]').text
                ToDaepyoName=driver.find_element_by_xpath('//*[@id="textbox1074"]').text
                ToSaupjangAddr=driver.find_element_by_xpath('//*[@id="textbox1075"]').text
                ToUptae=driver.find_element_by_xpath('//*[@id="textbox1076"]').text
                ToJongmok=driver.find_element_by_xpath('//*[@id="textbox1077"]').text
                ToEmailAddr1=driver.find_element_by_xpath('//*[@id="textbox1078"]').text
                ToEmailAddr2=driver.find_element_by_xpath('//*[@id="textbox1079"]').text
                
                RegDate=driver.find_element_by_xpath('//*[@id="textbox1090"]').text
                AmtUnc=driver.find_element_by_xpath('//*[@id="textbox1091"]').text
                AmtTax=driver.find_element_by_xpath('//*[@id="textbox1092"]').text
                EditSayoo=driver.find_element_by_xpath('//*[@id="textbox1093"]').text
                AmtTot=driver.find_element_by_xpath('//*[@id="textbox1120"]').text
                AmtCash=driver.find_element_by_xpath('//*[@id="textbox1121"]').text
                AmtSupyo=driver.find_element_by_xpath('//*[@id="textbox1122"]').text
                AmtUEum=driver.find_element_by_xpath('//*[@id="textbox1123"]').text
                AmtMisu=driver.find_element_by_xpath('//*[@id="textbox1124"]').text
                GubunRequPay=driver.find_element_by_xpath('//*[@id="textbox1126"]').text
                FlowProcYN=None
                SyncIndex=None
                CorpCode=None
                print(HomeTaxApprNo)

                for j in range(1,5): # 4번 반복
                    # tblErpTaxBillTransitem 테이블 데이터
                    # 빨간색 공급자와 파란색 공급받는자 아래 있는 데이터들도 가져옴
                    itemNo=j
                    Mn=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[1]').text
                    Dd=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[2]').text
                    Pummok=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[3]').text
                    if Pummok=='': # 4번 반복하는데 만약에 품목이 공백이면 내용이 없다는 뜻이기 때문에 break로 탈출
                        break
                    Spec=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[4]').text
                    Cnt=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[5]').text
                    if Cnt == '':
                        Cnt=None
                    Unc=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[6]').text
                    if Unc == '':
                        Unc=None
                    Amt=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[7]').text
                    
                    if Amt == '':
                        Amt=None
                    Tax=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[8]').text
                    if Tax == '':
                        Tax=None
                    
                    Bogo=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[1]/div[2]/div/table/tbody/tr['+str(j)+']/td[9]').text
                    # tblErpTaxBillTransitem 테이블에 데이터 넣기
                    inputScDb = tblErpTaxBillTransitem(TransSeq,itemNo,Mn,Dd,Pummok,Spec,Cnt,Unc,Amt,Tax,Bogo) 
                    db.session.add(inputScDb)
                # tblErpTaxBillTrans 테이블에 데이터 넣어주고 conmmit을 함으로써 데이터 저장 완료 커밋은 마지막에 한번해도 동작 가능
                inputDb = tblErpTaxBillTrans(TransSeq,FromSaupjaRegN,FromSaupjangNo,FromSaupjaName,FromDaepyoNam,FromSaupjangAd,FromUptae,FromJongmok,FromEmailAddr1,ToSaupjaRegNo,ToSaupjangNo,ToSaupjaName,ToDaepyoName,ToSaupjangAddr,ToUptae,ToJongmok,ToEmailAddr1,ToEmailAddr2,HomeTaxApprNo,RegDate,AmtUnc,AmtTax,EditSayoo,AmtTot,AmtCash,AmtSupyo,AmtUEum,AmtMisu,GubunRequPay,FlowProcYN,SyncIndex,CorpCode) 
                db.session.add(inputDb)
                db.session.commit()
                print('데이터 추가 완료')

                # 하나의 상세조회 데이터 크롤링 완료후 닫기 버튼 클릭
                selecte_box=driver.find_element_by_xpath('/html/body/div[1]/div[5]/a/input') #닫기버튼 
                selecte_box.click()
                # iframe 접속 종료
                driver.switch_to.default_content()
                # 닫기 버튼을 눌렀을때 나오는 화면의 iframe에 다시 접속
                element = driver.find_element_by_id("txppIframe")
                driver.switch_to.frame(element)
                
    # 여기서부터 시작
    for i in range(1,divide): # 페이지 넘김 번호 
        reply() # 위에 선언한 함수 실행
        # 위에서 return으로 함수 나올때 이곳에서 다시 시작 break는 for문 하나를 나가는 것이고 return 은 reply 함수 자체를 나가기 때문에 두개를 잘 구분
        time.sleep(2)
        try:
            # 10페이지까지 완료한 상태에서 화살표 클릭 하고 난후 바로 위에있는 reply 함수 재진입
            leftbtn=driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div[7]/div/div/div[1]/ul/li[13]')
            leftbtn.click()
        except:
            # 더이상의 화살표가 없으면 끝난것으로 확인후 break로 for문 탈출
            print('done!')
            break
    # chrome 종료
    driver.quit()



if __name__=="__main__":
    app.debug =True
    app.run(host='0.0.0.0',port='5003')
