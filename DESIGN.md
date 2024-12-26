# cs50-final-project
CS50 Final Project: Sam Huang and Nathan Wei on election simulations.

**Link to project:** https://nathanwei.pythonanywhere.com/

![Alt text](static/ReadMe.png?raw=true)

## How It's Made:

**Tech used:** Python, Flask, HTML, CSS, JavaScript, JSON, Jinja.

We implemented our project by establishing a front-end design and back-end calculations, then connected the two through JSON parsing. To simulate data, app.py functions would invoke helper functions from the helper_functions folder: these are statistical functions that, among other things, implement nodes that represent candidates and perform calculations to simulate which candidate people will vote for given some distribution. Once app.py got this data, it would send it to HTML files (formatting into a JSON-like format if necessary), and the HTML pages would then use JSON.parse() to turn the data into JSON, and plug it into Javascript blocks that would manipulate the data into charts or graphs and display it on each HTML page.

## Frontend Website Development

**High-Level app.py Overview:** We used Flask to create this app because it is a lightweight Python module that does everything we want it to do, and we don't have advanced functionality that would require a different method: we also had more familiarity with Python than, say, React.js. All pages are displayed using Flask functions, usually one per page. At the top, we have Flask app configuration. Then, we have SQL classes implemented using the python modules SQLAlchemy and Flask-SQLAlchemy: each class represents a table, and each attribute of a class object corresponds to a field of a row in SQL. These tables are in app.py, rather than elsewhere, so they can easily be referred to, and also because Flask-SQLAlchemy ties the app itself to the database, and so that part needs to be done in app.py. Below that are helper functions, doing small things like verifying that the user has logged in or converting hex values to RGBA values so they can be better passed to certain HTML pages or modified more readily within code. Below that are the functions for each page.

**High-Level HTML/CSS/Javascript Overview:** Each HTML page is created using layout.html using Jinja, letting us not copy-paste everything over and over again. Jinja was also very helpful for displaying data we passed in from app.py. You'll notice that there's a lot of JSON.parse() functions being used: this is mostly in Javascript blocks. Code editors do not respond well to Jinja being used in Javascript sections, so wrapping inputs in a JSON.parse() function makes things easier. If we assign Javascript variables to these python data objects, they'll need to be valid JSON, so we used the tojson and safe filters to safely convert data to JSON: on the Python side, this means making sure all data makes sense to convert to JSON, hence why you'll see formatting in app.py using dictionaries and lists. Another notable fact is that there is no .js file, only inline Javascript: this was because in our page display, it made sense for the Javascript blocks to be where they are (rather than in some file), and allows a more cohesive visual of the code for each HTML file.

**Index Page:** For better design, we wanted to avoid scrolling as much as possible: if we could make a page short enough that the user wouldn't have to scroll, we would. Thus, instead of having a text list of each candidate, we decided to implement a grey bar below the distribution image with Javascript that held all the candidates: each candidate being represented as a small colored circle. This way, the user can instantly see the political stances of every candidate, without unnecessary text. Additionally, adding and deleting candidates with text fields and forms made the index page very cluttered (not to mention a bit ugly), so we instead implemented adding candidates by simply clicking on the grey bar to generate a candidate, and clicking on a candidate to delete it. This was to make candidate creation and deletion more intuitive, visually appealing, and convenient. 

The distribution "image" itself is not an image, it is a bar graph implemented with Chart.js, a Javascript framework for drawing graphs. Each bar is colored according to where it is on the political spectrum, a gradient slowly turning from blue to red: this allows the user to clearly see which side is which, and provides a prettier visual.

**Simulation Visuals:** Perhaps the most important part of the website is how the simulations are shown to the user. We have three different voting algorithms that are used per simulation: popular vote, ranked choice voting, and the Tideman voting algorithm. Each algorithm has a different page: popular.html, ranked.html, and tideman.html. Each are displayed in progression, in that order, when the user wants to move on. For example, the popular() function returns a redirect to the ranked.html page when the user wants to continue.

Popular vote was the most straightforward: it made sense to implement a bar graph that would show which candidates had more votes relative to the others. To this end, we utilized Chart.js. When creating these graphs, we took pains to ensure the best user experience: thus, each candidate has its own color to set them apart from the others, and a name, allowing for clearer visuals: these were styled using CSS. Additionally, each graph is animated by Chart.js as it appears on the screen, making for a flowier design. We made sure that the colors of candidates would not blend in with the default background to improve user experience, and added a gold highlight around the winner to enhance user experience further.

Ranked-Choice voting consists of multiple rounds, so instead of just having one bar graph, we decided to display one bar graph for each round in progression: the site first shows the graph for round 1, and you can continue clicking to get the next rounds. To this end, the ranked() function returns render_template() of ranked.html with different parameters: thus, the code of ranked.html can stay the same while displaying completely different rounds. To improve user experience, a button was added to simply skip to Tideman if they didn't want to view ranked-choice.

Tideman voting is completely different, and there's no good way to represent it with bar graphs. To this end, we used Cytoscape.js, a Javascript framework that can draw graph-theory-like structures. This perfectly suited our purpose to provide an intuitive visual of which candidates beat which other candidates. Our visual is a direct graph, and each candidate is visually represented as a node, pointing to anyone who beat it. The winner is again highlighted in gold using CSS to allow the user to easily see the winner.

