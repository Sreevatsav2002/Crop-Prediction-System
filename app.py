from flask import Flask,render_template,request, redirect
import pickle
import numpy as np
app = Flask(__name__)

Label_mapping = {0: ['Apple', 'images/Apple.jpg'], 1: ['Banana', 'images/banana.jpg'], 2: ['Blackgram', 'http://shorturl.at/duFLR'], 
                 3: ['Chickpea', 'https://shorturl.at/cfkrG'], 
                 4: ['Coconut', 'http://shorturl.at/bmrOY'], 5: ['Coffee', 'http://shorturl.at/bxFHQ'], 6: ['Cotton', 'http://shorturl.at/lwIPZ'], 
                 7: ['Grapes', 'http://shorturl.at/bqKS8'], 8: ['Jute', 'http://shorturl.at/abfzK'], 
                 9: ['Kidneybeans', 'http://shorturl.at/aouRY'], 10: ['Lentil', 'http://shorturl.at/mxL36'], 
                 11: ['Maize', 'https://shorturl.at/mpBZ4'], 12: ['Mango', 'https://shorturl.at/kxDE0'], 13: ['Mothbeans', 'https://shorturl.at/mwOQ0'], 
                 14: ['Mungbean', 'https://shorturl.at/bACY2'], 15: ['Muskmelon', 'images/muskmelon.jpg'], 16: ['Orange', 'https://shorturl.at/iCEOX'], 
                 17: ['Papaya', 'https://shorturl.at/xD189'], 18: ['Pigeonpeas', 'https://shorturl.at/bvNXZ'], 
                 19: ['Pomegranate', 'http://shorturl.at/syIJ8'], 20: ['Rice', 'https://shorturl.at/ajoCD'], 21: ['Watermelon', 'http://shorturl.at/aiuDG']}

norm_data = {'N': 140,
 'P': 145,
 'K': 205,
 'temperature': 43.67549305,
 'humidity': 99.98187601,
 'ph': 9.93509073,
 'rainfall': 298.5601175}

model = pickle.load(open("Crop_Prediction_Model.pkl", 'rb'))

def ValuePredictor(arr):
    to_predict = np.array(arr).reshape(1,-1)
    model = pickle.load(open("Crop_Prediction_Model.pkl", "rb"))
    result = model.predict(to_predict)
    return result[0]

def norm(x):
    key = list(norm_data.keys())
    x_norm = x
    n = len(x)
    for i in range(n):
        x_norm[i] = x[i] / norm_data[key[i]]
    return np.array(x_norm)



@app.route("/",methods = ['GET','POST'])
def Manual():
    N,P,K,rain,temp,humd,pH = 0,0,0,0,0,0,0
    a = ["Please enter the neccessary details",'https://shorturl.at/iBIOU']
    if request.method == 'POST': 
        N = float(request.form['N'] if request.form['N'] else 0)
        P = float(request.form['P'] if request.form['P'] else 0)
        K = float(request.form['K'] if request.form['K'] else 0)
        rain = float(request.form['rain'] if request.form['rain'] else 0)
        temp = float(request.form['temp'] if request.form['temp'] else 0)
        humd = float(request.form['humd'] if request.form['humd'] else 0)
        pH = float(request.form['pH'] if request.form['pH'] else 0)
        arr = [N, P, K, temp, humd, pH, rain]
        arr = norm(arr)
        res = Label_mapping[ValuePredictor(arr)]
        return render_template("manual.html", a = res)
    return render_template("manual.html",a = a)



if __name__ == "__main__":
    app.run(debug = True,port = 8000)