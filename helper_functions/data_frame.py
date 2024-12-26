# importing things
from collections import defaultdict

"""
    Popular vote
"""
# Find nearest candidate
def find_nearest_candidate(value, head):
    if head is None:
        raise ValueError("Candidate list is empty. Add candidates first.")

    current = head
    nearest_candidate_node = current
    min_difference = abs(current.data - value)

    while current is not None:
        difference = abs(current.data - value)
        if difference < min_difference:
            min_difference = difference
            nearest_candidate_node = current
        current = current.next

    return nearest_candidate_node

# Popular vote function.
# Usage: Must pass through a distribution. For example popular_vote(samples.normal())
def popular_vote(distribution, politicians):
    dist = distribution
    popularvote = defaultdict(int)
    for value in dist:
        nearest_cand_node = find_nearest_candidate(value, politicians.head)
        popularvote[nearest_cand_node] += 1
    return dict(popularvote)

"""
    Ranked-choice voting
"""
# Generate ranked preferences based on a distribution
# Each "voter" is represented as a list of candidate preferences sorted by distance from their ideology
def generate_ranked_preferences(distribution, politicians):
    preferences = []
    current = politicians.head

    candidates = []
    while current is not None:
        candidates.append(current)  # Use the entire node
        current = current.next

    for value in distribution:
        ranked = sorted(candidates, key=lambda c: abs(c.data - value))  # Access c.data
        preferences.append(ranked)

    return preferences

# Ranked choice voting function
# Usage: Must pass through a distribution. For example popular_vote(samples.normal())
# Check Usage for documentation of output
def ranked_choice_voting(distribution, politicians):
    # Generate ranked preferences
    preferences = generate_ranked_preferences(distribution, politicians)

    # Initialize vote counts
    vote_counts = defaultdict(int)
    for pref in preferences:
        vote_counts[pref[0]] += 1  # Use the node as the key

    # Total number of votes
    total_votes = len(preferences)

    # Dataset to store results of each round
    dataset = []
    round_number = 1

    while True:
        # Record the current round's data
        round_data = {
            "round": round_number,
            "vote_counts": {candidate: votes for candidate, votes in vote_counts.items()}
        }
        dataset.append(round_data)

        # Check if any candidate has more than 50% of the votes
        for candidate, votes in vote_counts.items():
            if votes > total_votes / 2:
                return dataset  # Candidate wins

        # Find the candidate(s) with the fewest votes
        min_votes = min(vote_counts.values())
        candidates_to_eliminate = [c for c, v in vote_counts.items() if v == min_votes]

        # Eliminate the candidate(s) with the fewest votes
        for candidate in candidates_to_eliminate:
            del vote_counts[candidate]

            # Remove the eliminated candidate from all voters' preferences
            for pref in preferences:
                if candidate in pref:
                    pref.remove(candidate)

        # Recalculate vote counts for the next round
        vote_counts = defaultdict(int)
        for pref in preferences:
            if pref:  # Ensure there's at least one candidate left
                vote_counts[pref[0]] += 1

        # Check for tie or no candidates left
        if not vote_counts:
            print("No candidates left or tie detected.")
            return dataset

        round_number += 1

"""
    Ranked-Pairs/Tideman
"""
# Generate pairwise preferences
def calculate_pairwise_preferences(preferences, candidates):
    pairwise_counts = defaultdict(int)
    num_candidates = len(candidates)

    for pref in preferences:
        for i in range(num_candidates):
            for j in range(i + 1, num_candidates):
                if pref.index(candidates[i]) < pref.index(candidates[j]):
                    pairwise_counts[(candidates[i], candidates[j])] += 1
                else:
                    pairwise_counts[(candidates[j], candidates[i])] += 1

    return pairwise_counts
def ranked_pairs_voting(distribution, politicians):
    # Generate ranked preferences and candidate list
    preferences = generate_ranked_preferences(distribution, politicians)
    current = politicians.head

    candidates = []
    while current is not None:
        candidates.append(current)  # Use the entire node
        current = current.next

    # Calculate pairwise preferences
    pairwise_counts = calculate_pairwise_preferences(preferences, candidates)

    # Sort pairs by margin of victory
    pairs = []
    for (a, b), votes in list(pairwise_counts.items()):
        reverse_votes = pairwise_counts.get((b, a), 0)
        if votes > reverse_votes:
            margin = votes - reverse_votes
            pairs.append((a, b, margin))

    # Sort by descending margin
    pairs.sort(key=lambda x: -x[2])

    # Lock pairs without creating cycles
    locked = defaultdict(list)

    def creates_cycle(locked, start, end, visited=None):
        if visited is None:
            visited = set()
        if start == end:
            return True
        visited.add(start)
        for neighbor in locked[start]:
            if neighbor not in visited and creates_cycle(locked, neighbor, end, visited):
                return True
        return False

    for a, b, _ in pairs:
        if not creates_cycle(locked, b, a):
            locked[a].append(b)

    # Determine the winner
    incoming_edges = {candidate: 0 for candidate in candidates}
    for start, ends in locked.items():
        for end in ends:
            incoming_edges[end] += 1

    # The winner is the candidate with no incoming edges
    winner = [candidate for candidate, edges in incoming_edges.items() if edges == 0]
    return locked, winner[0] if winner else None

"""
    Adding/removing candidates
"""
# Function that adds a candidate based on user input
def add_candidate(n, politicians):
    if -1 <= n <= 1:
        politicians.prepend(n)
    return

# Function that removes a candidate based on user input.
# N is the candidate number. Basically if there is a candidate that is currently located at n, then it removes that candidate.
def remove_candidate(n, politicians):
    politicians.delete(n)
    return