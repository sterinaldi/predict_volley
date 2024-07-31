import numpy as np
import matplotlib.pyplot as plt
from matplotlib import axes, colormaps
from matplotlib.colors import Normalize
from matplotlib.gridspec import GridSpec
from scipy.stats import mode

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
    dt = np.dtype([('won', float), ('points', float), ('q_set', float)])
    v  = np.array([(wi, pi, qi) for wi, pi, qi in zip(won, points, q_set)], dtype = dt)
    stand = np.abs(np.argsort(np.argsort(v, order = ['won', 'points', 'q_set'])) - len(teams))
    for team, s in zip(teams, stand):
        if pool:
            team.pool_standing = s
        else:
            team.tournament_standing = s + remaining

def PlotResults(tournament):
    from predict_volley.tournament import Tournament
    if isinstance(tournament, Tournament):
        for pool in tournament.pools.keys():
            _plot_results(tournament.pools[pool], name = tournament.name+' - '+tournament.pools[pool].name, pool = True)
    _plot_results(tournament)

def _plot_results(tournament, name = None, pool = False):
    colormap = 'coolwarm'
    if name is None:
        name = tournament.name
    teams    = tournament.teams
    bins     = np.arange(1,len(teams)+2)
    if not pool:
        results = np.array([team.tournament_result for team in teams])
    else:
        results = np.array([team.pool_result for team in teams])
    expected = np.array([np.median(result) for result in results])
    teams = teams[np.argsort(expected)]
    results = results[np.argsort(expected)]
    # Labels
    xlabel = r'$\mathrm{Ranking}$'

    color = iter(colormaps[colormap](np.linspace(1, 0, len(teams))))
    cmappable = plt.cm.ScalarMappable(norm=Normalize(1,len(teams)+1), cmap=colormap)
    num_axes = len(teams)

    # Each plot will have its own axis
    if pool:
        fig = plt.figure(figsize = (len(teams)*1.2,len(teams)))
    else:
        fig = plt.figure(figsize = (len(teams)*0.8,len(teams)))
    gs = GridSpec(len(teams), len(teams), figure = fig)
    _axes = []
    [_axes.append(fig.add_subplot(gs[i, :-1])) for i in range(len(teams))]
    for i, (team, result) in enumerate(zip(teams[::-1], results[::-1])):
        ax = _axes[i]
        c = next(color)
        ax.hist(result, bins = bins, histtype = 'bar', density = True, clip_on = True, color = c, edgecolor = c, linewidth = 2, alpha = 0.65, align='left')
        ax.set_ylabel(r'$\mathrm{'+team.label+'}$', rotation = 0, loc = 'bottom')
        # Setup the current axis: transparency, labels, spines.
        ax.yaxis.grid(False)
        ax.patch.set_alpha(0)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_ticks([])
        ax.xaxis.set_ticks(np.arange(0,len(teams)+2))
        ax.tick_params(axis='x', which='both', length=0)
        ax.set_frame_on(False)

    # Final adjustments
    # Compute a final axis, used to apply global settings
    last_axis = fig.add_subplot(gs[:, :-1])
    for side in ['top', 'bottom', 'left', 'right']:
        last_axis.spines[side].set_visible(False)

    # This looks hacky, but all the axes share the x-axis,
    # so they have the same lims and ticks
    last_axis.set_xlim(_axes[0].get_xlim())
    last_axis.set_xticks(np.array(_axes[0].get_xticks()[1:-1]))
    last_axis.tick_params(axis='x', which='both', length=0)
    for t in last_axis.get_xticklabels():
        t.set_visible(True)
    else:
        last_axis.xaxis.set_visible(True)
    last_axis.yaxis.set_visible(False)
    last_axis.grid(False)

    # Last axis on the back
    last_axis.zorder = min(a.zorder for a in _axes) - 1
    _axes = list(_axes) + [last_axis]
    last_axis.set_xlabel(xlabel)

    # The magic overlap happens here.
    fig.tight_layout(h_pad=0)
    plt.title(name)
    fig.savefig(name+'.pdf', bbox_inches = 'tight')
    plt.close()
