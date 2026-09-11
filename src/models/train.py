import os
import mlflow
import polars as pl
from src.ingestion.entsoe_client import EntsoeClient
from src.features.build_features import create_features, split_data
from src.models.baseline_lgbm import QuantileLGBM
from src.models.conformal import calibrate_conformal
from src.models.evaluate import evaluate_predictions

def main():
    print("Fetching raw data...")
    client = EntsoeClient()
    df_raw = client.get_data("2021-01-01", "2025-12-31")
    
    df_pl = pl.from_pandas(df_raw)
    
    print("Building features...")
    df_features = create_features(df_pl)
    df_features = df_features.drop_nulls()
    
    print("Splitting data...")
    train, calib, test = split_data(df_features)
    
    train_pd = train.to_pandas()
    calib_pd = calib.to_pandas()
    test_pd = test.to_pandas()
    
    target = "day_ahead_price_eur"
    drop_cols = [target, "timestamp", "bidding_zone"]
    features = [c for c in train_pd.columns if c not in drop_cols]
    
    X_train, y_train = train_pd[features], train_pd[target]
    X_calib, y_calib = calib_pd[features], calib_pd[target]
    X_test, y_test = test_pd[features], test_pd[target]
    
    # MLflow config (defaulting to local mlruns if docker server is down)
    try:
        import requests
        requests.get("http://localhost:5000")
        mlflow.set_tracking_uri("http://localhost:5000")
    except:
        print("Warning: MLflow server at http://localhost:5000 is unreachable. Defaulting to local sqlite:///mlflow.db directory.")
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        
    mlflow.set_experiment("ecogrid-cast-quantile")
    
    with mlflow.start_run():
        print("Training QuantileLGBM...")
        model = QuantileLGBM(quantiles=[0.05, 0.50, 0.95], n_estimators=100)
        model.fit(X_train, y_train)
        
        print("Calibrating Conformal Prediction with MAPIE...")
        mapie = calibrate_conformal(model, X_calib, y_calib, alpha=0.1)
        
        print("Evaluating on Test Set...")
        y_pred, y_pis = mapie.predict_interval(X_test)
        
        # y_pis has shape (N, 2, 1) for a single alpha value
        y_pred_05 = y_pis[:, 0, 0]
        y_pred_50 = y_pred
        y_pred_95 = y_pis[:, 1, 0]
        
        evaluate_predictions(y_test.values, y_pred_05, y_pred_50, y_pred_95)
        
        print("Training cycle complete.")

if __name__ == "__main__":
    main()
