from flask import Flask, render_template, request, send_file
from matplotlib import pyplot as plt
import io
app = Flask(__name__)
import matplotlib
matplotlib.use('Agg')

people = []

@app.route('/')
def main():
    global people
    return render_template("index.html", data={"people":people})

@app.route('/update', methods=["GET"])
def getInfo():
    global people 
    profit_array = (request.json["Profit"]).split(',')
    profit_float_array = [(float(i)) for i in profit_array]
    personExists = False
    for ppl in people:
        if ppl["Name"] == request.json["name"]:
            ppl["Profit"] = profit_float_array
            personExists = True
    if not personExists:
        person_obj = {
            "Name": request.json["name"],
            "URL": request.json["URL"],
            "Profit": profit_float_array
        }
        people.append(person_obj)

    # Generate and save the graph
    generate_graph()
    return "OK", 200

def generate_graph():
    global people
    time_periods = ["10 min ago", "9 min ago", "8 min ago", "7 min ago", "6 min ago", "5 min ago", "4 min ago", "3 min ago", "2 min ago", "1 min ago"]
    #plot points for each person
    plt.figure(figsize=(15, 6))  # Adjust the width and height as needed

    for i in range(len(people)):
        plt.plot(time_periods, people[i]["Profit"], marker = 'o', label=people[i]["Name"])
    plt.xlabel('Time elapsed')
    plt.ylabel('Profit')
    plt.title('Profits of PCTech nerds')
    plt.legend()
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    # Clear the plot to avoid memory leaks
    plt.clf()

    # Return the BytesIO object
    return img

@app.route('/graph')
def show_graph():
    img = generate_graph()
    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000, debug=False)
