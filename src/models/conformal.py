from mapie.regression import ConformalizedQuantileRegressor

def calibrate_conformal(model, X_calib, y_calib, alpha=0.1):
    estimators = model.get_estimators()
    mapie = ConformalizedQuantileRegressor(
        estimator=estimators,
        confidence_level=1 - alpha,
        prefit=True
    )
    mapie.conformalize(X_calib, y_calib)
    return mapie
