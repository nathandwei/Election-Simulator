# OS and Sys imports
import os
import sys

# Add helper_functions to PATH before importing dataframe_generator
sys.path.append(os.path.join(os.path.dirname(__file__), "helper_functions"))

# Module imports
from scipy.stats import norm, uniform, beta
from collections import OrderedDict
from math import sqrt
from datetime import datetime
from flask import Flask, flash, redirect, render_template, jsonify, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, exc
from sqlalchemy.orm import DeclarativeBase, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from helper_functions import data_frame, samples, data_structures

# Configure application
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///simulator.db"
db.init_app(app)

# Construct SQL Tables
class User(db.Model): # user id, username, and password hash
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(30), nullable=False, unique=True)
    hash = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, hash={self.hash!r})"

class SavedSimulation(db.Model): # simulation id, id of user who created it, distribution type
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    distribution_type = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"SavedSimulation(id={self.id!r}, user_id={self.user_id!r}, distribution_type={self.distribution_type!r})"

class SimulationCandidate(db.Model): # id of candidate, id of simulation it belongs to, name, political stance
    id = mapped_column(Integer, primary_key=True)
    simulation_id = mapped_column(ForeignKey("saved_simulation.id"))
    name = mapped_column(String, nullable=True)
    political_stance = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"SimulationCandidate(id={self.id!r}, simulation_id={self.simulation_id!r}, name={self.name!r}, political_stance={self.political_stance!r})"
    
with app.app_context():
    db.create_all() # Create the tables or update them

# Global variables
red = (252,70,107) # RGB
blue = (63,94,251)
type_to_dist = { # Converts distribution type to distribution sample data
    'normal': samples.normal(), 
    'bimodal': samples.two_peaks(), 
    'uniform': samples.uniform(), 
    'skewed_left': samples.skewed_left(), 
    'skewed_right': samples.skewed_right()
}

# Minor functions

# Takes in two RGB tuples and weight (0 to 1) of color 1, and outputs a weighted average in str format for Chart.js
def color_average(c1, c2, w):
    new_red = sqrt((c1[0]**2)*w + (c2[0]**2)*(1-w))
    new_green = sqrt((c1[1]**2)*w + (c2[1]**2)*(1-w))
    new_blue = sqrt((c1[2]**2)*w + (c2[2]**2)*(1-w))
    new_color = f"rgba({new_red},{new_green},{new_blue},1)"
    return new_color

# Converts a hex value parseable by HTML to an RGBA value parseable by HTML
def hex_to_rgb(hex_code, opacity):
    # Remove the '#' if it's there
    hex_code = hex_code.lstrip('#')
    # Convert the hex code to RGB
    build = "rgba"+str(tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)))
    build = build[:-1]+f", {str(opacity)})"
    return build

# Displays a screen showing an error message in case something goes wrong
def apology(message, code=400):
    """Render message as an apology to user."""

    return render_template("apology.html", error_message=message, error_code=code), code

