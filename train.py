import pandas as pd
import matplotlib.pyplot as plt

def standarizeDataset(df):
    std_df = df.copy(deep=True)
    for key, value in df.items():
        mean = value.mean()
        std_var = value.std()
        std_df[key] = (value - mean) / std_var
    
    return (std_df)

def trainModel(df, theta0, theta1, estimatePrice):
    # MAX NUMBER OF STEPS 1000 OR if step size is < than 0,001 (we consider is almost exact)
    learning_rate = 0.001
    epsilon = 0.001
    reverseStd = lambda std_value, mean, std_var: std_value * std_var + mean

    #theta0 = (theta0 - df.iloc[:, 1].mean()) / df.iloc[:, 1].std()
    #theta1 = (theta1 - df.iloc[:, 0].mean()) / df.iloc[:, 0].std()
    std_df = standarizeDataset(df)
    for i in range(1000):
        sum = 0
        for row in std_df.itertuples():
            sum += estimatePrice(theta0, theta1, row.km) - row.price
            #print("estimatePrice(theta0, theta1, row.km):", estimatePrice(theta0, theta1, row.km), "- row.price:", row.price, "sum:", sum)
        stepsize_theta0 = learning_rate * (1/std_df.shape[0]) * sum
        print("sum:", sum)
        print("stepsize_theta0:", stepsize_theta0)
        
        sum = 0
        for row in std_df.itertuples():
            sum += (estimatePrice(theta0, theta1, row.km) - row.price) * row.km
        stepsize_theta1 = learning_rate * (1/std_df.shape[0]) * sum
        print("sum:", sum)
        print("stepsize_theta1:", stepsize_theta1)
        
        theta0 = theta0 - stepsize_theta0
        theta1 = theta1 - stepsize_theta1
        
        print("theta0:", theta0, "theta1:", theta1)
        if abs(stepsize_theta0) < epsilon and abs(stepsize_theta1) < epsilon:
            break

    #print(theta0, theta1)
    print(reverseStd(theta0, df.iloc[:, 1].mean(), df.iloc[:, 1].std()), reverseStd(theta1, df.iloc[:, 0].mean(), df.iloc[:, 0].std()))    
    return(reverseStd(theta0, df.iloc[:, 1].mean(), df.iloc[:, 1].std())), reverseStd(theta1, df.iloc[:, 0].mean(), df.iloc[:, 0].std())

