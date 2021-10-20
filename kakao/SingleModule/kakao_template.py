# -*- coding: utf-8 -*-
from urllib.parse import DefragResult
from flask import Flask, render_template, request,redirect, url_for, flash,jsonify, send_file, session,escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,text,update
from datetime import datetime
from sqlalchemy.sql.elements import Null
import os, sys, re, time, random, string, pymysql, sqlalchemy, json, requests
# from requests.api import request

def kakao_msg_template(url,headers,clickFriendList):
    data={
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        "template_id" : 61896,
        'template_args' : '{"title":"방금, 신용카드가 결제되었습니다."}'
        }
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    data={
        "template_id" : 61894,
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        'template_args' : '{"title":"대도식당 동백지점에서 250,400원 국민카드 결재","BtnName":"매출전표보기"}'
    }

    response = requests.post(url, headers=headers, data=data)
    response.status_code

    data={
        "template_id" : 61910,
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        'template_args' : '{"title":"대도식당 동백지점은 사업자 상태는 정상상태이며, 용인시 처인구 동백지구에 위치해 있습니다.","BtnName":"지도로보기"}'
        }

    response = requests.post(url, headers=headers, data=data)
    response.status_code

    data={
        "template_id" : 61911,
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        'template_args' : '{"title":"비과세 가맹점입니다. 10% 부가세를 추가적으로 내셨다면 불법입니다.","BtnName":"신고하기"}'
        }
    response = requests.post(url, headers=headers, data=data)
    response.status_code

    data={
        "template_id" : 61918,
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        'template_args' : '{"title":"자동으로 분류된 계정과목은 접대비 입니다. (가맹점 + 과거이 력 근거)"}'
        }

    response = requests.post(url, headers=headers, data=data)
    response.status_code

    data={
        "template_id" : 61914,
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        'template_args' : '{"title":"이 가맹점에서 3일전 (9월 15일 오후 4시) 142,000원을 결제한 이력이 존재합니다.","BtnName":"사용이력 보기"}'
        }

    response = requests.post(url, headers=headers, data=data)
    response.status_code

    data={
        "template_id" : 61896,
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        'template_args' : '{"title":"국민카드의 한도는, 1,204,650원이 남았습니다."}'
        }

    response = requests.post(url, headers=headers, data=data)
    response.status_code

    data={
        "template_id" : 61896,
        "receiver_uuids": '["{}"]'.format(clickFriendList),
        'template_args' : '{"title":"세부 사용용도를 입력해주세요."}'
        }

    response = requests.post(url, headers=headers, data=data)
    response.status_code

def aaa () :
    print (1+2)
