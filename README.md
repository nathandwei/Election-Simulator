# Election Simulation Project
Sam Huang and Nathan Wei on election simulations.

**Link to project:** https://nathanwei.pythonanywhere.com/

![Alt text](static/ReadMe.png?raw=true)

## Access:
Simply enter https://nathanwei.pythonanywhere.com/ in your url to view our project.
No compilation, installation of files, or debugging is needed.

## How to set up your simulation

**Choosing Your Distribution:** We have 5 different distributions to choose from. Using the drop down menu, select your distribution and click on choose distribution button to confirm. The dynamic graph at the bottom should regenerate into the desired distribution. The distribution represents your voter base and their beliefs. For example, a uniform distribution means that there is an even distribution between the political right and left, while a bimodal distribution represents a polarized voter base.

**Adding/Removing Candidates:** At the bottom of the graph, there is a line that that contains your political candidates. Each dot represents one candidate. To add a new candidate, simply click on the line where you want their political stance to be. We will automatically create a color and name for your politician. If you would like to remove a candidate, simply click on the dot and it will be removed.

## Simulation Results:

**Popular Vote:** The first page after simulating is the popular votes page. Here, you will see a graph with all the candidates and the votes that they receieved. Outlined in gold is the candidate that receieved the popular vote. Click proceed to continue to ranked-choice voting.

**Ranked-Choice Voting:** The ranked-choice voting page will have a series of graphs that show the popular vote in each round. After every round, the candidate with the least amount of votes is eliminated, and the votes are allocated in the subsequent round. Once a candidate wins 50% or more of the popular vote, ranked-choice voting ends. If you see that there is only one round, check to make sure that someone has not already won! It is possible that someone has already taken 50% popular vote in the first round if there are not many total candidates or the distribution is skewed. Click proceed to continue to Tideman voting.

**Tideman:** Tideman, also known pair-wise voting, compares each candidate in a round-robin format and determines a winner based on which candidate wins the round-robin. In case of ties, it takes into account the amount of votes they won by. The graph shows each candidate as a node. If candidate A beat candidate B head to head, then there will be an arrow pointing from candidate A to candidate B. A golden circle will also appear around the candidate that has won the Tideman simulation. As a small easter-egg, the nodes in the graph are completely movable. Simply drag any node around to where ever you desire. If you have a lot of candidates and each node is small, you can zoom in by scrolling.

## Known bug

**Duplicate Names:** Although it is very unlikely to happen, if two candidates receive the same generated name (out of 7000 names), the tideman graph will think they are the same candidate and will not be accurate (although it will not crash).