from sys import stdin
input_ = stdin.read()

scopes = [[]]

def find_var(scopes,var):
    for i in range(len(scopes)-1,-1,-1):
        scope = scopes[i]
        if var in scope:
            return i
    return -1

def add_var(scopes,var):
    if var in scopes[-1]:
        return -1
    scopes[-1].append(var)
    return 1

for line in input_.splitlines():
    tokens = line.split(' ')
    action = tokens[0]
    operand = tokens[1]

    if action == "declare":
        result = add_var(scopes,operand)
        if result == -1:
            print("Trying to declare {} at scope {}: FAILED".format(
                operand,len(scopes)-1))
        else:
            print("Trying to declare {} at scope {}: SUCCESS".format(
                operand,len(scopes)-1))

    if action == "use":
        result = find_var(scopes,operand)
        if result == -1:
            print("Trying to use {} at scope {}: FAILED".format(
                operand,len(scopes)-1))
        else:
            print("Trying to use {} at scope {}: SUCCESS (found in scope {})"
                    .format(operand,len(scopes)-1,result))

    if action == "close":
        print("Trying to close scope at {}: SUCCESS".format(len(scopes)-1))
        scopes.pop()

    if action == "open":
        print("Trying to open scope at {}: SUCCESS".format(len(scopes)-1))
        scopes.append([])