# A decorator function verifying that the user has logged in
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# HTML page code
@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("candidate_list"): # If this is the first time entering the website
        politicians = data_structures.DoublyLinkedList()
        politicians.prepend(0.6)
        politicians.prepend(0.2)
        politicians.prepend(-0.2)
        politicians.prepend(-0.6)
        session["candidate_list"] = politicians
    
    numbers = [i for i in range(101)]
    bar_colors = [color_average(red,blue,value/100) for value in range(101)] # Sets up bar colors for distribution visuals
    candidate_list = session["candidate_list"]
    circle_colors = [tuple((candidate.data, candidate.color)) for candidate in candidate_list] # Sets up circle colors for candidate visuals
    session["ranked_visited"] = False # If the user is at index.html, they have not entered the ranked.html page for a new simulation yet
    if not session.get("distribution_type"): # If no distribution type chosen, set it to normal
        session["distribution_type"] = 'normal'
    distribution_type = session["distribution_type"]

    type_to_numbers = { # Convert type of distribution to numbers for display on index.html distribution graph
        'normal': [norm(0,1).pdf(7*i/100) for i in range(-50,51)],
        'bimodal': [(0.5)*(norm(2,1).pdf(7*i/100)+norm(-2,1).pdf(7*i/100)) for i in range(-50,51)],
        'uniform': [uniform(-1,1).pdf(i/100) for i in range(-101,0)],
        'skewed_left': [beta(2,4).pdf(i/100) for i in range(101)],
        'skewed_right': [beta(4,2).pdf(i/100) for i in range(101)]
    }

    distribution_order = {} # Decides what order the dropdown menu from the Choose Distribution button is, starting with the one already chosen
    distribution_order[distribution_type] = distribution_type.replace("_"," ").title()
    for i in type_to_numbers.keys():
        if i != distribution_type:
            distribution_order[i] = i.replace("_"," ").title() # Formats the text

    if request.method == "GET":
        distribution_numbers = type_to_numbers[session["distribution_type"]] # Default is normal       
        return render_template(
            "index.html",
            numbers=numbers,
            distribution_numbers=distribution_numbers,
            bar_colors=bar_colors,
            distribution_type=session["distribution_type"],
            candidate_list=candidate_list,
            circle_colors=circle_colors,
            distribution_order=distribution_order
        )
    
    if request.form.get("action") == "run_simulation":
        return redirect("/popular")
    elif request.form.get("action") == "choose_distribution": 
        distribution_type = request.form.get("distribution_type")
        valid_types = ['normal','bimodal','uniform','skewed_left','skewed_right']
        if distribution_type not in valid_types: # Make sure the type is valid
            return apology("Invalid distribution type.", 403)
        else:
            session["distribution_type"] = distribution_type # Set session variables
            distribution_numbers = type_to_numbers[distribution_type]
            session["distribution_numbers"] = distribution_numbers # Distribution numbers for display on page

        circle_colors = [tuple((candidate.data, candidate.color)) for candidate in candidate_list] # Colors of candidates

        distribution_order = {} # This code MUST be repeated for this action specifically since distribution changes
        distribution_order[distribution_type] = distribution_type.replace("_"," ").title()
        for i in type_to_numbers.keys():
            if i != distribution_type:
                distribution_order[i] = i.replace("_"," ").title()

        return render_template(
            "index.html",
            numbers=numbers,
            distribution_numbers=distribution_numbers,
            bar_colors=bar_colors,
            distribution_type=distribution_type,
            candidate_list=candidate_list,
            circle_colors=circle_colors,
            distribution_order=distribution_order
        )
    elif request.form.get("action") == "add_candidate":
        if not request.form.get("candidate_stance"): # Verify that the candidate stance is valid, if user accesses hidden inputs not displayed
            return apology("Must input a candidate stance.", 403)
        candidate_stance = request.form.get("candidate_stance")

        try:
            candidate_stance = float(candidate_stance)
        except ValueError:
            return apology("Candidate stance must be a number.", 403)
        if 1 < candidate_stance or -1 > candidate_stance:
            return apology("Candidate stance must be between 1 and -1.")
        
        data_frame.add_candidate(candidate_stance, session["candidate_list"]) # Add the candidate

        distribution_type = session.get("distribution_type")
        distribution_numbers = session.get("distribution_numbers")
        if not distribution_type: # Set defaults
            distribution_type = 'normal'
        if not distribution_numbers:
            distribution_numbers = [norm(0,1).pdf(7*i/100) for i in range(-50,51)]

        circle_colors = [tuple((candidate.data, candidate.color)) for candidate in candidate_list]

        return render_template(
            "index.html",
            numbers=numbers,
            distribution_numbers=distribution_numbers,
            bar_colors=bar_colors,
            distribution_type=distribution_type,
            candidate_list=candidate_list,
            circle_colors=circle_colors,
            distribution_order=distribution_order
        )
    elif request.form.get("action") == "delete_candidates":
        if not request.form.getlist("delete_marked"): # Delete all candidates marked for deletion, list in case multiple (future feature)
            return apology("Must check off candidates to delete.", 403)
        
        delete_marked = request.form.getlist("delete_marked")
        for candidate in delete_marked:
            data_frame.remove_candidate(float(candidate), session["candidate_list"])
        
        distribution_type = session.get("distribution_type")
        distribution_numbers = session.get("distribution_numbers")
        if not distribution_type:
            distribution_type = 'normal'
        if not distribution_numbers:
            distribution_numbers = [norm(0,1).pdf(7*i/100) for i in range(-50,51)]

        circle_colors = [tuple((candidate.data, candidate.color)) for candidate in candidate_list]
        
        return render_template(
            "index.html",
            numbers=numbers,
            distribution_numbers=distribution_numbers,
            bar_colors=bar_colors,
            distribution_type=distribution_type,
            candidate_list=candidate_list,
            circle_colors=circle_colors,
            distribution_order=distribution_order
        )
    else:
        return apology("Invalid action.", 403)


