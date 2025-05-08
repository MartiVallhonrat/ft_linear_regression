import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

def standarizeDataset(df):
	std_df = df.copy(deep=True)
	for key, value in df.items():
		mean = value.mean()
		std_var = value.std()
		std_df[key] = (value - mean) / std_var
	
	return (std_df)

def batchGD(df, theta0, theta1, estimatePrice):
	learning_rate = 0.1
	epsilon = 0.001

	# MAX NUMBER OF STEPS 1000 OR if step size is < than 0,001 (we consider is almost exact)
	for i in range(1000):
		sum = 0
		for row in df.itertuples():
			sum += estimatePrice(theta0, theta1, row.km) - row.price
		stepsize_theta0 = learning_rate * (1/df.shape[0]) * sum
		
		sum = 0
		for row in df.itertuples():
			sum += (estimatePrice(theta0, theta1, row.km) - row.price) * row.km
		stepsize_theta1 = learning_rate * (1/df.shape[0]) * sum
		
		theta0 = theta0 - stepsize_theta0
		theta1 = theta1 - stepsize_theta1
	
		if abs(stepsize_theta0) < epsilon and abs(stepsize_theta1) < epsilon:
			break

	return(theta0, theta1)

def stochasticGD(df, theta0, theta1, estimatePrice):
	learning_rate = 0.1
	epsilon = 0.00001

	# MAX NUMBER OF STEPS 1000 OR if step size is < than 0,001 (we consider is almost exact)
	for i in range(1000):
		rand_idx = np.random.randint(0, df.shape[0])
		row = df.iloc[rand_idx]

		sum = estimatePrice(theta0, theta1, row.iloc[0]) - row.iloc[1]
		stepsize_theta0 = learning_rate * sum
		
		sum = (estimatePrice(theta0, theta1, row.iloc[0]) - row.iloc[1]) * row.iloc[0]
		stepsize_theta1 = learning_rate * sum
		
		theta0 = theta0 - stepsize_theta0
		theta1 = theta1 - stepsize_theta1
	
		if abs(stepsize_theta0) < epsilon and abs(stepsize_theta1) < epsilon:
			break

	return(theta0, theta1)

def minibatchGD(df, theta0, theta1, estimatePrice):
	learning_rate = 0.1
	epsilon = 0.00001
	batch_size = 4

	# MAX NUMBER OF STEPS 1000 OR if step size is < than 0,001 (we consider is almost exact)
	for i in range(1000):
		batch_idxs = np.random.choice(df.shape[0], batch_size, replace=False)
		minibatch = df.iloc[batch_idxs]

		sum = 0
		for row in minibatch.itertuples():
			sum += estimatePrice(theta0, theta1, row.km) - row.price
		stepsize_theta0 = learning_rate * (1/minibatch.shape[0]) * sum
		
		sum = 0
		for row in minibatch.itertuples():
			sum += (estimatePrice(theta0, theta1, row.km) - row.price) * row.km
		stepsize_theta1 = learning_rate * (1/minibatch.shape[0]) * sum
		
		theta0 = theta0 - stepsize_theta0
		theta1 = theta1 - stepsize_theta1
	
		if abs(stepsize_theta0) < epsilon and abs(stepsize_theta1) < epsilon:
			break

	return(theta0, theta1)

def trainModel(df, theta0, theta1, estimatePrice):
	program_input = input("\nWHAT ALGORITHM DO YOU WANT TO USE?:\n\t- BATCH GRADIENT DESCENT (BGD)\n\t- STOCHASTIC GRADIENT DESCENT (SGD)\n\t- MINI-BATCH GRADIENT DESCENT (MBGD)\n\n- ")
	unstandarizeTheta1 = lambda std_theta1: std_theta1 * (df.iloc[:, 1].std() / df.iloc[:, 0].std())
	unstandarizeTheta0 = lambda unstd_theta1: df.iloc[:, 1].mean() - unstd_theta1 * df.iloc[:, 0].mean()

	start = time.time()
	if program_input == "BGD":
		std_df = standarizeDataset(df)
		theta0, theta1 = 0, 0
		theta = batchGD(std_df, theta0, theta1, estimatePrice)
		# REVERSING THE STANDARIZATION FOR THE COEFFICIENTS
		theta1 = unstandarizeTheta1(theta[1])
		theta0 = unstandarizeTheta0(theta1)
	elif program_input == "SGD":
		std_df = standarizeDataset(df)
		theta0, theta1 = 0, 0
		theta = stochasticGD(std_df, theta0, theta1, estimatePrice)
		# REVERSING THE STANDARIZATION FOR THE COEFFICIENTS
		theta1 = unstandarizeTheta1(theta[1])
		theta0 = unstandarizeTheta0(theta1)
	elif program_input == "MBGD":
		std_df = standarizeDataset(df)
		theta0, theta1 = 0, 0
		theta = minibatchGD(std_df, theta0, theta1, estimatePrice)
		# REVERSING THE STANDARIZATION FOR THE COEFFICIENTS
		theta1 = unstandarizeTheta1(theta[1])
		theta0 = unstandarizeTheta0(theta1)
	else:
		raise Exception("Please select an available algorithm")
	end = time.time()
	print(f"ALGORITHM TIME OF {program_input}: ", (end - start) * 1000, "ms")
	return (theta0, theta1)


