import numpy as np
from flask import Flask, request, jsonify, render_template
import newsrecommenderassignment
import sys
app = Flask(__name__)
output_list=[]
user_id=0
k=0
counter_var = 0
counter_var_2 = 0
#updated_ratings = [0]*10
@app.route('/')
def home():
    #don't want to run this for the first time
    global counter_var
    if counter_var == 1:
        newsrecommenderassignment.selected_docs_final,newsrecommenderassignment.selected_docs_final_with_ID = newsrecommenderassignment.hybrid(newsrecommenderassignment.collaborative_recommender,newsrecommenderassignment.content_recommender,newsrecommenderassignment.rank_matrix,newsrecommenderassignment.cos_sim,newsrecommenderassignment.news_corpus)
    counter_var = 1
    return render_template('index.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    float_features = [float(x) for x in request.form.values()]
    final_features = [np.array(float_features)]
    global user_id,output,output2,output3,output4,output5,output6,output7,output8,output9,output10
    user_id = int(round(final_features[0][0],0))
    global output_list
    output_list = newsrecommenderassignment.selected_docs_final.iloc[user_id,:].tolist()
    
    #output = "News for " + #str(final_features)
    output = newsrecommenderassignment.selected_docs_final.iloc[user_id,0]
    output2 = newsrecommenderassignment.selected_docs_final.iloc[user_id,1]
    output3 = newsrecommenderassignment.selected_docs_final.iloc[user_id,2]
    output4 = newsrecommenderassignment.selected_docs_final.iloc[user_id,3]
    output5 = newsrecommenderassignment.selected_docs_final.iloc[user_id,4]
    output6 = newsrecommenderassignment.selected_docs_final.iloc[user_id,5]
    output7 = newsrecommenderassignment.selected_docs_final.iloc[user_id,6]
    output8 = newsrecommenderassignment.selected_docs_final.iloc[user_id,7]
    output9 = newsrecommenderassignment.selected_docs_final.iloc[user_id,8]
    output10 = newsrecommenderassignment.selected_docs_final.iloc[user_id,9]
    
    #global counter_var_2
    #if counter_var_2 == 0:
        #text1 = ""
        #text2 = ""
        #counter_var_2 = 1
    #else:
    text1 = "Logged in as "
    text2 = ": User "
    return render_template('index.html', text1=text1,text2=text2,user_name = user_id,prediction_text=' {}...'.format(output[0:100]),prediction_text_2=' {}...'.format(output2[0:100]),prediction_text_3=' {}...'.format(output3[0:100]),prediction_text_4=' {}...'.format(output4[0:100]),prediction_text_5=' {}...'.format(output5[0:100]),prediction_text_6=' {}...'.format(output6[0:100]),prediction_text_7=' {}...'.format(output7[0:100]),prediction_text_8=' {}...'.format(output8[0:100]),prediction_text_9=' {}...'.format(output9[0:100]),prediction_text_10=' {}...'.format(output10[0:100]))

@app.route('/news/<i>',methods=['POST', 'GET'])
def news(i):
    global k
    k = i   
    
    return render_template('news.html',news_body =' {}.'.format(output_list[int(i)])) 

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      time = request.form['Time spent']
      
      time=int(time)
      words=0
      for l in range(len(output_list[int(k)])):
        t = output_list[int(k)]
        if(t[l] == ' ' or t == '\n' or t == '\t'):
            words = words + 1      
      
      expected_time = 60*words/200
      print(time,expected_time,words)
      rating = int(round(time/expected_time,1)*10)
      print("new rating",rating)

      if rating > 10:
          rating =10
      print("new rating",rating)
      print("news no",newsrecommenderassignment.selected_docs_final_with_ID.iloc[int(user_id),int(k)])
      news_id = newsrecommenderassignment.selected_docs_final_with_ID.iloc[int(user_id),int(k)]
      newsrecommenderassignment.rank_matrix.iloc[user_id,news_id] = rating
      return render_template('index.html', prediction_text=' {}...'.format(output[0:100]),prediction_text_2=' {}...'.format(output2[0:100]),prediction_text_3=' {}...'.format(output3[0:100]),prediction_text_4=' {}...'.format(output4[0:100]),prediction_text_5=' {}...'.format(output5[0:100]),prediction_text_6=' {}...'.format(output6[0:100]),prediction_text_7=' {}...'.format(output7[0:100]),prediction_text_8=' {}...'.format(output8[0:100]),prediction_text_9=' {}...'.format(output9[0:100]),prediction_text_10=' {}...'.format(output10[0:100]))


if __name__ == "__main__":
    app.run()
