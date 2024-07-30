class Team:
    """
    Class to represent a volleyball national team
    
    Arguments:
        str name: team name
        float ranking: FIVB ranking
        str label: team label
    """
    def __init__(self,
                 name,
                 ranking,
                 label = None,
                 ):
        self.name = name
        self.ranking = ranking
        if label is not None:
            self.label = label.upper()
        else:
            self.label = self.name[:3].upper()
        # Tournament results
        self.won       = 0
        self.points    = 0
        self.sets_won  = 0.
        self.sets_lost = 0.
        # Actual results (IRL)
        self.played_won       = 0
        self.played_points    = 0
        self.played_sets_won  = 0.
        self.played_sets_lost = 0.
        # Outcome
        self.pool_standing       = None
        self.tournament_standing = None
        self.pool_result         = []
        self.tournament_result   = []
