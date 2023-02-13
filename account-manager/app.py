import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent # Outside
working_dir = pathlib.Path(__file__).resolve().parent.parent.parent #Bankof3v
project_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/global_config")
from flask import Flask, render_template
import sql

app = Flask(__name__)

@app.route('/')
def home():

    exchange = sql.balance("BINANCE")

    return render_template('index.html',exchange=exchange) 


if __name__ == "__main__":
    app.run(debug=True)