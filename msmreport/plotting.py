import seaborn as sns

import numpy as np
from scipy.stats import gaussian_kde

from matplotlib import pyplot as plt


def plot_bars(timescales, sigma_ts, sigma=5, lower=1E2, upper=1E6):
    sns.set_style('dark')

    fig = plt.figure()
    ax = plt.subplot(111)
    colors = ['#d64d67', '#547098'] + 3*['#525055']
    for i, item in enumerate(zip(timescales, sigma_ts)):
        t, s = item
        color = colors[i]
        ax.errorbar([0, 1], [t, t], c=color)
        ax.fill_between([0, 1], y1=[t - sigma*s, t - sigma*s],
                        y2=[t + sigma*s, t + sigma*s], color=color, alpha=0.2)
    plt.xticks([])
    plt.ylabel(r'Relaxation Time ($ns$)', size=18)
    plt.yscale('log')
    autoAxis = ax.axis()
    plt.ylim([lower, upper])
    rec = plt.Rectangle((autoAxis[0], 100), (autoAxis[1] - autoAxis[0]),
                        upper, fill=False, lw=2)
    rec = ax.add_patch(rec)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
    return fig, ax


def scipy_kde(sample, obs=(0, 1), n=300000, p=None, bw_method='scott'):
    """
    Returns  a population weighted kernel. Useful for plotting things
    :param pr_mdl: The protein mdl to use
    :param pop_vector: Population vector to use when sampling tic values.
    Defaults to the msm population vector if None is given.
    :param obs: Tuple of either dictionaries or ints. Defaults to 0 and 1st tic
    :param n_samples: The number of samples to use to fit the kde
    :param bw_method: See scipy gaussian kde.
    :return: The fitted kernel, and the
    """
    idx = np.random.choice(range(sample.shape[0]), size=n, p=p)
    prune = sample[idx, :]
    _x_val, _y_val = prune[:, obs].T
    kernel = gaussian_kde(np.vstack((_x_val, _y_val)), bw_method=bw_method)

    return kernel, _x_val, _y_val


def two_dim_free_energy_kde(sample,
                            eigs=None,
                            obs=(0, 1),
                            n=300000,
                            p=None,
                            bw_method='scott',
                            mlp_fct=1.4):

    """
    Get a free energy landscape for a protein mdl
    :param pr_mdl: The protein mdl under consideration
    :param limits_dict: Limits of the tics being considered
    :param pop_vector: optional population vector. Defaults to the msm pop.
    :param obs: Tuple of either dictionaries or ints. Defaults to 0 and 1st tic
    :param n_samples: Number of samples to use. defaults to 30000
    :param bw_method: Band width method for the kernel. Defaults to "scott"
    :param mlp_fct: Multiplicative factor for the boundaries to allow the "extra"
    edges around the data to make smoother kde plots
    :return: X,Y, and a population weighted free energy map(in kcals/mol). Use
    contourf(X,Y, f) to plot the results. Limit levels to something reasonable
    to account to the non-existant tic spaces
    """
    if eigs is not None:
        sample = sample*eigs
    kernel, x, y = scipy_kde(sample, obs, n, p, bw_method)

    x_lim = mlp_fct*np.array([x.min(), x.max()])
    y_lim = mlp_fct*np.array([y.min(), y.max()])
    n_p = 100
    x = np.linspace(x_lim[0], x_lim[1], n_p)
    y = np.linspace(y_lim[0], y_lim[1], n_p)

    # make a mesh grid
    X, Y = np.meshgrid(x, y)

    # create a massive n*2 array
    positions = np.vstack([X.flatten(), Y.flatten()])

    return X, Y, -.6 * np.log(kernel.evaluate(positions)).reshape(n_p, n_p)


def plot_free_energy(sample,
                     eigs=None,
                     obs=(0, 1),
                     n=300000,
                     p=None,
                     bw_method='scott',
                     mlp_fct=1.4):

    sns.set_style('whitegrid')
    my_cmap = sns.palettes.blend_palette(['#547098', '#FFF8DC', '#d64d67'],
                                         as_cmap=True)

    X, Y, Z = two_dim_free_energy_kde(sample, eigs, obs, n, p, bw_method,
                                      mlp_fct)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca()

    ax.contourf(X, Y, Z - Z.min(), levels=np.linspace(0, 4, 10), rstride=8,
                cstride=8, alpha=1, cmap=my_cmap, zorder=1, vmin=0, vmax=6)
    ax.contour(X, Y, Z - Z.min(), levels=np.linspace(0, 4, 10), rstride=8,
               cstride=8, alpha=1, cmap=plt.get_cmap('bone'), zorder=1,
               vmin=0, vmax=6)

    ax.set_xlim([round(.95 * X.min(), 0), round(.9 * X.max(), 0)])
    ax.set_ylim([round(1.05 * Y.min(), 0), round(Y.max(), 0)])

    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(zorder=0)

    return fig, ax