@app.route("/popular", methods=["GET", "POST"])
def popular():
    if request.method == "GET":
        distribution_type = session.get("distribution_type")
        if not distribution_type: # Set default
            distribution_type = 'normal'
        distribution = type_to_dist[distribution_type]

        try:
            candidate_dict = OrderedDict(sorted(data_frame.popular_vote(distribution, session["candidate_list"]).items(), key=lambda x: x[0].data)) # Create ordered dict by stance
        except ValueError:
            return apology("Must have at least one candidate.", 403) # Verify there is at least one candidate
        
        session["popular"] = candidate_dict
        max_num = -1
        winner = "NOT AVAILABLE"
        for candidate in candidate_dict: # Algorithm to detect the winner (most votes)
            if candidate_dict[candidate] > max_num:
                max_num = candidate_dict[candidate]
                winner = candidate.name
        candidates = [x.name for x in list(candidate_dict.keys())] # I can't just use candidate_dict dictionary as Jinja does not allow for list() in HTML
        vote_numbers = list(candidate_dict.values())
        bar_colors = [str(x.color) for x in list(candidate_dict.keys())] # Bar colors are colors of the nodes
        bar_outlines = []
        for candidate,color in zip(list(candidate_dict.keys()),bar_colors):
            if candidate.name == winner:
                bar_outlines.append('rgba(255, 215, 0, 1)') # HTML RGB color for gold, outline winner in gold
            else:
                bar_outlines.append(hex_to_rgb(color,0.5)) # Outline non-winners in lighter version of bar color
        return render_template( 
            "popular.html",
            candidates=candidates, 
            vote_numbers=vote_numbers,
            bar_colors=bar_colors,
            bar_outlines=bar_outlines,
        )
    
    return redirect("/ranked")

@app.route("/ranked", methods=["GET", "POST"])
def ranked():
    if not session.get("ranked_visited"): # If ranked.html has not been visited before for this simulation
        session["ranked_round"] = 0
        session["ranked_visited"] = True

        distribution_type = session.get("distribution_type")
        if not distribution_type:
            distribution_type = 'normal'
        distribution = type_to_dist[distribution_type]
        candidate_round_list = data_frame.ranked_choice_voting(distribution, session["candidate_list"]) # Generate the ranked choice voting results from distribution

        session["ranked"] = candidate_round_list # Save data for ranked choice voting
    else:
        candidate_round_list = session["ranked"] # Get the data from before
    num_rounds = len(candidate_round_list)

    if request.method == "GET":
        round = 0 # Get method implies it's the first round, 0-indexed here but adds 1 in ranked.html for display
        candidate_dict = OrderedDict(sorted(candidate_round_list[round]['vote_counts'].items(), key=lambda x: x[0].data)) # Dict of votes for each cand each round
        candidates = [x.name for x in list(candidate_dict.keys())]
        vote_numbers = list(candidate_dict.values())
        bar_colors = [str(x.color) for x in list(candidate_dict.keys())]
        max_num = -1
        winner = "NOT AVAILABLE"
        for candidate in candidate_dict: # Algorithm to detect the winner (most votes)
            if candidate_dict[candidate] > max_num:
                max_num = candidate_dict[candidate]
                winner = candidate.name
        bar_outlines = []
        for candidate,color in zip(list(candidate_dict.keys()),bar_colors):
            if candidate.name == winner:
                bar_outlines.append('rgba(255, 215, 0, 1)') # HTML RGB color for gold, outline winner in gold
            else:
                bar_outlines.append(hex_to_rgb(color,0.5)) # Outline non-winners in lighter version of bar color

        return render_template(
            "ranked.html",
            candidates=candidates,
            vote_numbers=vote_numbers,
            bar_colors=bar_colors,
            round=round,
            bar_outlines=bar_outlines,
        )

    valid_actions = ["proceed", "next_round"]
    if request.form.get("action") not in valid_actions:
        return apology("Invalid action.", 403)
    elif request.form.get("action") == "proceed":
        return redirect("/tideman")
    elif request.form.get("action") == "next_round":
        if session["ranked_round"] == num_rounds-1: # Increase the number of rounds mod total number of rounds
            session["ranked_round"] = 0
        else:
            session["ranked_round"] += 1
        round = session["ranked_round"] # Get round from session data
        candidate_dict = OrderedDict(sorted(candidate_round_list[round]['vote_counts'].items(), key=lambda x: x[0].data)) # Dict of votes for each cand each round
        candidates = [x.name for x in list(candidate_dict.keys())]
        vote_numbers = list(candidate_dict.values())
        bar_colors = [str(x.color) for x in list(candidate_dict.keys())]
        max_num = -1
        winner = "NOT AVAILABLE"
        for candidate in candidate_dict: # Algorithm to find the winner (most votes)
            if candidate_dict[candidate] > max_num:
                max_num = candidate_dict[candidate]
                winner = candidate.name
        bar_outlines = []
        for candidate,color in zip(list(candidate_dict.keys()),bar_colors):
            if candidate.name == winner:
                bar_outlines.append('rgba(255, 215, 0, 1)') # HTML RGB color for gold, outline winner in gold
            else:
                bar_outlines.append(hex_to_rgb(color,0.5)) # Outline non-winners in lighter version of bar color
        return render_template(
            "ranked.html",
            candidates=candidates,
            vote_numbers=vote_numbers,
            bar_colors=bar_colors,
            round=session["ranked_round"],
            bar_outlines=bar_outlines,
        )


