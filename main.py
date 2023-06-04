# try link dialogflow
import os
import google.cloud.dialogflow_v2 as dialogflow
from flask import Flask, request
import json
from flask import make_response
from bs4 import BeautifulSoup
import requests
import openpyxl
import numpy

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'movie-recommend-373311-42df2701aa4f.json'  # 剛剛下載的金鑰 json
project_id = 'movie-recommend-9lrj'# dialogflow 的 project id
language = 'zh-TW' # 語系
session_id = '7cdf2a08-c41d-4110-be14-5097723bc489-c4fd3c84'   # 自訂義的 session id

def dialogflowFn(text):
    session_client = dialogflow.SessionsClient()                   # 使用 Token 和 dialogflow 建立連線
    session = session_client.session_path(project_id, session_id)  # 連接對應專案
    text_input = dialogflow.types.TextInput(text=text, language_code=language)  # 設定語系
    query_input = dialogflow.types.QueryInput(text=text_input)     # 根據語系取得輸入內容
    try:
        response = session_client.detect_intent(session=session, query_input=query_input) # 連線 Dialogflow 取得回應資料
        print("input:", response.query_result.query_text)
        print("intent:", response.query_result.intent.display_name)
        print("reply:", response.query_result.fulfillment_text)
        return response.query_result.fulfillment_text    # 回傳回應的文字
    except:
        return 'error'

app = Flask(__name__)
@app.route("/")
def home():
   text = request.args.get('text')   # 取得輸入的文字
   reply = dialogflowFn(text)        # 取得 Dialogflow 回應的文字
   return reply

@app.route('/webhook', methods=['POST'])
def webhook():
   req = request.get_json()    # 轉換成 dict 格式
   # print(req)
   res=makeWebhookResult(req) 
   res =json.dumps(res,indent=4)
   r = make_response(res)#將接收的文字回傳
   r.headers['Content-Type'] = 'application/json'
   print(r)
   return r

def makeWebhookResult(req):
   movie_list=[] #推薦列表
   movie_recom=""
   query_result=req.get("queryResult")
   if query_result.get('action')=="movie_find": #取得電影類別，推薦電影
      req1=req.get("queryResult")
      param=req1.get("parameters")
      type=param.get("movie_type")
      if type=="全部電影": #全部電影
        file_name="movie_list"
      elif type=="Deals on movie purchases" or type=="Deals on recent releases" or type=="Most popular movies" or type=="New to Rent" or type=="Offers on movie rentals" or type=="Top new movie releases to rent or buy" or type=="Analysis with NLP":
         file_name=type
      wb = openpyxl.load_workbook(file_name+".xlsx") #輸入隨便則回傳所有電影的排行
      ws = wb.active
      myList = [row for row in ws.values]
      myArr = numpy.array(myList)
      for i in range(1,11): #推薦的數量
         string=" "+str(i)+". "+myArr[i][1]+"\n"
         movie_list.append(string)
      movie_recom= "".join(movie_list) #列表轉字串
      #其他類別也用if去判斷，再開啟不同的檔案
      fullfillmentText="以下是"+type+"類的電影排行榜\n"+movie_recom+"輸入您想看的電影，我們可以為您提供電影的相關資訊" #回傳的文字
   
   if query_result.get('action')=="movie_find_info": #取得查看哪個資訊
      req1=req.get("queryResult")
      param=req1.get("parameters")
      global movie_name
      movie_name=param.get("movie_name")
      fullfillmentText="好的，輸入「1」可以查看電影簡介，輸入「2」可以查看電影預告片，輸入「3」可以查看電影在Google電影中的星等。\n請輸入您想查看的電影資訊：" 
   
   if query_result.get('action')=="info_input": #回傳電影資訊
      info_num={"1":"電影簡介:","2":"電影預告片:","3":"電影星等"}
      req1=req.get("queryResult")
      param=req1.get("parameters")
      num=param.get("movie_info")
      wb = openpyxl.load_workbook("movie_list.xlsx")
      ws = wb.active
      myList = [row for row in ws.values]
      myArr = numpy.array(myList)
      for i in range(1,len(myArr)):
         if myArr[i][1]==movie_name:
            index=i
      if num=="1":
         describe=myArr[index][5]
         if describe=="":
            describe="暫無電影簡介"
         fullfillmentText="以下是"+movie_name+"的"+info_num[num]+"\n"+describe
      elif num=="2":
         trailer=myArr[index][6]
         if trailer=="":
            trailer="暫無預告片"
         fullfillmentText="以下是"+movie_name+"的"+info_num[num]+"\n"+trailer
      elif num=="3":
         star=myArr[index][2]
         if star=="":
            star="暫無星等"
         fullfillmentText=movie_name+"在google電影上的"+info_num[num]+"為"+str(star)
      else:
         fullfillmentText="請重新輸入電影名稱"

   #以下為使用者輸入的情況
   if query_result.get('action')=="movie_input": #取得即時爬蟲的電影名稱，先做爬蟲
      req1=req.get("queryResult")
      param=req1.get("parameters")
      global movie_name1,trailer1,describe1,tomato
      movie_name1=param.get("new_movie_name")
      url="https://play.google.com/store/search?q="+movie_name1+"&c=movies&hl=zh_TW&gl=US"
      r=requests.get(url)
      resp = BeautifulSoup(r.text, 'html.parser') 
      detail="https://play.google.com"+resp.find("a","Si6A0c ZD8Cqc").get("href")
      print(detail)
      r1=requests.get(detail)
      resp1 = BeautifulSoup(r1.text, 'html.parser') 
      describe1=resp1.find('div','bARER').text
      try:
         star=resp1.find('div', 'jILTFe').text.replace('\n','').replace(' ','').replace('star','')
      except:
         star="無"
      try:
         trailer1 = resp1.find('div','kuvzJc').find("button").get("data-trailer-url")
      except:
         trailer1 = None
      fullfillmentText="好的，"+movie_name1+"在Google電影中的星評為"+str(star)+"顆星。\n另外，輸入「A」可以查看電影簡介，輸入「B」可以查看電影預告片。\n請輸入您想查看的電影資訊："
  
   if query_result.get('action')=="info_input1": #取得回傳資訊的代碼，回傳電影資訊
      req1=req.get("queryResult")
      param=req1.get("parameters") 
      num1=param.get("movie_info")
      if num1=="A":
         fullfillmentText="以下是"+movie_name1+"的電影簡介：\n"+describe1
      if num1=="B":
         fullfillmentText="以下是"+movie_name1+"的電影預告片：\n"+trailer1
         
   return {
            "fulfillmentMessages": [
               {
                  "text": {
                  "text": [
                     fullfillmentText
                  ]
                  }
               }
            ]
            }
app.run("127.0.0.1",port=80) #改成自己ngrok的ip和port 執行之後再去LINE那邊測試
