# the variable 'teams' is already defined
from itertools import combinations
teams = ['Best-ever', 'Not-so-good', 'Amateurs']
my_iter = combinations(teams, 2)
for team in my_iter:
    print(team)
# the variable 'teams' is already defined