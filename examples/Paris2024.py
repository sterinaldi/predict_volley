from predict_volley.teams import Team
from predict_volley.tournament import Tournament
from predict_volley.utils import PlotResults

teams = [[Team('France', 4), Team('Slovenia', 5), Team('Serbia', 11, 'SRB'), Team('Canada', 10)],
         [Team('Egypt', 20), Team('Poland', 1), Team('Italy', 2), Team('Brazil', 7)],
         [Team('USA', 6), Team('Germany', 9), Team('Japan', 3, 'JPN'), Team('Argentina', 8)],
        ]

olympics = Tournament(teams, olympics = True, name = 'Paris 2024')
# Matches as of 15:00 of 31/07
olympics.pools['A'].set_results(['JPN-GER', '2-3'], ['FRA-SRB', '3-2'], ['SLO-CAN', '3-1'], ['SLO-SER', '3-0'], ['FRA-CAN', '3-0'])
olympics.pools['B'].set_results(['ITA-BRA', '3-1'], ['POL-EGY', '3-0'], ['ITA-EGY', '3-0'], ['POL-BRA', '3-2'])
olympics.pools['C'].set_results(['USA-ARG', '3-0'], ['USA-GER', '3-2'], ['JPN-ARG', '3-1'])
# Prediction
olympics.predict()

PlotResults(olympics)
