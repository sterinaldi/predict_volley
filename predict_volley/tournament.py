import numpy as np
from itertools import combinations
from string import ascii_uppercase
from predict_volley.utils import ProbabilityResult, Standings

possible_results = ['3-0', '3-1', '3-2', '2-3', '1-3', '0-3']

class Match:
    """
    Match between two teams
    
    Arguments:
        predict_volley.teams.Team team1: first team
        predict_volley.teams.Team team2: second team
    """
    def __init__(self, team1, team2):
        self.team1  = team1
        self.team2  = team2
        self.labels = ['-'.join((self.team1.label, self.team2.label)), '-'.join((self.team2.label, self.team2.label))]
        self.played  = False
        
    def play(self):
        p = ProbabilityResult(self.team1.ranking, self.team2.ranking)
        res = np.random.choice(possible_results, p = p)
        self.result(res)

    def result(self, result):
        self.outcome = result
        self.team1.sets_won  += float(result[0])
        self.team1.sets_lost += float(result[2])
        self.team2.sets_won  += float(result[2])
        self.team2.sets_lost += float(result[0])
        if self.played:
            self.team1.played_sets_won  += float(result[0])
            self.team1.played_sets_lost += float(result[2])
            self.team2.played_sets_won  += float(result[2])
            self.team2.played_sets_lost += float(result[0])
        if result == '3-0' or result == '3-1':
            self.winner = self.team1
            self.loser  = self.team2
            self.team1.points += 3
            if self.played:
                self.team1.played_points += 3
        if result == '3-2':
            self.winner = self.team1
            self.loser  = self.team2
            self.team1.points += 2
            self.team2.points += 1
            if self.played:
                self.team1.played_points += 2
                self.team2.played_points += 1
        if result == '2-3':
            self.winner = self.team2
            self.loser  = self.team1
            self.team1.points += 1
            self.team2.points += 2
            if self.played:
                self.team1.played_points += 1
                self.team2.played_points += 2
        if result == '1-3' or result == '0-3':
            self.winner = self.team2
            self.loser  = self.team1
            self.team2.points += 3
            if self.played:
                self.team2.played_points += 3
        self.winner.won += 1
        if self.played:
            self.winner.played_won += 1

class Pool:
    """
    First round pool
    
    Arguments:
        list teams: participating teams
    """
    def __init__(self, teams, pool_name = None, reset = True):
        self.teams   = teams
        self.matches = [Match(t1, t2) for (t1, t2) in combinations(self.teams, 2)]
        if reset:
            self.reset()
        if pool_name is not None:
            self.pool_name = pool_name
        else:
            self.pool_name = 'Pool'

    def reset(self):
        for team in self.teams:
            team.won           = team.played_won
            team.points        = team.played_points
            team.sets_won      = team.played_sets_won
            team.sets_lost     = team.played_sets_lost
            team.pool_standing = None

    def set_results(self, results):
        for result in results:
            for match in self.matches:
                if result[0] in match.labels:
                    match.played = True
                    match.result(result[1])

    def play(self):
        for match in self.matches:
            if not match.played:
                match.play()
        Standings(self)

    def predict(self, n_draws = 1000):
        for team in self.teams:
            team.pool_result = []
        for _ in range(int(n_draws)):
            self.play()
            for team in self.teams:
                team.pool_result.append(team.pool_standing)
            self.reset()

class Knockout:
    """
    Knockout stage
    
    Arguments:
        list teams: ordered list of participating teams
    """
    def __init__(self, teams):
        self.teams   = np.array(teams)
        self.active_teams = self.teams
        self.update_matches()
        self.reset()
    
    def update_matches(self):
        self.matches = [Match(self.active_teams[i], self.active_teams[len(self.active_teams)-(i+1)]) for i in range(len(self.active_teams)//2)]
    
    def reset(self):
        for team in self.teams:
            team.won                 = 0
            team.points              = 0
            team.sets_won            = 0.
            team.sets_lost           = 0.
            team.tournament_standing = None
        self.active_teams = self.teams
        self.update_matches()
    
    def play(self):
        while True:
            self.advance()
            if len(self.matches) > 2:
                self.active_teams = [match.winner for match in self.matches]
                self.update_matches()
            else:
                break
        # Semi-finals
        self.advance()
        # Finals
        gold_final   = Match(self.matches[0].winner, self.matches[1].winner)
        bronze_final = Match(self.matches[0].loser, self.matches[1].loser)
        bronze_final.play()
        bronze_final.winner.tournament_standing = 3
        bronze_final.loser.tournament_standing  = 4
        gold_final.play()
        gold_final.winner.tournament_standing = 1
        gold_final.loser.tournament_standing  = 2
    
    def advance(self):
        for match in self.matches:
            match.play()
        losers_pool = Pool([match.loser for match in self.matches])
        losers_pool.active_teams = losers_pool.teams
        Standings(losers_pool, pool = False, remaining = len(self.active_teams)//2)

class Tournament:
    """
    Tournament
    
    Arguments:
        list of lists of Teams: pools
    """
    def __init__(self, pools, olympics = False):
        self.teams = np.array([team for pool in pools for team in pool])
        self.pools = {s: Pool(pool, f'Pool {s}') for pool, s in zip(pools, ascii_uppercase[:len(pools)])}
        self.olympics = olympics

    def reset(self):
        for pool in pools:
            pool.reset()
    
    def create_knockout(self):
        if self.olympics:
            for i in range(len(self.pools['A'].teams)):
                temp_pool = Pool([team for team in self.teams if team.pool_standing == i+1], reset = False)
                temp_pool.active_teams = temp_pool.teams
                Standings(temp_pool, pool = False, remaining = i*len(self.pools.keys()))
        else:
            self.active_teams = self.teams
            Standings(self, pool = False)
        rr            = [team.tournament_standing for team in self.teams]
        idx           = np.argsort(rr)[::-1]
        self.teams    = self.teams[idx]
        self.knockout = Knockout(self.teams[-8:])
    
    def play(self):
        for pool in self.pools.keys():
            self.pools[pool].play()
        self.create_knockout()
        self.knockout.play()
    
    def predict(self, n_draws = 1000):
        for team in self.teams:
            team.tournament_result = []
        for _ in range(int(n_draws)):
            self.play()
            for team in self.teams:
                team.pool_result.append(team.tournament_standing)
            self.reset()
