import lightgbm as lgb
import numpy as np

class QuantileLGBM:
    """
    A wrapper to train multiple LightGBM models for specified quantiles.
    """
    def __init__(self, quantiles=[0.05, 0.50, 0.95], **kwargs):
        self.quantiles = quantiles
        self.models = {}
        for q in quantiles:
            self.models[q] = lgb.LGBMRegressor(
                objective='quantile',
                alpha=q,
                metric='quantile',
                **kwargs
            )

    def fit(self, X, y):
        for q in self.quantiles:
            self.models[q].fit(X, y)
        return self

    def predict(self, X):
        """
        Returns predictions in the format expected by MAPIE with cv='prefit'.
        Shape: (n_samples, len(quantiles)), usually [lower_bound, median, upper_bound]
        """
        preds = []
        for q in self.quantiles:
            preds.append(self.models[q].predict(X))
        return np.column_stack(preds)

    def get_estimators(self):
        return [self.models[q] for q in self.quantiles]
