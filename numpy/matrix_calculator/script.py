import numpy as np

def getInput(name="matrix"):
    print("Enter values. Note: sperated by spaces")
    rows = int(input("Enter row: "))
    col = int(input("Enter column: "))
    print(f"Enter {rows} rows: ")
    data=[]

    for i in range(rows):
        r=list(map(float, input().strip().split()))
        if len(r)!=col:
            print("Error: Invalid row length. Try Again!!")
            return getInput(name)
        data.append(r)
    return np.array(data)

def menu():
    print("\nMatrix Calculator")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    print("4. Transpose a Matrix")
    print("5. Determinant")
    print("6. Inverse")
    print("0. Exit")

def main():
    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            A = getInput("Matrix A")
            B = getInput("Matrix B")

            if A.shape != B.shape:
                print("Error: Matrices must have the same dimensions to add.")
            else:
                print("Result:\n", A + B)
        elif choice == "2":
            A = getInput("Matrix A")
            B = getInput("Matrix B")
            if A.shape != B.shape:
                print("Error: Matrices must have the same dimensions to subtract.")
            else:
                print("Result:\n", A - B)

        elif choice == "3":
            A = getInput("Matrix A")
            B = getInput("Matrix B")
            if A.shape[1] != B.shape[0]:
                print("Error: Columns of A must equal rows of B to multiply.")
            else:
                print("Result:\n", A @ B)

        elif choice == "4":
            A = getInput("Matrix")
            print("Transpose:\n", A.T)
        
        elif choice == "5":
            A = getInput("Matrix A")
            if A.shape[0] != A.shape[1]:
                print("Error: Must be a square matrix.")
            else:
                det = np.linalg.det(A)
                print("Determinant:", det)
        elif choice == "6":
            A = getInput("Square Matrix")
            if A.shape[0] != A.shape[1]:
                print("Error: Must be a square matrix.")
            else:
                try:
                    inv = np.linalg.inv(A)
                    print("Inverse:\n", inv)
                except np.linalg.LinAlgError:
                    print("Matrix is not invertible (singular).")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again")


if __name__ == "__main__":
    main()