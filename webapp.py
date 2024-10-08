from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    states = get_states()
    #print(states)
    return render_template('home.html', states=states)

@app.route('/showFact')
def render_fact():
    states = get_states()
    state = request.args.get('state')
    county = county_most_under_18(state)
    county2 = county_most_women(state)
    fact = "In " + state + ", the county with the highest percentage of under 18 year olds is " + county + "."
    fact2 = "In " + state + ", the county with the highest percentage of women is " + county2 + "."
    fact3 = request.args.get('fact3')
    if fact3 == None:
        fact3 = ""
    return render_template('home.html', states=states, funFact=fact, funFact2=fact2, funFact3=fact3)
    
@app.route('/secondFact')
def render_second_fact():
    states = get_states()
    state = request.args.get('state2')
    lowest_bachelors = county_lowest_bachelors(state)
    county = lowest_bachelors[0]
    percent = lowest_bachelors[1]
    fact = request.args.get('fact')
    fact2 = request.args.get('fact2')
    
    if percent is not None:
        fact3 = "In " + state + ", the county with the lowest percentage of people with a bachelor's degree or higher is " + county + ", with only " + str(percent) + " percent of people having a bachelor's degree or higher."
    else:
        fact3 = ""
    
    return render_template('home.html', states=states, funFact=fact, funFact2=fact2, funFact3=fact3)
    
def get_states():
    """Return a list of state abbreviations from the demographic data."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    #states=[]
    #for c in counties:
        #if c["State"] not in states:
            #states.append(c["State"])
    #a more concise but less flexible and less easy to read version is below.
    states=list(set([c["State"] for c in counties])) #sets do not allow duplicates and the set function is optimized for removing duplicates
    return states

def county_most_under_18(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county

def county_most_women(state):
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Miscellaneous"]["Percent Female"] > highest:
                highest = c["Miscellaneous"]["Percent Female"]
                county = c["County"]
    return county
    
def county_lowest_bachelors(state):
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    lowest=100
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Education"]["Bachelor's Degree or Higher"] < lowest:
                lowest = c["Education"]["Bachelor's Degree or Higher"]
                county = c["County"]
    result = [county, lowest]
    return result

def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
