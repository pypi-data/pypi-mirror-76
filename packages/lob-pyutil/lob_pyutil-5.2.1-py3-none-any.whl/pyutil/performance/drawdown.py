import pandas as pd


# The drawdown is based on a return time series! In particular the drawdown on the first day can be positive
# if the series starts with a negative return
def drawdown(series) -> pd.Series:
    """
    Compute the drawdown for a nav series. The drawdown is defined as 1 - price/highwatermark.
    The highwatermark at time t is the highest price that has been achieved before or at time t.

    Args:
        series:

    Returns: Drawdown as a pandas series
    """
    return Drawdown(series).drawdown


class Drawdown(object):
    def __init__(self, nav: pd.Series, eps: float = 0) -> object:
        """
        Drawdown for a given series
        :param nav: pandas Series
        :param eps: a day is down day if the drawdown (positive) is larger than eps
        """
        # check series is indeed a series
        assert isinstance(nav, pd.Series)
        # check that all indices are increasing
        assert nav.index.is_monotonic_increasing
        # make sure all entries non-negative
        # assert not (series < 0).any()

        self.__series = nav
        #self.__series = (returns + 1.0).cumprod()

        # make sure all entries non-negative
        assert not (self.__series < 0).any()

        self.__eps = eps

    @property
    def eps(self):
        return self.__eps

    @property
    def price_series(self) -> pd.Series:
        return self.__series

    @property
    def highwatermark(self) -> pd.Series:
        x = self.price_series.expanding(min_periods=1).max()
        x[x <= 1.0] = 1.0
        return x

    @property
    def drawdown(self) -> pd.Series:
        return 1 - self.price_series / self.highwatermark
