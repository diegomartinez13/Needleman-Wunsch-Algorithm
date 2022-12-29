from fileinput import close
from sys import argv
from typing import List
import csv

def ScoringMatrix(A:str,B:str):
    '''Function that will return a value (1 or -1) depending if the letters passed match or not.
    
    Args:
        A (str): Letter from the stringA
        B (str): Letter from the stringB

    Returns:
        1 (int): A and B match
        -1 (int): A and B don't match
    '''
    if A == B: return 1
    else: return -1

def Backtracking(F:List[List[int]], stringA:str, stringB:str, d:int):
    '''Function that will do a backtrack on the matrix that we passed as argument and will return the optimal alignment of the two strings.
    
    Args:
        F ( List[List[int]] ): Matrix of size m,n where we will do our backtracking.
        stringA (str): First string in line read from the csv file.
        stringB (str): Second string in line read from the csv file.
        d (int): gap_penalty value. 
    
    Returns: 
        str: The correct alignment with the format "Alignment1 Alignment2" 
                + the value of the starting tile.
                Format: "{alignment1} {alignment2} {value_starting_tile}"
    '''
    
    Alignment1 = ""
    Alignment2 = ""
    
    i = abs(len(stringB))
    j = abs(len(stringA))
    
    while i > 0 and j > 0:
        
        #Backtracking using the largest score between the top, left or diagonal(top,left) value from the current value while bath is not on edge.
        current = F[j][i]
        score_diagonal= F[j-1][i-1] + ScoringMatrix(stringA[j-1],stringB[i-1])
        score_top = F[j-1][i] + d
        score_left = F[j][i-1] + d

        #Storing optimal alignment in a variable for conciseness
        optimal_alignment = max(score_diagonal,score_left,score_top)
        
        #Depending on the value of optimal_aligment, the corrisponding alignment will be added to the variables Alignment1 & Alignment2.
        if optimal_alignment == score_left:
            Alignment1 = "-" + Alignment1
            Alignment2 = stringB[i-1] + Alignment2
            i -= 1
            
        elif optimal_alignment == score_top:
            Alignment1 = stringA[j-1] + Alignment1
            Alignment2 = "-" + Alignment2
            j -= 1
            
        else:
            Alignment1 = stringA[j-1] + Alignment1
            Alignment2 = stringB[i-1] + Alignment2
            i -= 1
            j -= 1
            
    while j > 0:
        #Backtracking to the top when path has reached the left of the matrix until reaches the top left position in matrix.
        Alignment1 = stringA[j-1] + Alignment1
        Alignment2 = "-" + Alignment2
        j -= 1
    
    while i > 0:
        #Backtracking to the left when path has reached the top of the matrix until reaches the top left position in matrix.
        Alignment1 = "-" + Alignment1
        Alignment2 = stringB[i-1] + Alignment2
        i -= 1
    
    return f"{Alignment1} {Alignment2} {F[abs(len(stringA))][abs(len(stringB))]}"

def NeedlemanWunsh(stringA:str, stringB:str):
    """Function that will create the matrix, and call the backtracking fuction in order to solve the alignment.

    Args:
        stringA (str): First string in line read from the csv file.
        stringB (str): Second string in line read from the csv file.

    Returns:
        str:  The alignment of the two strings of every line of the csv
    """
    width = abs(len(stringB))+1
    height = abs(len(stringA))+1

    gap_penalty = -2

    #Creation of a matrix with all values equal to 0
    matrix = [ [0 for _ in range(0,width)] for _ in range(0,height) ]
    
    #Matrix Initialitation:
    for row in range(0,height):
        matrix[row][0] = gap_penalty * row
        
    for col in range(0,width):
        matrix[0][col] = gap_penalty * col

    #FillingProcess:
    for j in range(1,height):
        for i in range(1,width):
            case1 = matrix[j-1][i-1] + ScoringMatrix(stringA[j-1],stringB[i-1])
            
            case2 = matrix[j][i-1] + gap_penalty
            
            case3 = matrix[j-1][i] + gap_penalty
            
            #Equation used to fill the matrix:
            matrix[j][i] = max( case1, case2, case3 )
            
    
    #Printing the alignment:
    print(Backtracking(matrix, stringA, stringB, gap_penalty))


if __name__ == '__main__':
    #Checking if arguments where passed
    if len(argv) > 1:
        
        #Saving file that was passed through the commandline in a variable
        argvfile = argv[1]
        
        # argvfile = "test1.csv" ---------- Test case made by me.
        
        with open(argvfile, 'r') as csvfile:
            
            #Creation of file reader 
            csvreader = csv.reader(csvfile)
            
            for row in csvreader:
                #Saving sequences 
                sequence1,sequence2 = row[0],row[1]
                
                #Checking if the row has the heathers/titles
                if sequence1 == "sequence1" or sequence2 == "sequence2":
                    continue
                
                #Calling function that will solve the alignment
                else: 
                    NeedlemanWunsh(sequence1,sequence2)
        