@app.route("/tideman", methods=["GET", "POST"])
def tideman():
    if request.method == "GET":
        distribution_type = session.get("distribution_type")
        if not distribution_type:
            distribution_type = 'normal'
        distribution = type_to_dist[distribution_type] # Generate the distribution
        candidate_win_dict = data_frame.ranked_pairs_voting(distribution, session["candidate_list"]) # Generate the dictionary of candidates and wins

        session["tideman"] = candidate_win_dict # Save data for Tideman voting
    
        candidate_dict = OrderedDict(sorted(candidate_win_dict[0].items(), key=lambda x: x[0].data))
        candidates = [x.name for x in list(candidate_dict.keys())]
        node_list = []
        edge_list = []
        style_list = []
        num_candidates = 0
        winner = "TIE"

        style_list.append({ # Append generic style for each node in JSON-like format
            'selector': 'node',
            'style': {
                'label': 'data(id)',
                'border-color': '#000',
                'border-width': 3,
                'border-opacity': 0.5
            },
        })
        style_list.append({ # Apply generic style for each edge in JSON-like format
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'width': 3,
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle'
            }
        })

        for candidate in candidate_dict.keys():
            cand_dict = {"data": {"id": candidate.name}} 
            node_list.append(cand_dict) # Append node to list of nodes in Cytoscape.js
            style_list.append({"selector": "#"+candidate.name, "style": {"background-color": str(candidate.color)}}) # Append node-specific style
            num_candidates += 1
        for candidate in candidate_win_dict[0].keys():
            for win in candidate_win_dict[0][candidate]: # Determine who has the most wins as the winner
                win_dict = {"data": {"source": win.name, "target": candidate.name}} 
                edge_list.append(win_dict) # Append edge to list of nodes in Cytoscape.js
            if len(candidate_win_dict[0][candidate]) == num_candidates-1:
                winner = candidate.name # Algorithm for detecting who has the max wins

        style_list.append({ # Apply special style to the winner
            'selector': f'#{winner}',
            'style': {
                'border-color': 'gold'
            }
        })
        
        return render_template(
            "tideman.html",
            candidates=candidates,
            candidate_win_dict=candidate_win_dict,
            node_list=node_list,
            edge_list=edge_list,
            style_list=style_list,
            winner=winner
        )
    
    return redirect("/summary")

@app.route("/summary", methods=["GET", "POST"])
def summary(): 
    if request.method == "GET":
        popular_dict = session["popular"] # Get all data from all simulations
        ranked_dict_list = session["ranked"]
        tideman_win_dict = session["tideman"][0]
        return render_template(
            "summary.html",
            candidate_dict=popular_dict,
            ranked_dict_list=ranked_dict_list,
            tideman_win_dict=tideman_win_dict,
            saved=False
        )
    
    if request.form.get("action") == "homepage":
        return redirect("/")
    elif request.form.get("action") != "save":
        return apology("403: Invalid form submission.", 403)
    else:
        return redirect("/save")
