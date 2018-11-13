import sys, operator
operations = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv
}

precedence = {'+' : 2,'-' : 2,
             '*' : 3,'/' : 3}

def doShuntingYard(tokens):
    # Djikstras Shunting Yard algorithm produces expression tree in reverse polish notation
    operators = []
    output = []
    for token in tokens:
        if token not in '+-*/()': # token is a digit
            output.append(token)
        if token in '+-*/': # token is an operator
            while len(operators) > 0 and operators[-1] != '(' and (precedence[operators[-1]] >= precedence[token]):
                output += operators.pop()
            operators.append(token)
        if token == '(':
            operators.append(token)
        if token == ')':
            while len(operators) > 0 and operators[-1] != '(':
                output += operators.pop()
            if len(operators) > 0:
                operators.pop()
    
    for op in operators:
        output += operators.pop()
    output += operators[::-1]
    return output

def buildTree(expression):
    # Start by tokenizing the expression
    tokens = ['']
    for char in expression:
        if tokens[0] == '':
            tokens[-1] += char
            continue
        if char.isdigit():
            if tokens[-1].isdigit():
                tokens[-1] += char
            else:
                tokens.append(char)
        elif char in '+-*/()':
            tokens.append(char)
    # Shunting Yard Algorithm (Djikstra)
    return doShuntingYard(tokens)

def evaluate(tree):
    # Traverse the tree (already in reverse polish notation) and evaluate
    stack = []
    i = 0
    for node in tree:
        if node in '+-*/':
            t1 = float(stack.pop())
            t2 = float(stack.pop())
            
            r = operations[node](t2,t1)
            print('step %d : Pop %d, Pop %d.' % (i, t1, t2))
            print('Compute %d %s %d. ' % (t2, node, t1))
            i += 1
            stack.append(str(r))
            print('Push %0.2f' % (r))

        else:
            print('Step %d : Push %s' % (i, node))
            stack.append(node)
        i += 1
    return stack.pop()

def display(tree):
    # Traverse Tree Depth-First (i.e. displaying in parenthetical notation)
    stack = []
    for char in tree:
        if char not in '+-*/':
            stack.append(char)
        else:
            right = stack.pop()
            left = stack.pop()

            stack.append((char, left, right))
    t = stack.pop()
    print('DISPLAYING CONSTRUCTED TREE:')
    print(t)

    
def main():
    if len(sys.argv) < 2:
        print('Error: Cannot run without input. Ex: p2.py "(3+2*6)/(8-5)"')
        print('(Be sure to put " " around the expression or bash will complain!). You can test the program with "p2.py test"')
        return
    expression = [sys.argv[1]]
    if expression[0] == 'test':
        expression = ['(3+2*6)/(8-5)', '(25*7-3)/6', '(3+2)', '4-3', '4-(3*3-5)', '36-(25+1)', '(3*3+6)*3-5', '((3*3-5)*4-10)']
    for expr in expression:
        print("INPUT EXPRESSION: %s" % (expr))
        tree = buildTree(expr)
        display(tree)
        print('-'*40)
        print("EVALUATING: %s" % (expr))
        result = evaluate(tree)
        print('COMPLETE')
        print('-'*40)
        print("EVALUATION RESULT: ")
        print('%s = %s' % (expr, result))
        print('*'*40)
        print('\n\n\n')

if __name__ == "__main__":
    main()

##############################################
############### SAMPLE OUTPUT ################
##############################################

# >>python p2.py test
# INPUT EXPRESSION: (3+2*6)/(8-5)
# DISPLAYING CONSTRUCTED TREE:
# ('/', ('+', '3', ('*', '2', '6')), ('-', '8', '5'))
# ----------------------------------------
# EVALUATING: (3+2*6)/(8-5)
# Step 0 : Push 3
# Step 1 : Push 2
# Step 2 : Push 6
# step 3 : Pop 6, Pop 2.
# Compute 2 * 6. 
# Push 12.00
# step 5 : Pop 12, Pop 3.
# Compute 3 + 12. 
# Push 15.00
# Step 7 : Push 8
# Step 8 : Push 5
# step 9 : Pop 5, Pop 8.
# Compute 8 - 5. 
# Push 3.00
# step 11 : Pop 3, Pop 15.
# Compute 15 / 3. 
# Push 5.00
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# (3+2*6)/(8-5) = 5.0
# ****************************************




