# write your code for 3.3 (optional) here


# Using pandas and tabulate to print a pretty truth table
import pandas as pd
from tabulate import tabulate


# Unless proven that the conclusion is False when the premises are True, an argument is valid.

# Initializing validity to use at a global scope (accessible by all functions)
validity = True


# Function to convert written statements into arguments

def getArguments():
    
    # Fixing the number of statements
    n = int(input("Enter the number of statements in the argument (including conclusion): "))

    # Notes to remember while writing the statements
    
    print("Statements should be such that the variables used should not be replaced by other versions \
like capitalization or change in form. INCLUDE BRACKETS FOR PARTS OF THE STATEMENT THAT NEED TO BE EVALUATED \
BEFORE AN OPERATOR WHICH IS PLACED PRECEDING IT. GIVE 'SPACES' BETWEEN EACH OF THE OPERATORS AND VARIABLES. \
Words to be used for each logical sentence include: ")

    # Signs to be used for writing down the statements:

    print("Negation: 'not'")
    print("Conjunction: 'and'")
    print("Disjunction: 'or'")
    print("Exclusive disjunction: 'xor'")
    print("NAND: 'nand'")
    print("Implication/conditional: 'implies', 'conditional'")
    print("Biconditional: 'biconditional', 'biimplies'")
    print("Equality: '=='")
    print("Inequality: '!='\n")

    
    # Declaring arg as the list containing the argument
    arg = []

    
    # Input all statements
    for i in range(n-1):
        arg.append(input("Enter Premise " + str(i+1) +": "))

    arg.append(input("\nEnter the conclusion: "))

    
    # Variable to store all statements in a form that can be executed
    args = []

    for i in range(n):
        # Converting the string into a list to form executable statements
        elements = arg[i].split()

        temp = []
        j = 0
        while j<len(elements):
            
            #Using a function to switch to python-friendly executable statements for the following:
            if elements[j] == 'xor' or elements[j] == 'nand' or elements[j] == 'implies'\
            or elements[j] == 'conditional' or elements[j] == 'biconditional'\
            or elements[j] == 'biimplies':

                # Removing the last element to replace the entire new code block
                temp.pop()
                
                # Using {(('l[' + str(-(97-ord(elements[j-1]))) + ']')} to convert every letter variable to
                # element of a list starting with a as l[0]
                
                # Using the returnStatement function to get a string for the operators
                temp.append(returnStatement(('l[' + str(-(97-ord(elements[j-1]))) + ']'), ('l['\
+ str(-(97-ord(elements[j+1]))) + ']'), elements[j]))
                
                # Skipping 2 as the surrounding variables are already considered
                j+=2

            elif len(elements[j]) == 1:
                ASCII = ord(elements[j])
                
                # Finding the ASCII value to check if it is a letter
                
                if ASCII>=97 and ASCII<=122:
                    
                    # Using {('l[' + str(-(97-ASCII)) + ']')} to convert every letter variable to
                    # element of a list starting with a as l[0]
                    
                    temp.append('l[' + str(-(97-ASCII)) + ']')
                    j+=1
                
                else:
                    # Just adding the operators if they do not meet the guidelines (eg, '(' and ')')
                    temp.append(elements[j])
                    j+=1
                    
            else:
                # Adding all other operators as is, eg 'and', 'or', 'not', etc.
                temp.append(elements[j])
                j+=1

                
        # Converting the list intostring by using .join()
        tempstr = ' '
        tempstr = tempstr.join(temp)
        
        # Adding the string to the executable list 'args'
        args.append(tempstr)
        
    # Returning the two lists to main for creating truth table
    return (args, arg)
    

def returnStatement(a,b,operator):
    if operator == 'xor':
        # a XOR b = (a and b) == (a or b)
        return '(' + a + ' and ' + b + ') == (' + a + ' or ' + b + ')'
    elif operator == 'nand':
        # a NAND b = (not (a and b))
        return '(not (' + a + ' and ' + b + '))'
    elif operator == 'implies' or operator == 'conditional':
        # a --> b = not a or b
        return '(not '+ a + ' or ' +  b + ')'
    elif operator == 'biconditional' or operator == 'biimplies':
        # a <--> b = (a == b)
        return '(' + a + ' == ' + b + ')'

