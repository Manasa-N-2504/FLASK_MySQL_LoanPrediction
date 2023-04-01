from flask import Flask, request, render_template
import pickle
import mysql.connector as sql
from model import rfc
app = Flask(__name__)

with open ('model.pkl','rb') as f:
	model = pickle.load(f)
				
@app.route("/")
def main():
    return render_template("login.html")

@app.route("/login", methods=['Post','Get'])
def login():
    global cursor
    mycon = sql.connect(host = "localhost", user = "root", passwd = "manasa", database = "cia")
    cursor = mycon.cursor()
    login_username = request.form.get("username")
    login_password = request.form.get("password")
    cursor.execute("select * from login")
    data = cursor.fetchall()
    username_list=[]
    password_list=[]

    for i in data:
        username_list.append(i[0])
        password_list.append(i[1])

    print(username_list)
    print(login_username)
    if login_username not in username_list:
        return render_template("login.html",info='Invalid Username. Username does not exist.Please try again')
    else:
        if login_password not in password_list:
            return render_template("login.html",info='Incorrect Password. Please try again')
        else:
            return render_template("predict.html")
			
@app.route("/prediction",methods=['Post'])
def prediction():
	Applicant_Income=request.form.get("Applicant_Income")
	Coapplicant_Income=request.form.get("Coapplicant_Income")
	Loan_Amount=request.form.get("Loan_Amount")
	Term=request.form.get("Term")
	Credit_History=request.form.get("Credit_History")
	Gender=request.form["Gender"]
	Married=request.form["Married"]
	Education=request.form["Education"]
	Self_Employed=request.form["Self_Employed"]
    
	print(Applicant_Income,Coapplicant_Income,Loan_Amount,Term,Credit_History,Gender,Married,Education,Self_Employed)
    
	if Gender=='female':
		Gender1=1
	else:
		Gender1=0
        
	if Married=='yes':
		Married1=1
	else: 
		Married1=0
        
	if Education=='yes':
		Education1=1
	else: 
		Education1=0
        
	if Self_Employed=='yes':
		Self_Employed1=1
	else: 
		Self_Employed1=0
        
	loan_pred=rfc.predict( [[int(Applicant_Income),int(Coapplicant_Income),int(Loan_Amount),int(Term),int(Credit_History),Gender1, Married1,Education1,Self_Employed1]] )
    
	if loan_pred[0]==1:
		res = "LOAN CAN BE SANCTIONED"
	else:
		res = "LOAN CAN NOT BE SANCTIONED"

	return render_template("success.html",input1=Applicant_Income,input2=Coapplicant_Income,input3=Loan_Amount,input4=Term,input5=Credit_History,input6=Gender,input7=Married,input8=Education,input9=Self_Employed,result=res)
    

@app.route("/logout")
def logout():
	return render_template("login.html")

if __name__ == "__main__":
	app.run(host='localhost', port = 5000)





    
        
    	