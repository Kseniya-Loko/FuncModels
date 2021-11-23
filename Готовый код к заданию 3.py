import numpy as np
import pandas as pd
__author__ = 'Chris Potts'


class RSA:
    """Implementation of the core Rational Speech Acts model.

    Parameters
    ----------
    lexicon : `np.array` or `pd.DataFrame`
        Messages along the rows, states along the columns.
    prior : array-like
        Same length as the number of colums in `lexicon`.
    costs : array-like
        Same length as the number of rows in `lexicon`.
    alpha : float
        The temperature parameter. Default: 1.0
    """
    def __init__(self, lexicon, prior, costs, alpha=1.0):
        self.lexicon = lexicon
        self.prior = np.array(prior)
        self.costs = np.array(costs)
        self.alpha = alpha

    def literal_listener(self):
        """Literal listener predictions, which corresponds intuitively
        to truth conditions with priors.

        Returns
        -------
        np.array or pd.DataFrame, depending on `self.lexicon`.
        The rows correspond to messages, the columns to states.

        """
        return rownorm(self.lexicon * self.prior)
           
    def speaker(self):
        """Returns a matrix of pragmatic speaker predictions.

        Returns
        -------
        np.array or pd.DataFrame, depending on `self.lexicon`.
        The rows correspond to states, the columns to states.
        """
        lit = self.literal_listener().T
        utilities = self.alpha * (safelog(lit) + self.costs)
        return rownorm(np.exp(utilities))

    def listener(self):
        """Returns a matrix of pragmatic listener predictions.

        Returns
        -------
        np.array or pd.DataFrame, depending on `self.lexicon`.
        The rows correspond to messages, the columns to states.
        """
        spk = self.speaker().T
        return rownorm(spk * self.prior)


def rownorm(mat):
    """Row normalization of np.array or pd.DataFrame"""
    return (mat.T / mat.sum(axis=1)).T


def safelog(vals):
    """Silence distracting warnings about log(0)."""
    with np.errstate(divide='ignore'):
        return np.log(vals)


if __name__ == '__main__':
    """Examples"""

    from IPython.display import display
    
    
    def display_reference_game(mod):
        d = mod.lexicon.copy()
        d['costs'] = mod.costs
        d.loc['prior'] = list(mod.prior) + [""]
        d.loc['alpha'] = [mod.alpha] + [" "] * mod.lexicon.shape[1]
        display(d)


    # Core lexicon:
    msgs = ['hat', 'glasses', 'mustache']
    states = ['r1', 'r2', 'r3']
    lex = pd.DataFrame([
        [1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0]], index=msgs, columns=states)
    print("="*70 + "\nEven priors and all-0 message costs\n")
    basic_mod = RSA(lexicon=lex, prior=[0.33, 0.33, 0.33], costs=[0.0, 0.0, 0.0])

    display_reference_game(basic_mod)

    print("\nLiteral listener")
    display(basic_mod.literal_listener())

    print("\nPragmatic speaker")
    display(basic_mod.speaker())

    print("\nPragmatic listener")
    display(basic_mod.listener())