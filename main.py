import pandas as pd
import matplotlib.pyplot as plt

def estimatedPrice(theta0, theta1, estimatePrice):
    try:
        milage = int(input("PLEASE ENTER THE MILAGE: "))
    except EOFError:
        return
    except KeyboardInterrupt:
        return
    except ValueError as e:
        print(f"\n---> ERROR: {e} <---")
        return
    
    estimated_price = estimatePrice(theta0, theta1, milage)

    marker = plt.plot(milage, estimated_price, marker="o", color="red")[0]
    text = plt.text(milage, estimated_price, f"Estimated Price({milage}, {estimated_price})", color="red")
    plt.savefig("plot.png")
    marker.remove()
    text.remove()

def drawDataset(theta0, theta1, estimatePrice):
    try:
        df = pd.read_csv('data.csv')
    except FileNotFoundError as e:
        print(f"\n---> ERROR: {e} <---")
        return(1)

    plt.scatter(df["km"], df["price"], marker="o", color="blue")

    trainModel(df, theta0, theta1, estimatePrice)

    plt.savefig("plot.png")

    return(0)

def trainModel(df, theta0, theta1, estimatePrice):
    # MAX NUMBER OF STEPS 1000 OR if step size is < than 0,001 (we consider is almost exact)
    learning_rate = 0.01
    stepsize_theta0 = 1
    stepsize_theta1 = 1
    for i in range(1):
        if (abs(stepsize_theta0) > 0.001):
            sum = 0
            for row in df.itertuples():
                sum += estimatePrice(theta0, theta1, row.km) - row.price
                #print("estimatePrice(theta0, theta1, row.km):", estimatePrice(theta0, theta1, row.km), "- row.price:", row.price)
            stepsize_theta0 = learning_rate * (1/df.shape[0]) * sum
            print("sum:", sum)
            #print("stepsize_theta0:", stepsize_theta0)
            theta0 = theta0 - stepsize_theta0
        if (abs(stepsize_theta1) > 0.001):
            sum = 0
            for row in df.itertuples():
                sum += (estimatePrice(theta0, theta1, row.km) - row.price) * row.km
            stepsize_theta1 = learning_rate * (1/df.shape[0]) * sum
            print("sum:", sum)
            #print("stepsize_theta1:", stepsize_theta1)
            theta1 = theta1 - stepsize_theta1
        if (abs(stepsize_theta0) < 0.001 and abs(stepsize_theta1) < 0.001):
            break

    print("theta0:", theta0, "theta1:", theta1)    
    plt.axline(xy1=(0, theta0), slope=theta1, color="green", label="Linear Regression")
    plt.legend()
    print("TRAINING MODEL...")
    
def main():
    plt.title("Car Price-Milage Correlation")
    plt.grid("True")
    plt.ylabel("Price")
    plt.xlabel("Milage")
    plt.savefig("plot.png")

    program_input = ""
    estimatePrice = lambda theta0, theta1, milage: theta0 + theta1 * milage
    theta0 = 0
    theta1 = 0

    print("WELCOME TO FT_LINEAR_REGRESSION!")
    while program_input != "EXIT":
        
        try:
            program_input = input("\nWHAT CAN I DO FOR YOU?:\n\t- ESTIMATE CAR PRICE (ESTIMATE)\n\t- TRAIN MODEL (TRAIN)\n\t- EXIT PROGRAM (EXIT)\n\n- ")
        except KeyboardInterrupt:
            break
        except EOFError:
            break

        if program_input == "ESTIMATE":
            estimatedPrice(theta0, theta1, estimatePrice)
        elif program_input == "TRAIN":
            if (drawDataset(theta0, theta1, estimatePrice) > 0):
                continue
    
    print("\nGOODBYE!")
            

        

if __name__ == '__main__':
    main()