'''
@app.route("/save", methods=["GET", "POST"])
@login_required
def save():
    if request.method == "GET":
        candidate_dict = session["popular"] # Get all data from all simulations
        ranked_dict_list = session["ranked"]
        tideman_win_dict = session["tideman"][0]
        distribution_type = session.get('distribution_type')
        if not distribution_type:
            distribution_type = 'normal' # Normal is default
        
        simulation_params = SavedSimulation( # Create simulation object, which is linked to SQL database
            user_id = session["user_id"],
            distribution_type = session["distribution_type"]
        )
        db.session.add(simulation_params)
        db.session.commit() # Add simulation to database
        for candidate in candidate_dict.keys():
            sim_cand = SimulationCandidate(
                simulation_id = simulation_params.id, 
                name = candidate.name,
                political_stance = candidate.data
            )
            db.session.add(sim_cand)
            db.session.commit() # Add candidate to database
        
        return render_template(
            "summary.html",
            candidate_dict=candidate_dict,
            ranked_dict_list=ranked_dict_list,
            tideman_win_dict=tideman_win_dict,
            saved=True
        )
    
    return redirect("/")
'''
'''
@app.route("/simulations")
@login_required
def simulations():
    if request.method == "GET":
        user_simulations = db.session.execute(db.select(SavedSimulation).filter_by(user_id=session["user_id"])).scalars() # Find all saved simulations from this user
        simulation_dict = {}
        for simulation in user_simulations:
            simulation_candidates = db.session.execute(db.select(SimulationCandidate).filter_by(simulation_id=simulation.id)).scalars() # Find candidates of simulations
            simulation_dict[simulation] = [candidate for candidate in simulation_candidates]

        cards = [] # List of HTML cards for each simulation
        dist_to_img = { # Decides what image to display
            'normal': '/static/normal.png', 
            'bimodal': '/static/bimodal.png', 
            'uniform': '/static/uniform.png', 
            'skewed_left': '/static/skewed_left.png', 
            'skewed_right': '/static/skewed_right.png'
        }
        for simulation, candidate_list in simulation_dict.items(): # Creates HTML code to be executed in a .innerHTML() function for each card
            card_content = ""
            for candidate in candidate_list: # For each candidate create HTML code to display name and political stance
                if not candidate.name:
                    candidate.name = "Nameless"
                card_content += f"{candidate.name}<br> Political Stance: {candidate.political_stance}<br>"
            card_content = f"<img src='{dist_to_img[simulation.distribution_type]}' alt='{simulation.distribution_type}'><br>"+card_content # Adds image to HTML code
            cards.append({"title": simulation.distribution_type.replace("_"," ").title(), "content": card_content}) # Formats title of card

        return render_template("simulations.html", simulation_dict=simulation_dict, cards=cards)
'''
'''
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
'''

'''
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username.", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password.", 403)
        
        username = request.form.get("username")

        # Query database for username
        try:
            user_extraction = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
        except:
            return apology("Invalid username and/or password.", 403)

        # Ensure username exists and password is correct
        if not check_password_hash(
            user_extraction.hash, request.form.get("password")
        ):
            return apology("Invalid password and/or password.", 403)

        # Remember which user has logged in
        session["user_id"] = user_extraction.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
'''

'''
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user ID
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    # Verify that the user inputted a username, password, and confirmation
    if not request.form.get("username"):
        return apology("Must provide username.", 400)
    elif not request.form.get("password"):
        return apology("Must provide password.", 400)
    elif not request.form.get("confirmation"):
        return apology("Must confirm password.", 400)

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # Verify that the password and confirmation match
    if password != confirmation:
        return apology("Password and confirmation do not match.", 400)

    password_hash = generate_password_hash(password)

    # Verify that the username is not a duplicate
    try:
        user = User(
            username = request.form.get("username"),
            hash = password_hash
        )
        db.session.add(user)
        db.session.commit()
    except (exc.IntegrityError, exc.MultipleResultsFound):
        db.session.rollback()
        return apology("That username already exists, please try another.", 400)

    # Set the session id to the new registered id
    user_extraction = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
    session["user_id"] = user_extraction.id

    return redirect("/")
'''

def main():
    app.run()

if __name__ == "__main__":
    main()