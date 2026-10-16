import pathlib
import math

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []
    
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            # Separ partea stanga de partea dreapta a ecuatiei
            left_side, right_side = line.split('=')
            
            # B este partea dreapta a ecuatiei
            B.append(float(right_side.replace(' ', '')))
            
            # "2x + 3y - z" devine "2x +3y -z" pentru a elimina spatiile
            left_side = left_side.replace('+ ', '+').replace('- ', '-')
            
            # fac o lista in care retin fiecare termen al ecuatiei [2x, +3y, -z]
            tokens = left_side.split()
            
            row = []
            for token in tokens:
                # Elimin litera variabilei pt a obtine coeficientul
                coef_str = token[:-1] 
                
                if coef_str == '' or coef_str == '+':
                    row.append(1.0)
                elif coef_str == '-':
                    row.append(-1.0)
                else:
                    row.append(float(coef_str))
            
            A.append(row)
            
    return A, B

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} \n{B=}")

def determinant(matrix: list[list[float]]) -> float:
    n = len(matrix)
    
    if n == 1:
        return matrix[0][0]
    
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    if n == 3:
        term1 = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        term2 = matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        term3 = matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
        return term1 - term2 + term3

print(f"{determinant(A)=}")

def trace(matrix: list[list[float]]) -> float:
    return matrix[0][0] + matrix[1][1] + matrix[2][2]

print(f"{trace(A)=}")

def norm(vector: list[float]) -> float:
    return math.sqrt(sum(x**2 for x in vector))

print(f"{norm(B)=}")

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

print(f"{transpose(A)=}")

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    result = []
    
    for i in range(len(matrix)):
        row_sum = 0
        for j in range(len(vector)):
            row_sum += matrix[i][j] * vector[j]
        result.append(row_sum)
        
    return result

print(f"{multiply(A, B)=}")

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    
    if det_A == 0:
        raise ValueError("Determinantul este zero, sistemul nu are solutie unica.")
    
    Ax = [list(row) for row in matrix]
    Ay = [list(row) for row in matrix]
    Az = [list(row) for row in matrix]
    
    for i in range(len(matrix)):
        Ax[i][0] = vector[i]
        Ay[i][1] = vector[i]
        Az[i][2] = vector[i]
        
    x = determinant(Ax) / det_A
    y = determinant(Ay) / det_A
    z = determinant(Az) / det_A
    
    return [x, y, z]

print(f"{solve_cramer(A, B)=}")

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    M = []
    for row in range(len(matrix)):
        if row != i:
            M.append([matrix[row][col] for col in range(len(matrix[row])) if col != j])
    return M

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cof_mat = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix)):
            minor_ij = minor(matrix, i, j)
            val = ((-1) ** (i + j)) * determinant(minor_ij)
            row.append(val)
        cof_mat.append(row)
    return cof_mat

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    
    if det_A == 0:
        raise ValueError("Determinantul este zero, sistemul nu are solutie unica.")
    
    adj_A = adjoint(matrix)
    
    inv_A = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix)):
            row.append(adj_A[i][j] / det_A)
        inv_A.append(row)
        
    return multiply(inv_A, vector)

print(f"{solve(A, B)=}")