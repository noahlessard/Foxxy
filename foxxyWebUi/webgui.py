from flask import Flask, render_template, request
import datetime
import time
import os
import torch
from transformers import CodeGenTokenizer
from transformers import AutoModelForCausalLM
import accelerate

print("set init status of model")
model = None
modelName = "N\A"
maxtokens = 100
tokenizer = CodeGenTokenizer.from_pretrained("models/6B")
textarea = "input python code here"

def standInFunction(stringy):
    time.sleep(2)
    print(stringy)
    return stringy

def checkModel():
    if model is None:
        return False
    return True

def loadModel(nameOfModel):
    global model
    print("loading model...")

    model = AutoModelForCausalLM.from_pretrained(
        nameOfModel, device_map="auto",
        offload_folder="offload",
        offload_state_dict = True, torch_dtype=torch.float16
    )

    print("done!")
    

def fowardPass(text):
    global tokenizer
    global model 
    global maxtokens

    completion = model.generate(**tokenizer(text, return_tensors="pt").to("cuda"), max_new_tokens=maxtokens)
    return (tokenizer.decode(completion[0]))


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    global model
    global modelName
    global textarea
    global maxtokens

    content = "Generated Code will appear here"
    
    if request.method == "POST":

        if request.form.get('loadbutton') == 'Load':
            match request.form.get('selection'):
                case '350M':
                    del model
                    torch.cuda.empty_cache()
                    loadModel("models/350M")
                    modelName = "350M"
                case '2B':
                    del model
                    torch.cuda.empty_cache()
                    loadModel("models/2B")
                    modelName = "2B"
                case '6B':
                    del model
                    torch.cuda.empty_cache()
                    loadModel("models/6B")
                    modelName = "6B"


        if request.form.get('submitbutton') == 'Submit':
            maxtokens = int(request.form["max tokens"])
            if(checkModel()):
                prompt = request.form["input python"]
                textarea = prompt
                print("starting generation...")
                content = fowardPass(prompt)
                print(content)
                print("done!")
            else:
                print("NO MODEL IS LOADED!")
    


    return render_template("index.html", text_area_text=textarea, output_text=content, model_status=checkModel(), model_name = modelName, max_tokens=maxtokens)
    
if __name__ == "__main__":
    app.run()
