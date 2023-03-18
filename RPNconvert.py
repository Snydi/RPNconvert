import math

# Define functions and their arities
functions = {
    "sin": 1,
    "cos": 1,
    "log": 2,
    "sqrt": 1,
}

# Define operators and their properties
operators = {
    "^": {"precedence": 4, "associativity": "right"},
    "*": {"precedence": 3, "associativity": "left"},
    "/": {"precedence": 3, "associativity": "left"},
    "+": {"precedence": 2, "associativity": "left"},
    "-": {"precedence": 2, "associativity": "left"},
}

# Convert infix notation to RPN
def infix_to_rpn(expression):
    output = []
    stack = []
    for token in expression:
        if token.isdigit() or "." in token:
            output.append(token)
        elif token in functions:
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            if len(stack) > 0 and stack[-1] in functions:
                output.append(stack.pop())
            stack.pop()
        else: # token is an operator
            while len(stack) > 0 and stack[-1] != "(" and (operators[token]["precedence"] < operators[stack[-1]]["precedence"] or (operators[token]["precedence"] == operators[stack[-1]]["precedence"] and operators[token]["associativity"] == "left")):
                output.append(stack.pop())
            stack.append(token)
    while len(stack) > 0:
        output.append(stack.pop())
    return output

# Evaluate an RPN expression
def evaluate_rpn(expression):
    stack = []
    for token in expression:
        if token.isdigit() or "." in token:
            stack.append(float(token))
        elif token in functions:
            args = []
            for i in range(functions[token]):
                args.append(stack.pop())
            args.reverse()
            if token == "sin":
                stack.append(math.sin(args[0] * math.pi/180))
            elif token == "cos":
                if args[0] == 90:
                    stack.append(0)
                else:
                    stack.append(math.cos(args[0] * math.pi/180))
            elif token == "log":
                stack.append(math.log(args[1], args[0]))
            elif token == "sqrt":
                stack.append(math.sqrt(args[0]))
        else:
            arg2 = stack.pop()
            arg1 = stack.pop()
            if token == "^":
                stack.append(arg1 ** arg2)
            elif token == "*":
                stack.append(arg1 * arg2)
            elif token == "/":
                stack.append(arg1 / arg2)
            elif token == "+":
                stack.append(arg1 + arg2)
            elif token == "-":
                stack.append(arg1 - arg2)
    return stack.pop()

# Read and evaluate expressions from standard input
while True:
    try:
        expression = input("Enter an expression: ")
        tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
        rpn = infix_to_rpn(tokens)
        print("Converted expression:", " ".join(rpn))
        result = evaluate_rpn(rpn)
        #print("Result:", result)
    except (EOFError, KeyboardInterrupt):
        break
    except:
        print("Error evaluating expression")
