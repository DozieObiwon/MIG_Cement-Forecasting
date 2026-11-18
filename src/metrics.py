import numpy as np
from sklearn.metrics import mean_squared_error

def print_metrics(y_true, y_pred, label):
    mask = y_true != 0  # Create a mask to filter out zero values in the true values
    mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100      # Calculate Mean Absolute Percentage Error (MAPE)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))         # Calculate Root Mean Squared Error (RMSE)
    print(f"{label} - MAPE: {mape:.2f}%, RMSE: {rmse:.2f} tonnes") 