# Main() function to control the flow of accessing each function
def main():
    
    
    # Obtaining args (original argument) and arg (executable arguments) from getArguments()
    (args, arg) = getArguments()
    
    # Input the number of variables used
    num = int(input("\nEnter the total number of variables (less than or equal to 26 and more than or equal to one): "))
    
    # The program currently only supports up to 26 variables
    if num<1 or num>26:
        raise ValueError('Error in value entered!')
    
    # Calling createTT() to create the Truth Table and check validity
    createTT(num, args, arg)

def createTT(num,args,arg):
    
    # Making the global vairable 'validity' accessible in this function
    global validity
    
    # Creating temp and filling it in with the variable names and arguments as the column names for DataFrame
    temp = []
    
    for i in range(97,97+num):
        temp.append(chr(i))
    
    for element in arg:
        temp.append(element)
        
        
    # Creating empty DataFrame with the temp as list of column names to store the variables
    df = pd.DataFrame(columns = temp)
    
    # Initializing a list 'l' to store True or False as values of the variables
    # Using list comprehension such that l[0] == l[num-1] == True
    l = [True for i in range(num)]
    
    ## Calling recursiveTT() which will go through all variables and create the truth table
    
    recursiveTT(0, num, args, l, df)
    
    # Printing the truth table in the df (DataFrame) in a pretty fashion
    print(tabulate(df, headers='keys', tablefmt='psql'))
    
    
    # Making a statement based on the validity of the argument
    ValidityStr = 'The argument is '
    if validity == True:
        ValidityStr += 'valid!'
    else:
        ValidityStr += 'invalid!'

    # Printing the validity
    print(ValidityStr)


## Function to not print, but add rows to df (DataFrame) to be printed later
def printTT(num, args, l, df):
    
    # Creating a list with each variable and evaluation of each statement
    temp = []
    
    # Assuming all premises are True, checking that inside the loop
    flag = True
    
    # Adding the values in each variable to temp
    for j in range(num):
        temp.append(l[j])
    
    # Adding the evaluated values for each premise
    for j in range(len(args)-1):
        temp.append(eval(args[j]))    #eval() evaluates the value in a string as if it was directly listed for evaluation
        
        # Checking if all premises are True
        if flag == True:                  # If all until now are True
            if eval(args[j]) == False:    # and the current is False
                flag = False              # then the premises are not True
                
    # Adding the evaluation of conclusion to the list
    temp.append(eval(args[-1]))
    
## An argument is invalid if and only if in at least 1 scenario, the premises are all True while conclusion is False.
    
    # Assuming this instance is valid
    result = True
    
    if eval(args[num-1])==False:    # If conclusion is False,
        if flag == True:            # and the premises are True;
            result = False          # the argument is Invalid.
    
    # Adding temp as a new row if df (DataFrame)
    df.loc[len(df)] = temp
    
    # Return the validity assessment from this scenario
    return result
        
    
## Recursive function (calls itself) to go through all possibilities for each statement in the argument

def recursiveTT(count, num, args, l, df):
    # Counting up to num-1 where the first evaluation would happen
    if count<num:
        for l[count] in [True,False]:
            # Recursion - calling the function itself
            recursiveTT(count+1, num, args, l, df)
    
    # If the values have gone through every statement, add the new row of truth table to the df using printTT()
    else:
        # Making the global variable validity accessible in this function
        global validity
        
        # Calling printTT() to add the new row to df (DataFrame) to print it later. Receiving the value
        # 'result', which is the validity determined for the given row.
        result = printTT(num, args, l, df)
        
        # If an argument is invalid, it needs just one instance to prove so. Otherise, updating the validity
        # found from the function printTT() if it is False. Else, the validity remains True.
        if validity == True and result == False:
            validity = False
    
    
# Calling the main() function when code is run

if __name__ == '__main__':
    main()
    