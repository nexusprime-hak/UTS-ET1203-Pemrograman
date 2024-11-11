from flask import Flask, render_template
from satellite_parser import parse_satellite_data  # Import your function here

app = Flask(__name__)

@app.route('/')
def home():
    norad_n2yo = parse_satellite_data()
    # Additional fixed values for other variables
    size_n2yo = 'large'
    allpasses_n2yo = '0'
    map_n2yo = '5'
    
    return render_template('landing_page.html', 
                           norad_n2yo=norad_n2yo, 
                           size_n2yo=size_n2yo,
                           allpasses_n2yo=allpasses_n2yo,
                           map_n2yo=map_n2yo)

if __name__ == '__main__':
    app.run(debug=True)
