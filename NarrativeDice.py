import operator

# Each die face is a tuple with four numbers representing results on that face.
# The four numbers represent, in order: (Success/Failure, Advantage/Threat, Triumph, Despair).
# Each die type is an array of "face tuples": boost, setback, ability, difficulty, proficiency, challenge.
# Success and Advantage are positive integers, while Failure and Threat are negative integers.
# Triumph and Despair are each either 0 or 1 (for counting purposes).

boost = [(0, 0, 0, 0), (0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0), (0, 2, 0, 0), (0, 1, 0, 0)]
setback = [(0, 0, 0, 0), (0, 0, 0, 0), (-1, 0, 0, 0), (-1, 0, 0, 0), (0, -1, 0, 0), (0, -1, 0, 0)]
ability = [(0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (2, 0, 0, 0),
           (0, 1, 0, 0), (0, 1, 0, 0), (1, 1, 0, 0), (0, 2, 0, 0)]
difficulty = [(0, 0, 0, 0), (-1, 0, 0, 0), (-2, 0, 0, 0), (0, -1, 0, 0),
              (0, -1, 0, 0), (0, -1, 0, 0), (0, -2, 0, 0), (-1, -1, 0, 0)]
proficiency = [(0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (2, 0, 0, 0), (2, 0, 0, 0), (0, 1, 0, 0),
               (1, 1, 0, 0), (1, 1, 0, 0), (1, 1, 0, 0), (0, 2, 0, 0), (0, 2, 0, 0), (1, 0, 1, 0)]
challenge = [(0, 0, 0, 0), (-1, 0, 0, 0), (-1, 0, 0, 0), (-2, 0, 0, 0), (-2, 0, 0, 0), (0, -1, 0, 0),
             (0, -1, 0, 0), (-1, -1, 0, 0), (-1, -1, 0, 0), (0, -2, 0, 0), (0, -2, 0, 0), (-1, 0, 0, 1)]

# Functions to legibly access result types on a die's "face."
def success(result): return result[0]       # A negative result here means some number of Failures.
def advantage(result): return result[1]     # A negative result here means some number of Threats.
def triumph(result): return result[2]
def despair(result): return result[3]


class DicePoolData:
    # Several dictionaries and variables holding data collected from a tree of DieNode objects.
    # Accompanying functions to interrogate, export, and display the data.
    # TODO: Write file export supporting (JSON?, CSV?, Database?, ???)
    #  - This means cumulative() and discrete() must feed into data structures
    #  - With separate functions for printing and writing a file
    #  - Detect filetype for export from extensions? How do other programs work?

    results_count: float

    def __init__(self, results_list):
        self.results_list = results_list
        self.results_count = float(len(results_list))   # Cast to float to force division later
        # Triumph and despair not precisely tracked because quantities are less relevant to game balance.
        self.success_counts = {}        # Results by number of successes/failures
        self.advantage_counts = {}      # Results by number of advantages/threats
        self.any_success = 0            # Results with any success
        # Failure is defined as !Success (0 or fewer Success results), so it is not tracked as any_failure.
        self.any_advantage = 0          # Results with any advantage
        self.any_threat = 0             # Results with any threat
        self.any_triumph = 0            # Results with any triumph
        self.any_despair = 0            # Results with any despair
        # Iterate through the results list and count up each relevant result into buckets by quantity
        for r in self.results_list:
            # Count up success and failure
            self.success_counts.setdefault(success(r), 0)
            self.success_counts[success(r)] += 1
            if success(r) > 0:
                self.any_success += 1
            # Count up advantage and threat
            self.advantage_counts.setdefault(advantage(r), 0)
            self.advantage_counts[advantage(r)] += 1
            if advantage(r) > 0:
                self.any_advantage += 1
            elif advantage(r) < 0:
                self.any_threat += 1
            # Count up triumph and despair
            if triumph(r) > 0:
                self.any_triumph += 1
            if despair(r) > 0:
                self.any_despair += 1
        self.p_s = {}   # Probability of success by quantity of successes
        self.p_a = {}   # Probability of advantage by quantity of advantages
        self.p_t = {}   # Probability of threat by quantity of threats
        self.p_success = self.any_success / self.results_count      # Probability of any success
        self.p_advantage = self.any_advantage / self.results_count  # Probability of any advantage
        self.p_threat = self.any_threat / self.results_count        # Probability of any threat
        self.p_triumph = self.any_triumph / self.results_count      # Probability of any triumph
        self.p_despair = self.any_despair / self.results_count      # Probability of any despair
        # Calculate probabilities for each quantity of success/failure and advantage/threat
        for s in self.success_counts.keys():
            self.p_s[s] = self.success_counts[s] / self.results_count
        for a in self.advantage_counts.keys():
            self.p_a[a] = self.advantage_counts[a] / self.results_count

    def summary(self):
        print('\n Summary of Outcomes\n')
        print('       Success:', round(self.p_success * 100, 4), '%')
        print('     Advantage:', round(self.p_advantage * 100, 4), '%')
        print('        Threat:', round(self.p_threat * 100, 4), '%')
        print('       Triumph:', round(self.p_triumph * 100, 4), '%')
        print('       Despair:', round(self.p_despair * 100, 4), '%')

    def discrete(self):
        print('\n Discrete Probabilities: Successes/Failures\n')
        for s in range(max(self.p_s.keys()), 0, -1):
            print('     ', s, 'S:', round(self.p_s[s] * 100, 4), '%')
        for f in range(0, min(self.p_s.keys()) - 1, -1):
            print('     ', abs(f), 'F:', round(self.p_s[f] * 100, 4), '%')
        print('\n Discrete Probabilities: Advantages/Threats\n')
        for a in range(max(self.p_a.keys()), 0, -1):
            print('     ', a, 'A:', round(self.p_a[a] * 100, 4), '%')
        print('      0 A:', round(self.p_a[0] * 100, 4), '%')
        for t in range(-1, min(self.p_a.keys()) - 1, -1):
            print('     ', abs(t), 'T:', round(self.p_a[t] * 100, 4), '%')

    def cumulative(self):
        print('\n Cumulative Probabilities (at least): Successes/Failures\n')
        cumulative_success_p = 0.0
        cumulative_failure_p = 0.0
        cumulative_advantage_p = 0.0
        cumulative_threat_p = 0.0
        failure_sums = {}
        threat_sums = {}
        for s in range(max(self.p_s.keys()), 0, -1):
            cumulative_success_p += self.p_s[s]
            print('     ', s, 'S:', round(cumulative_success_p * 100, 4), '%')
        for f in range(min(self.p_s.keys()), 1, 1):
            cumulative_failure_p += self.p_s[f]
            failure_sums[f] = cumulative_failure_p
        for f in range(0, min(self.p_s.keys()) - 1, -1):
            print('     ', abs(f), 'F:', round(failure_sums[f] * 100, 4), '%')
        print('\n Cumulative Probabilities (at least): Advantages/Threats\n')
        for a in range(max(self.p_a.keys()), -1, -1):
            cumulative_advantage_p += self.p_a[a]
            print('     ', a, 'A:', round(cumulative_advantage_p * 100, 4), '%')
        for t in range(min(self.p_a.keys()), 1, 1):
            cumulative_threat_p += self.p_a[t]
            threat_sums[t] = cumulative_threat_p
        for t in range(-1, min(self.p_a.keys()) - 1, -1):
            print('     ', abs(t), 'T:', round(threat_sums[t] * 100, 4), '%')

class DieNode:
    # A tree of dice results. Each level of the tree represents outcomes of a die in a list.
    # Each node is a single face rolled. Each node's children are the possible rolls (faces) of the next die.

    def __init__(self, parent, face):
        self.parent = parent            # Parent node (None if root)
        self.face = face                # Die's face, containing a tuple of 4 results
        self.cumulative_results = face  # Running total including all parent results in this tree walk
        if self.parent is not None:
            self.cumulative_results = tuple(map(operator.add, parent.cumulative_results, face))
        self.children = None

    def append_die(self, outcomes):
        # Append a new die to all the tree's present leaves, establishing a new layer of leaves.
        if self.children is None:
            self.children = []
            for face in outcomes:
                self.children.append(DieNode(self, face))
        else:
            for child in self.children:
                child.append_die(outcomes)

    def append_dice(self, dice):
        # Appends a list of dice to the tree in succession
        for die in dice:
            self.append_die(die)

    def gather_results(self):
        # Collect cumulative results from each leaf node into a list of result tuples
        # TODO: Integrate this traversal into building the tree
        if self.children is not None:
            results_list = []
            for child in self.children:
                if child.children is None:
                    results_list.append(child.gather_results())
                else:
                    results_list.extend(child.gather_results())
            return results_list
        else:
            return self.cumulative_results

    def export_results(self):
        results_list = self.gather_results()
        return DicePoolData(results_list)
