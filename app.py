from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Configure your Foodvisor API credentials
FOODVISOR_API_KEY = "Dm5UlDdl.K3fau5U3IoCOyjRtVffhPzjeLWwfkQ3A"
FOODVISOR_API_URL = "https://vision.foodvisor.io/api/1.0/en/analysis/"

# Configure the upload folder
UPLOAD_FOLDER = "/Users/srinivasib/Developer/ai-calorie-calculator/static"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)
    
    file = request.files["file"]
    
    if file.filename == "":
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        
        # Prepare the request to Foodvisor API
        headers = {"Authorization": f"Api-Key {FOODVISOR_API_KEY}"}
        files = {"image": (file.filename, open(file_path, "rb"), "image/jpg")}
        
        # response = requests.post(FOODVISOR_API_URL, headers=headers, files=files, data=data)
        response = requests.post(FOODVISOR_API_URL, headers=headers, files=files)
        data = response.json()

        # Display the Foodvisor API response on the website
        return render_template(
            "index.html", 
            calories=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["calories_100g"], 2), 
            serving_size=round(data["items"][0]['food'][0]["food_info"]["g_per_serving"], 2),
            total_fat=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["fat_100g"], 2),
            sat_fat=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["sat_fat_100g"], 2),
            protein=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["proteins_100g"], 2),
            sodium=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["sodium_100g"], 2),
            potassium=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["potassium_100g"], 2),
            cholesterol=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["cholesterol_100g"], 2),
            carbs=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["carbs_100g"], 2),
            fiber=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["fibers_100g"], 2),
            sugar=round(data["items"][0]['food'][0]["food_info"]["nutrition"]["sugars_100g"], 2),
            image_url=file.filename,
            food=data["items"][0]['food'][0]["food_info"]["display_name"],
                               )
    
    return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)
