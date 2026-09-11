import numpy as np
import mlflow

def pinball_loss(y_true, y_pred, alpha):
    error = y_true - y_pred
    return np.maximum(alpha * error, (alpha - 1) * error).mean()

def evaluate_predictions(y_true, y_pred_05, y_pred_50, y_pred_95):
    pb_05 = pinball_loss(y_true, y_pred_05, 0.05)
    pb_50 = pinball_loss(y_true, y_pred_50, 0.50)
    pb_95 = pinball_loss(y_true, y_pred_95, 0.95)
    mean_pb = (pb_05 + pb_50 + pb_95) / 3.0
    
    # Winkler Score for 90% interval (alpha=0.1)
    alpha = 0.1
    delta = y_pred_95 - y_pred_05
    winkler = np.where(
        y_true < y_pred_05, delta + 2/alpha * (y_pred_05 - y_true),
        np.where(
            y_true > y_pred_95, delta + 2/alpha * (y_true - y_pred_95),
            delta
        )
    ).mean()
    
    # PICP (Prediction Interval Coverage Probability)
    covered = (y_true >= y_pred_05) & (y_true <= y_pred_95)
    picp = covered.mean() * 100
    
    metrics = {
        "pinball_loss_mean": mean_pb,
        "pinball_0.05": pb_05,
        "pinball_0.50": pb_50,
        "pinball_0.95": pb_95,
        "winkler_score": winkler,
        "picp_percentage": picp
    }
    
    for k, v in metrics.items():
        mlflow.log_metric(k, v)
        print(f"{k}: {v:.4f}")
        
    return metrics
