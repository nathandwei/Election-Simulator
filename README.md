# cs50-final-project
CS50 Final Project: Sam Huang and Nathan Wei on election simulations.

**Video** https://youtu.be/l4Mh64SKsds

**Link to project:** https://nathanwei.pythonanywhere.com/

![Alt text](static/ReadMe.png?raw=true)

## Access:
Simply enter https://nathanwei.pythonanywhere.com/ in your url to view our project.
No compilation, installation of files, or debugging is needed.

## Account Information:
**Account Registration:** Although an account is not required to run a simulation, if you would like to save your simulation, you must register an account. To register, click on the top right register button and enter a unique username and password. Confirm your password, then click register.
**Log-in** To log-in, simply click on the login button on the top right of the page and enter your username and password. Then, you should be logged in.
**Log-Out** Once you are logged in, you can log out at any time by clicking log out on the top right corner.

## How to set up your simulation

**Choosing Your Distribution:** We have 5 different distributions to choose from. Using the drop down menu, select your distribution and click on choose distribution button to confirm. The dynamic graph at the bottom should regenerate into the desired distribution. The distribution represents your voter base and their beliefs. For example, a uniform distribution means that there is an even distribution between the political right and left, while a bimodal distribution represents a polarized voter base.

**Adding/Removing Candidates:** At the bottom of the graph, there is a line that that contains your political candidates. Each dot represents one candidate. To add a new candidate, simply click on the line where you want their political stance to be. We will automatically create a color and name for your politician. If you would like to remove a candidate, simply click on the dot and it will be removed.

## Simulation Results:

**Popular Vote:** The first page after simulating is the popular votes page. Here, you will see a graph with all the candidates and the votes that they receieved. Outlined in gold is the candidate that receieved the popular vote. Click proceed to continue to ranked-choice voting.

**Ranked-Choice Voting:** The ranked-choice voting page will have a series of graphs that show the popular vote in each round. After every round, the candidate with the least amount of votes is eliminated, and the votes are allocated in the subsequent round. Once a candidate wins 50% or more of the popular vote, ranked-choice voting ends. If you see that there is only one round, check to make sure that someone has not already won! It is possible that someone has already taken 50% popular vote in the first round if there are not many total candidates or the distribution is skewed. Click proceed to continue to Tideman voting.

**Tideman:** Tideman, also known pair-wise voting, compares each candidate in a round-robin format and determines a winner based on which candidate wins the round-robin. In case of ties, it takes into account the amount of votes they won by. The graph shows each candidate as a node. If candidate A beat candidate B head to head, then there will be an arrow pointing from candidate A to candidate B. A golden circle will also appear around the candidate that has won the Tideman simulation. As a small easter-egg, the nodes in the graph are completely movable. Simply drag any node around to where ever you desire. If you have a lot of candidates and each node is small, you can zoom in by scrolling.

## Saving Your Simuation
**Saving:** Once you have finished viewing your simulation results, go to the bottom of the summary page. There will be an option to save your simulation. Note that you must first log-in before saving. If you have trobule finding where to login, view the account information section.
**Viewing Saved Simulations:** At the top left corner of the page, you can view saved simulations. The saved simulations will depict what type of distribution you choose and the candidates you created. Each candidate will have a value between -1 and 1. This corresponds with the bar at the bottom of the simulation page, where -1 is the left-most point in the bar and 1 is the right-most point in the bar.

## Easter-egg

**Brilliant Mode:** As an extra feature for logging in, there is a brilliant mode button on the top-left corner of the page. What it does? That's for you to find out!

## Known bug

**Duplicate Names:** Although it is very unlikely to happen, if two candidates receive the same generated name (out of 7000 names), the tideman graph will think they are the same candidate and will not be accurate (although it will not crash).