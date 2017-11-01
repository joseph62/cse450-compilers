# Name: Sean Joseph
# Bad to Ugly compilation.
# This should be much easier to accomplish than
# Good to Bad. I'm basically Dennis Ritchie now.

def compile_val_copy(tokens,output):
    source = tokens[1]
    destination = tokens[2]
    if source.startswith("s"):
        mem1 = source.replace("s","")
        mem2 = destination.replace("s","")
        output.append("load {} regA".format(mem1))
        output.append("store regA {}".format(mem2))
    else:
        mem1 = destination.replace("s","")
        output.append("store {} {}".format(source,mem1))

def compile_out(tokens,output,command):
    value = tokens[1]
    if value.startswith("s"):
        value = value.replace("s","")
        output.append("load {} regA".format(value))
        output.append("{} regA".format(command))
    else:
        output.append("{} {}".format(command,value))

def compile_conditional_jump(tokens,output):
    command = tokens[0]
    value = tokens[1]
    tag = tokens[2]

    if value.startswith("s"):
        value = value.replace("s","")
        output.append("load {} regA".format(value))
        value = "regA"
    output.append("{} {} {}".format(command,value,tag))

def compile_random(tokens,output):
    argument = tokens[1]
    destination = tokens[2]
    if argument.startswith("s"):
        argument = argument.replace("s","")
        output.append("load {} regA".format(argument))
        argument = "regA"
    output.append("random {} regB".format(argument))
    if destination.startswith("s"):
        destination = destination.replace("s","") 
    output.append("store {} {}".format("regB",destination))

def compile_arith(tokens,output):
    command = tokens[0]
    left = tokens[1]
    right = tokens[2]
    result = tokens[3]

    if left.startswith("s"):
        left = left.replace("s","")
        output.append("load {} regA".format(left))
    else:
        output.append("val_copy {} regA".format(left))

    if right.startswith("s"):
        right = right.replace("s","")
        output.append("load {} regB".format(right))
    else:
        output.append("val_copy {} regB".format(right))

    output.append("{} regA regB regA".format(command))
    output.append("store regA {}".format(result.replace("s","")))

def compile_ugly_command(tokens,output):
    command = tokens[0]
    arith = ["add","sub","mult","div","test_gtr",
            "test_less","test_gte","test_lte",
            "test_equ","test_nequ"]
    if command == "val_copy":
        compile_val_copy(tokens,output)
    elif command.startswith("out_"):
        compile_out(tokens,output,command)
    elif command in arith:
        compile_arith(tokens,output)
    elif command == "jump":
        output.append(" ".join(tokens))
    elif command.startswith("jump"):
        # jump_if_0 and jump_if_n0
        compile_conditional_jump(tokens,output)
    elif command == "random":
        compile_random(tokens,output)
    elif command.endswith(":"):
        # Tag, just pass through
        output.append(" ".join(tokens))
    elif command == "":
        output.append("# Empty line")
    else:
        output.append("# Failed to compile line command: {}".format(command))

def compile_ugly_lines(lines):
    output = []
    for line in lines:
        # Process ' ' properly
        if "' '" in line:
            line = line.replace("' '","'<space>'")
        tokens = line.split(" ")
        for index,token in enumerate(tokens):
            if "<space>" in token:
                tokens[index] = token.replace("<space>"," ")
        if tokens[0].startswith("#"):
            #Skip comment lines
            continue
        output.append("# Interpreting: {}".format(line))
        compile_ugly_command(tokens,output)
        output.append("# Done Interpreting: {}".format(line))
    return output
