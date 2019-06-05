# Narrative Dice Probability Calculator
Python code to calculate the probabilities of rolling different combinations of narrative dice, as described below. The narrative dice are called: boost (d6), setback (d6), ability (d8), difficulty (d8), proficiency (d12), and challenge (d12). Their results can include: successes and failures (which cancel 1-to-1), advantages and threats (which cancel 1-to-1), and triumphs and despairs (which do not cancel).

d6 | 1 | 2 | 3 | 4 | 5 | 6
:--------|:-:|:-:|:-:|:-:|:-:|:-:
**Boost**   | Blank | Blank | 1 Success <br>&nbsp; | 1 Success <br> 1 Advantage | <br> 2 Advantage | <br> 1 Advantage
**Setback** | Blank | Blank | 1 Failure <br>&nbsp; | 1 Failure <br>&nbsp; | <br> 1 Threat | <br> 1 Threat

d8 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
:--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:
**Ability**    | Blank | 1 Success <br>&nbsp; | 1 Success <br>&nbsp; | 2 Successes <br>&nbsp; | <br> 1 Advantage | <br> 1 Advantage | 1 Success <br> 1 Advantage | <br> 2 Advantages
**Difficulty** | Blank | 1 Failure <br>&nbsp; | 2 Failures <br>&nbsp; | <br> 1 Threat | <br> 1 Threat | <br> 1 Threat | <br> 2 Threat | 1 Failure <br> 1 Threat

d12 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12
:--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:--:|:--:|:--:
**Proficiency** | Blank | 1 Success <br>&nbsp; | 1 Success <br>&nbsp; | 2 Successes <br>&nbsp; | 2 Successes <br>&nbsp; | <br> 1 Advantage | 1 Success <br> 1 Advantage | 1 Success <br> 1 Advantage | 1 Success <br> 1 Advantage | <br> 2 Advantages | <br> 2 Advantages | 1 Success <br> Triumph
**Challenge**   | Blank | 1 Failure <br>&nbsp; | 1 Failure <br>&nbsp; | 2 Failures <br>&nbsp; | 2 Failures <br>&nbsp; | <br> 1 Threat | <br> 1 Threat | 1 Failure <br> 1 Threat | 1 Failures <br> 1 Threat | <br> 2 Threats | <br> 2 Threats | 1 Failure <br> Despair

## Usage
For now, invoke 'python main.py' from the command line in the project directory and add arguments defining a dice pool (from which to gather potential results) and the extrapolated data desired by the user.

Dice arguments are positional: **b** for **boost**, **a** for **ability**, **p** for **proficiency**, and so on. These arguments aren't sensitive to capitalization.

Optional arguments specify the extrapolated data from the dice pool:

* **-h, --help**: show the help message and exit
* **-s, --summary**: summary of simple outcome probabilities
* **-d, --discrete**: discrete probabilities per result count
* **-c, --cumulative**: probabilities of at least each given result count

### Example
The command `python main.py a a p d d s -sc` will build a dice pool of 2 ability dice, 1 proficiency die, 2 difficulty dice, and 1 setback die. It will then summarize the overall probabilities of success, advantage, threat, triumph, and despair. It will further calculate the cumulative probabilities (at least X number of Y result) for success, failure, advantage, and threat.

## Notes & Todos
The code returns correct results when checked against manual test cases but works very naively and slowly. It builds a tree, for which each node is a single face (potential roll) of a die. These results are stored in a 4-tuple, and accumulate down the tree. The leaves of the tree are therefore each possible result from rolling a given pool of dice.

### Todo List
These todos are also scattered as comments in the code.

* **File I/O**: file export to CSV and JSON for consumption by other programs.
  * **Functions in DicePoolData**: for export of CSV and JSON data.
  * **Argument Parsing**: `-e, --export` flag, pick function based on given filename's extension
  * **Check Behavior**: check the behavior of other command line utilities to see if the above conforms to common usage (and user expectations)
* **Optimization**: Use look-up tables for common sub-trees of the same die-type (e.g. store and recover a tree of up to 5 difficulty dice) so that these sub-trees can be accessed and composed rather than dynamically (and wastefully) computed.