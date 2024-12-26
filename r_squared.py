import pandas as pd
import matplotlib.pyplot as plt

def rSquare(df, theta0, theta1, estimatePrice):
    
    sum_line = 0
    for row in df.itertuples():
        sum_line += (row.price - estimatePrice(theta0, theta1, row.km)) ** 2
    sum_mean = 0
    y_mean = df.iloc[:, 1].mean()
    for row in df.itertuples():
        sum_mean += (row.price - y_mean) ** 2

    # WE SUBTRACT THE ERROR TO THE 100%
    r_squared = 1 - (sum_line / sum_mean)

    return (r_squared)