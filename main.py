from flask import Flask , render_template , request , jsonify 
import requests 
from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen as ureq
import logging 
import pymongo 

logging.basicConfig(filename = 'project_1.log' , level= logging.DEBUG)


client =   pymongo.MongoClient("mongodb+srv://rk7018295:rsquare369@cluster0.ckt1qtj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database_1 = client['game_database']

app = Flask(__name__)

@app.route('/' , methods = ['GET'])
def homepage() :
  return render_template('index.html')

@app.route('/review' , methods = ['GET' , 'POST'])
def resultpage() :
  if request.method == 'POST' :
    try :
      searchstring = request.form['content']
      collection = database_1[f"{searchstring}"]
      url = 'https://play.google.com/store/search?q='+ searchstring.replace(" " , '+') + '&c=apps&hl=en'
      uclient = ureq(url)
      gamepage = uclient.read()
      uclient.close()
      gamepage = bs(gamepage , 'html.parser')
      bigbox = gamepage.find_all('div' , {'class' : 'ULeU3b'})
      del(bigbox[0:3])
      review_box = []
      for i in bigbox :
        game_link = 'https://play.google.com' + i.a['href']
        game_page = requests.get(game_link)
        game_page = bs(game_page.text  , 'html.parser')
        title = game_page.find('span' , {'AfwdI'}).text
        reviews = game_page.find_all('div' , {'class' : 'EGFGHd'})
        
        for j in reviews :
          try :
            name =  j.find('div' , {'class' : 'X5PpBb'}).text
          except :
            logging.info("name not found")
          try :
            text = j.find('div' , {'class' : 'h3YV2d'}).text
          except :
            logging.info("content not found")
          try :
            rating = j.find('div' , {'class' : 'iXRFPc'})['aria-label']
          except :
            logging.info("rating not found")
          try :
            date = j.find('span' , {'class' : 'bp9Aid'}).text
          except :
            logging.info("date not found")
          my_dict = {'Game' : title , 'Name' : name , 'Comment' : text , 'Rating' : rating , 'Date' : date}
          collection.insert_one(my_dict)
          review_box.append(my_dict)

        #client =    pymongo.MongoClient("mongodb+srv://rk7018295:rsquare369@cluster0.ckt1qtj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        #database_1 = client['game_database']
        #collection = database_1['collection']
      #collection.insert_many(review_box)
        logging.info(f"log my final result ")
        
      return render_template("result.html" , reviews = review_box[0 : (len(review_box)-1)])      
    except Exception as e :
      logging.info(e)
      return 'something went wrong'
  else :
    return render_template('index.html')


if __name__ == '__main__' :
  app.run(host = '0.0.0.0')
