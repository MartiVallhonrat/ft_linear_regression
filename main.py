import pandas as pd
import matplotlib.pyplot as plt

from train import trainModel
from r_squared import rSquare

def getEstPrice(theta0, theta1, estimatePrice):
    try:
        mileage = int(input("PLEASE ENTER THE MILEAGE: "))
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(f"\n---> ERROR: {e} <---")
        return
    
    estimated_price = estimatePrice(theta0, theta1, mileage)

    marker = plt.plot(mileage, estimated_price, marker="o", color="red")[0]
    text = plt.text(mileage, estimated_price, f"Estimated Price({mileage}, {estimated_price})", color="red")
    plt.savefig("plot.png")
    marker.remove()
    text.remove()

def drawDataset(df):
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1], marker="o", color="blue")
    plt.savefig("plot.png")

def drawRegression(theta0, theta1, r_squared):
    plt.axline(xy1=(0, theta0), slope=theta1, color="green", label=f"Linear Regression (R^2={r_squared:.2f})")
    plt.legend()
    plt.savefig("plot.png")
    
    
def main():
    plt.title("Car Price-Mileage")
    plt.grid("True")
    plt.ylabel("Price(euros)")
    plt.xlabel("Mileage(km)")
    plt.savefig("plot.png")

    program_input = ""
    estimatePrice = lambda theta0, theta1, mileage: theta0 + theta1 * mileage
    theta0 = 0
    theta1 = 0

    print("WELCOME TO FT_LINEAR_REGRESSION!")
    while program_input != "EXIT":
        
        try:
            program_input = input("\nWHAT CAN I DO FOR YOU?:\n\t- ESTIMATE CAR PRICE (ESTIM)\n\t- TRAIN MODEL (TRAIN)\n\t- RESTART COEFFICIENTS (REST)\n\t- EXIT PROGRAM (EXIT)\n\n- ")
        except KeyboardInterrupt:
            break
        except Exception:
            break

        if program_input == "ESTIM":
            getEstPrice(theta0, theta1, estimatePrice)
        elif program_input == "TRAIN":
            try:
                df = pd.read_csv('data.csv')
            except Exception as e:
                print(f"\n---> ERROR: {e} <---")
                continue
            
            drawDataset(df)
            try:
                theta = trainModel(df, theta0, theta1, estimatePrice)
            except KeyboardInterrupt:
                continue
            except Exception as e:
                print(f"\n---> ERROR: {e} <---")
                continue
            theta0 = theta[0]
            theta1 = theta[1]
            drawRegression(theta0, theta1, rSquare(df, theta0, theta1, estimatePrice))
        elif program_input == "REST":
            theta0 = 0
            theta1 = 0
    
    print("\nGOODBYE!")
            

        

if __name__ == '__main__':
    main()