# INPUT EXPRESSION: (25*7-3)/6
# DISPLAYING CONSTRUCTED TREE:
# ('/', ('-', ('*', '25', '7'), '3'), '6')
# ----------------------------------------
# EVALUATING: (25*7-3)/6
# Step 0 : Push 25
# Step 1 : Push 7
# step 2 : Pop 7, Pop 25.
# Compute 25 * 7. 
# Push 175.00
# Step 4 : Push 3
# step 5 : Pop 3, Pop 175.
# Compute 175 - 3. 
# Push 172.00
# Step 7 : Push 6
# step 8 : Pop 6, Pop 172.
# Compute 172 / 6. 
# Push 28.67
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# (25*7-3)/6 = 28.6666666667
# ****************************************




# INPUT EXPRESSION: (3+2)
# DISPLAYING CONSTRUCTED TREE:
# ('+', '3', '2')
# ----------------------------------------
# EVALUATING: (3+2)
# Step 0 : Push 3
# Step 1 : Push 2
# step 2 : Pop 2, Pop 3.
# Compute 3 + 2. 
# Push 5.00
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# (3+2) = 5.0
# ****************************************




# INPUT EXPRESSION: 4-3
# DISPLAYING CONSTRUCTED TREE:
# ('-', '4', '3')
# ----------------------------------------
# EVALUATING: 4-3
# Step 0 : Push 4
# Step 1 : Push 3
# step 2 : Pop 3, Pop 4.
# Compute 4 - 3. 
# Push 1.00
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# 4-3 = 1.0
# ****************************************




# INPUT EXPRESSION: 4-(3*3-5)
# DISPLAYING CONSTRUCTED TREE:
# ('-', '4', ('-', ('*', '3', '3'), '5'))
# ----------------------------------------
# EVALUATING: 4-(3*3-5)
# Step 0 : Push 4
# Step 1 : Push 3
# Step 2 : Push 3
# step 3 : Pop 3, Pop 3.
# Compute 3 * 3. 
# Push 9.00
# Step 5 : Push 5
# step 6 : Pop 5, Pop 9.
# Compute 9 - 5. 
# Push 4.00
# step 8 : Pop 4, Pop 4.
# Compute 4 - 4. 
# Push 0.00
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# 4-(3*3-5) = 0.0
# ****************************************




# INPUT EXPRESSION: 36-(25+1)
# DISPLAYING CONSTRUCTED TREE:
# ('-', '36', ('+', '25', '1'))
# ----------------------------------------
# EVALUATING: 36-(25+1)
# Step 0 : Push 36
# Step 1 : Push 25
# Step 2 : Push 1
# step 3 : Pop 1, Pop 25.
# Compute 25 + 1. 
# Push 26.00
# step 5 : Pop 26, Pop 36.
# Compute 36 - 26. 
# Push 10.00
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# 36-(25+1) = 10.0
# ****************************************




# INPUT EXPRESSION: (3*3+6)*3-5
# DISPLAYING CONSTRUCTED TREE:
# ('-', ('*', ('+', ('*', '3', '3'), '6'), '3'), '5')
# ----------------------------------------
# EVALUATING: (3*3+6)*3-5
# Step 0 : Push 3
# Step 1 : Push 3
# step 2 : Pop 3, Pop 3.
# Compute 3 * 3. 
# Push 9.00
# Step 4 : Push 6
# step 5 : Pop 6, Pop 9.
# Compute 9 + 6. 
# Push 15.00
# Step 7 : Push 3
# step 8 : Pop 3, Pop 15.
# Compute 15 * 3. 
# Push 45.00
# Step 10 : Push 5
# step 11 : Pop 5, Pop 45.
# Compute 45 - 5. 
# Push 40.00
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# (3*3+6)*3-5 = 40.0
# ****************************************




# INPUT EXPRESSION: ((3*3-5)*4-10)
# DISPLAYING CONSTRUCTED TREE:
# ('-', ('*', ('-', ('*', '3', '3'), '5'), '4'), '10')
# ----------------------------------------
# EVALUATING: ((3*3-5)*4-10)
# Step 0 : Push 3
# Step 1 : Push 3
# step 2 : Pop 3, Pop 3.
# Compute 3 * 3. 
# Push 9.00
# Step 4 : Push 5
# step 5 : Pop 5, Pop 9.
# Compute 9 - 5. 
# Push 4.00
# Step 7 : Push 4
# step 8 : Pop 4, Pop 4.
# Compute 4 * 4. 
# Push 16.00
# Step 10 : Push 10
# step 11 : Pop 10, Pop 16.
# Compute 16 - 10. 
# Push 6.00
# COMPLETE
# ----------------------------------------
# EVALUATION RESULT: 
# ((3*3-5)*4-10) = 6.0
# ****************************************
