"""ScoreGrid is a utility class holding information about which scores
to use and report
"""

# Authors: Lyubomir Danov <->
# License: -

import collections.abc

from sklearn.metrics import accuracy_score, f1_score, make_scorer
from sklearn.metrics.scorer import _BaseScorer

_DEFAULT_SCORE_SELECTION = [{'score_name': 'Accuracy', 'score_key': 'rank_test_Accuracy',
                             'score_criteria': 'min', 'scorer': make_scorer(accuracy_score)},
                            {'score_name': 'F1-Score', 'score_key': 'rank_test_F1-Score',
                             'score_criteria': 'min', 'scorer': make_scorer(f1_score)}]


class ScoreGrid:
    """Generates a ScoreGrid as required by `cvextend.EvaluationGrid`

    Parameters
    ----------
    score_selection : list of dicts
        A list of dictionaries. Each dictionary contains the following
        keys and values:

        * 'score_name' (str)
            name of the score, used for determining best
        * 'score_key' (str)
            key as found in a fitted instance of `BaseSearchCV.cv_results_`.
            Will be used to select the desired value
        * 'score_criteria' (str or callable)
            function or str function name as taken by
            `pandas.DataFrame.transform`. Will be used to select the
            winning value from score_key column's values
        * 'scorer' - (sklearn.scorer)
            a callable as returned by `sklearn.metrics.make_scorer`

    Examples
    --------
    >>> from cvextend import ScoreGrid
    >>> example_scores = [
    ...     {
    ...         'score_name': 'Accuracy',
    ...         'score_key': 'rank_test_Accuracy',
    ...         'score_criteria': 'min',
    ...         'scorer': make_scorer(accuracy_score)
    ...     },
    ...     {
    ...         'score_name': 'F1-Score',
    ...         'score_key': 'rank_test_F1-Score',
    ...         'score_criteria': 'min',
    ...         'scorer': make_scorer(f1_score)
    ...     }
    ... ]
    >>> sc = ScoreGrid(example_scores)
    >>> sc.get_sklearn_dict()
    >>> sc.score_selection

    """

    _expected_keys = [
        {
            # user-defined name that will be used in generating result df columnname
            'name': 'score_name',
            'type': str
        },
        {
            # which column or key to use when looking for metric
            'name': 'score_key',
            'type': str
        },
        {
            # which pandas-known string callable to give to call transform on results
            'name':  'score_criteria',
            'type': (str, collections.abc.Callable)
        },
        {
            # scorer object itself
            'name': 'scorer',
            'type': _BaseScorer
        }]

    def __init__(self, score_selection=_DEFAULT_SCORE_SELECTION):
        for score in score_selection:
            for exp_k in self._expected_keys:
                if not isinstance(score[exp_k['name']], exp_k['type']):
                    raise TypeError()
        self.score_selection = score_selection

    def get_sklearn_dict(self):
        """Returns a dict of scores as expected by sklearn.BaseSearchCV
        scoring parameter
        """
        sklearn_score_dict = {}
        for score in self.score_selection:
            sklearn_score_dict[score['score_name']] = score['scorer']

        return sklearn_score_dict
