import numpy as np

x = np.linspace(0,1,8)[1:-1]

def ProbabilityResult(r1, r2):
    alpha = np.abs(r1-r2)
    if r1 > r2:
        q = 1-0.5*r2/r1
    if r2 >= r1:
        q = 0.5*r1/r2
    a = alpha*q
    b = alpha*(1-q)
    p = x**(a-1)*(1-x)**(b-1)
    return p/np.sum(p)

def Standings(tournament, pool = True, remaining = 0):
    if pool:
        teams = tournament.teams
    else:
        teams = tournament.active_teams
    won    = np.array([team.won for team in teams])
    points = np.array([team.points for team in teams])
    with np.errstate(divide = 'ignore'):
        q_set = np.array([team.sets_won/team.sets_lost if team.sets_lost > 0 else np.inf for team in teams])
    dt = np.dtype([('won', np.float64), ('points', np.float64), ('q_set', np.float64)])
    v  = np.array([(wi, pi, qi) for wi, pi, qi in zip(won, points, q_set)], dtype = dt)
    stand = np.abs(np.argsort(v, order = ['won', 'points', 'q_set']) - len(teams))
    for team, s in zip(teams, stand):
        if pool:
            team.pool_standing = s
        else:
            team.tournament_standing = s + remaining
