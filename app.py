from flask import Flask,url_for,redirect,render_template,request
import pickle
import numpy as np
import pandas as pd
app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

model = pickle.load(open('model.pkl', 'rb'))
lambda_dict = pickle.load(open('lamda_values.pkl', 'rb'))

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        
        length_of_service = float(request.form['length_of_service'])
        avg_training_score = float(request.form['avg_training_score'])
        Age = float(request.form['Age'])
        department = str(request.form['department'])
        education = str(request.form['education'])
        gender = str(request.form['gender'])
        recruitment_channel = str(request.form['recruitment_channel'])
        KPIs_met  = str(request.form['KPIs_met >80%'])
        awards_won = str(request.form['awards_won?'])
        previous_year_rating = int(request.form['previous_year_rating'])
        no_of_trainings = str(request.form['no_of_trainings'])

        ## Feature Engineering
        length_of_service = (length_of_service**lambda_dict['length_of_service'] - 1)/lambda_dict['length_of_service']
        avg_training_score = (avg_training_score**lambda_dict['avg_training_score'] - 1)/lambda_dict['avg_training_score']
        Age = (Age**lambda_dict['age'] - 1)/lambda_dict['age']

        ## Department Feature

        department_list = ['Finance', 'HR', 'Legal','Operations','Procurement', 'R&D', 'Sales & Marketing','Technology']
        variable_list_department = []
        for i in department_list:

            if department==i:
                variable = 'department' + '_' + str(i)
                globals()[variable] = 1
                variable_list_department.append(globals()[variable])
            else:
                variable = 'department' + '_' + str(i)
                globals()[variable] = 0
                variable_list_department.append(globals()[variable])

        ## Education Feature

        education_list = ['Below Secondary', "Master's & above"]
        variable_list_education = []
        for i in education_list:

            if education ==i:
                variable = 'education' + '_' + str(i)
                globals()[variable] = 1
                variable_list_education.append(globals()[variable])
            else:
                variable = 'education' + '_' + str(i)
                globals()[variable] = 0
                variable_list_education.append(globals()[variable])
        
        ## Gender Feature

        if gender=='Male':
            gender_m = 1
        else:
            gender_m = 0

        if awards_won == 'Yes':
            awards_won = 1
        else:
            awards_won = 0

        if KPIs_met == 'Yes':
            KPIs_met = 1
        else:
            KPIs_met = 0

        recruitment_channel_list = ['referred', 'sourcing']
        variable_list_recruitment_channel = []
        for i in recruitment_channel_list:

            if recruitment_channel ==i:
                variable = 'recruitment_channel' + '_' + str(i)
                globals()[variable] = 1
                variable_list_recruitment_channel.append(globals()[variable])
            else:
                variable = 'recruitment_channel' + '_' + str(i)
                globals()[variable] = 0
                variable_list_recruitment_channel.append(globals()[variable])
        

        no_of_trainings_list = ['2', '3','4','more_trainings']
        variable_list_no_of_trainings = []
        for i in no_of_trainings_list:

            if no_of_trainings ==i:
                variable = 'no_of_trainings' + '_' + str(i)
                globals()[variable] = 1
                variable_list_no_of_trainings.append(globals()[variable])
            else:
                variable = 'no_of_trainings' + '_' + str(i)
                globals()[variable] = 0
                variable_list_no_of_trainings.append(globals()[variable])

        list_of_features = [Age,previous_year_rating,length_of_service,KPIs_met,awards_won,avg_training_score] + variable_list_department + variable_list_education + [gender_m] + variable_list_recruitment_channel + variable_list_no_of_trainings
        
        prediction = model.predict(np.array([list_of_features]))

        if prediction==1:
            prediction_text = 'Congratulations!! You will get a promotion'
            return render_template('index.html', prediction_text=prediction_text)
        else :
            prediction_text = 'Oops!! You will not get a promotion'
            return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)