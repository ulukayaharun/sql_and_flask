from flask import Flask,request,render_template
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import urlparse

app =Flask(__name__)
app.secret_key="verystrongpassword"

def get_domain(url):
    #cut all url to main domain part (www.example.com)
    parsed_url = urlparse(url)
    return parsed_url.netloc

def update_df():
    #get start and end date from user 
    start_date=request.form.get("start_date")
    end_date=request.form.get("end_date")

    if start_date and end_date:
        #read table and reach data
        engine = create_engine("mysql+pymysql://username:password@address/database_name", connect_args={"charset": "utf8mb4"}, echo=False)
        df=pd.read_sql_table("table_name",engine)
        #filter dataframe between start and end date
        filtered_df = df[(df['DATETIME'] >= start_date) & (df['DATETIME'] <= end_date)]

        #count how many news in data
        data={}
        for _,row in filtered_df.iterrows():
            domain=get_domain(row["URL"])
            if domain in data:
                data[domain]+=1
            else:
                data[domain]=1

        new_df = pd.DataFrame(list(data.items()), columns=['Domain', 'News Numbers'])
    return  new_df.to_html(index=False)

@app.route("/",methods=["GET","POST"])
def index():
    #update table when press "Make Table" button 
    table_html=update_df() if request.method == "POST" else ""
    return render_template("index.html",table_html=table_html)


if __name__=="__main__":
    app.run(debug=True)