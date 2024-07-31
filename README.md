# predict_volley
Framework to predict the outcome of an internationall volleyball tournament.

Each team is represented using the dedicated `predict_volley.teams.Team` class, which takes as inputs the name of the national team, its [FIVB ranking](https://en.volleyballworld.com/volleyball/world-ranking/men) and a three-letters label (optional):

```python
from predict_volley.teams import Team

italy = Team(name = 'Italy', ranking = 2, label = 'ITA')
```

A tournament is instatiated using the `predict_volley.tournament.Tournament` class. This class takes as input a 2D list of `Team` objects, one list per pool:

```python
from predict_volley.tournament import Tournament

pools = [[team1, team2, team3, team4],
         [team5, team6, team7, team8],
         [team9, team10, team11, team12]]

world_cup = Tournament(pools, name = 'World Cup', olympics = False)
```

The `olympics` keyword argument controls the way in which the knockout stage is built, either using the aggregated ranking (`olympics = False`) or using the [Paris 2024 formula](https://en.volleyballworld.com/volleyball/competitions/volleyball-olympic-games-paris-2024/competition/formula) (`olympics = True`).
The predicted results can be displayed using the `predict_volley.utils.PlotResults` method:

```python
from predict_volley.utils import PlotResults
PlotResults(world_cup)
```

A working example can be found in the [Paris2024 folder](https://github.com/sterinaldi/predict_volley/tree/main/Paris2024), where you can find the Paris 2024 Olympic Tournament already set up, with the results updated with all the matches played up to July 31, 15:00 CEST.
To try it, simply move to that folder and run
```bash
cd Paris2024
python Paris2024.py
```
