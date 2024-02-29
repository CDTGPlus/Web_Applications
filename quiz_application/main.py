from flask import Flask, render_template, request, redirect, url_for
import random
from quiz_data import quiz


app = Flask(__name__,template_folder='templates')
#read data and shuffle order
data = {}
ord_data = list(range(1,len(quiz)+1))
random.shuffle(ord_data)

for x in ord_data:
    data[x] = quiz[x]

right_ans = [data[n]['answers'][data[n]['correct']] for n in data.keys()]
corrected_ans = []

@app.route('/')
def start():

    entries = [str(x) for x in list(range(1,len(quiz)+1))]
    keys = list(data.keys())
    zd = zip(entries,keys)
    
    return render_template('quiz_start.html',data=data, zipped = zd)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    # Get the submitted form data
    if request.method == "POST":
        #clear previous corrected answers
        if len(corrected_ans) > 0:
            corrected_ans.clear()
        
        form_data = request.form
        meta_ans = [[key,value] for  key, value in form_data.items()]
        
        user_ans = [x[1] for x in meta_ans]
        #compare user repsonses against correct answer, declare count var for correct answers
        if len(user_ans) == len(data):
            print('Alert:',user_ans)
            correct = 0
            for i in range(len(right_ans)):
                if user_ans[i] == right_ans[i]:
                    print(user_ans[i], right_ans[i])
                    correct += 1
                else:
                    corrected_ans.append((meta_ans[i][0],right_ans[i]))
            
            score = round((correct/len(user_ans))*100)
            return redirect(url_for('quiz_results', score=score))
        else:
            return redirect(url_for('start'))

@app.route('/quiz_results<int:score>')
def quiz_results(score):
    scr = str(score)
    # user needs score over 85 to pass quiz
    if score > 85:
        message = 'You have passed'
    else:
        message = 'Please try again. Score over 85 % to pass'

    return render_template('quiz_results.html', scr=scr, message=message, corrected_ans = corrected_ans)



if __name__ == '__main__':
    app.run(debug=True)