At the end, there is a summary page: this might not seem necessary, but we decided it was good for the user to be able to see all the data from each type of algorithm on one page, so they can compare and contrast the different methods. We used HTML tables, with CSS to style them.

**Saving Simulations:** If a user really likes a certain simulation and thinks it will be useful, they can save the simulation, allowing them to see their old simulations anytime they want. Of course, the user must first be logged in to save a simulation, otherwise we couldn't associate a simulation with them. SQL is the perfect tool for this, so we used the SQLAlchemy and Flask-SQLAlchemy python modules to implement a SQLite database: Flask-SQLAlchemy better integrates SQLAlchemy with Flask by associating a Flask app to a specified SQL database. The structure of the tables is a one-to-many relationship from users to simulations, and a many-to-many relationship from simulations to candidates,: this is because each user has many simulations, and each simulation has many candidates, but users cannot share simulations, so the relationship from users to simulations is one-to-many. For logging in and registering, we used flask's werkzeug password hash function to store passwords in a secure manner, instead of using plaintext.

For the page where they can view their saved simulations, we believed that having each simulation in its own separate area would be much cleaner and easier on the eyes than raw text. Thus, each simulation is enclosed in it's own "card", with an image showing what type of distribution was used and what political stances each candidate had. 

**Miscellaneous Visuals:** The following were mostly implemented with plain CSS. For the default background, we aimed for a color that would contrast well with the distribution and simulation graphs, so we went with a light grey, a gentle color that's easy on the eyes and contrasts with the stronger colors of the candidates. We also added some waves at the bottom for a bit of stylistic flair. There is also a button at the top, the "Brilliant Mode" toggle that adds a CSS property called "brilliant" to the body HTML of any page, creating a multicolored animated background, because it seemed cool. 

For font, we wanted a sans-serif font that was easier on the eyes. However, many browsers cannot display some fonts. Trebuchet MS is considered more of a CSS-safe font, so it is widely browser compatible, which is why we used it.

**Other Development Details:** One thing that was very important to us when programming was adaptability. This is why popular.html and ranked.html are very similar: they both display a bar graph. The only difference is that the way the data is structured is slightly different, so they have to be different html pages, but the data fed into the pages are manipulated by Python beforehand, so any large changes to how the data is treated are isolated purely within app.py, and the display will adapt automatically. Another example of this philosophy is within app.py: many global constants are initialized at the top so that they can be readily used, and global variables are stored in the Flask session so that they can be easily used whenever needed. We also prefer to use session.get() instead of directly querying the session in case the field doesn't actually exist, for added security.

All input from the user is rigorously tested via server-side verification. Our lack of text fields and implementing candidate addition/deletion from clicking eliminates user inputs from almost the entire website, except for registration and login. If there are no candidates, the website knows what to do and won't return an error. All text fields are verified to make sure the inputs are sensible, and even inputs/variables that the user should not have direct access to are tested and guarded against: for example, we cover the possibility that the user has somehow input a simulation type that doesn't exist.

## Backend (Helper) Functions

**Sampling:** We wanted the user to be able to choose the political climate of their voters for the simulation, so we used NumPy, a data analysis library, to generate a unique distributions that our users can select. Each time an election a simulated, 1000 random points, scaled to between -1 and 1, is sampled from the distribution. Our goal imitate realistic voting where the votes are not guaranteed to be exactly the same each time, but follow a pattern based on the distribution.

**Voting Data Frame:** We fully implemented three voting methods: popular vote, ranked choice voting, and tideman. Each function returns a python dictionary with the candidate node as the key and the amount of votes they received. Each candidate has a 'political stance', from -1 to 1, stored in the data value of the node, and we assign each vote drawn randomly from the chosen distribution to the candidate that is closest to their political views. For ranked-choice voting and tideman, this is retabluated after each round or pair-wise respectively.

## Optimizations

**Custom Node:** Each one of our candidates needed to store several pieces of information such as their name, their political ideology, and their unique label color. Therefore, we decided to create a custom node that stored each of these values. Upon initialization, it would generate a random name and color, checking with previous nodes created before it to make sure that the name and color is unique.

**Linked List:** We wanted to give the user options to add and remove candidates, so we knew we needed to implement a data-structure that can add and remove candidates quickly. Because of this, we decided to use a doubly linked list to store our candidates. This allows for adding candidates in O(1) time and removing candidates in O(n) time because it doesn't matter where the node is in the memory as long as each node knows where the next node is located, making our program much more efficient than if we instead used the built-in python list data structure that would have to copy, shift, and replace each node if a node in the middle of the list is deleted.

## Hosting

**Python Anywhere:** We decided to host the website on Python Anywhere. After installing the requirements on a virtual environment, we were able to host our flask website on Python Anywhere. However, this was not without its troubles. The first time we hosted it, the website crashed almost instantly. After some time of debugging, we realized that our global variables needed to be stored into each session because Python Anywhere would run the code on multiple machines, and each machine would have a different value for the global variable, so even though the website worked perfectly in VSCode (where only one machine was running the code), it would crash on Python Anywhere. Thankfully, we found a workaround by implementing global variables into the session which can be accessed from every machine.