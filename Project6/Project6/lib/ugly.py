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

def compile_array_get_size(tokens,output):
    array = tokens[1].replace("a","")
    mem = tokens[2].replace("s","")
    output.append("load {} regA".format(array))
    output.append("mem_copy regA {}".format(mem))

def compile_array_set_size(tokens,output,counter):
    array = tokens[1].replace("a","")

    mem = tokens[2]
    output.append("load {} regA".format(array))
    if mem.startswith("s"):
        mem = mem.replace("s","")
        output.append("load {} regB".format(mem))
    else:
        output.append("val_copy {} regB".format(mem))

    output.append("test_equ regA 0 regC")
    output.append("jump_if_n0 regC init_array_{}".format(counter))

    output.append("load regA regC")
    output.append("store regB regA")
    output.append("test_lte regB regC regD")
    output.append("jump_if_0 regD resize_end_{}".format(counter))
    output.append("load 0 regD")
    output.append("add regD 1 regE")
    output.append("add regE regB regE")
    output.append("store regE 0")
    output.append("store regD {}".format(array))
    output.append("store regB regD")
    output.append("resize_start_{}:".format(counter))
    output.append("add regA 1 regA")
    output.append("add regD 1 regD")
    output.append("test_gtr regD regE regF")
    output.append("jump_if_n0 regF resize_end_{}".format(counter))
    output.append("mem_copy regA regD")
    output.append("jump resize_start_{}".format(counter))

    output.append("init_array_{}:".format(counter))
    output.append("mem_copy 0 {}".format(array))
    output.append("load 0 regC")
    output.append("store regB regC")
    output.append("add regB 1 regB")
    output.append("add regB regC regD")
    output.append("store regD 0")
    output.append("store regC {}".format(array))


    output.append("resize_end_{}:".format(counter))

def compile_array_copy(tokens,output,counter):

    source = tokens[1].replace("a","")
    destination = tokens[1].replace("a","")

    output.append("load {} regA".format(source))
    output.append("load regA regB")
    output.append("load 0 regC")
    output.append("store regC {}".format(destination))
    output.append("add regC regB regD")
    output.append("add regD 1 regD")
    output.append("store regD 0")
    # regA: Pointer to array
    # regB: size of array 
    # regC: Pointer to new array on the heap
    
    output.append("val_copy 0 regD")
    output.append("start_array_copy_{}:".format(counter))
    output.append("test_lte regD regB regE")
    output.append("jump_if_0 regE end_array_copy_{}".format(counter))
    output.append("mem_copy regA regC")
    output.append("out_val regA")
    output.append("out_char ' '")
    output.append("out_val regC")
    output.append("out_char '\\n'")
    output.append("add regA 1 regA")
    output.append("add regC 1 regC")
    output.append("add regD 1 regD")
    output.append("jump start_array_copy_{}".format(counter))
    output.append("end_array_copy_{}:".format(counter))

def compile_array_get_index(tokens,output):
    array = tokens[1].replace("a","")
    index = tokens[2]
    destination = tokens[3]

    output.append("load {} regA".format(array))

    if index.startswith("s"):
        index = index.replace("s","")
        output.append("load {} regB".format(index))
        index = "regB"

    if destination.startswith("s"):
        destination = destination.replace("s","")

    output.append("add regA {} regA".format(index))
    output.append("add regA 1 regA".format(index))
    output.append("mem_copy regA {}".format(destination))

def compile_array_set_index(tokens,output):
    array = tokens[1].replace("a","")
    index = tokens[2]
    source = tokens[3]

    output.append("load {} regA".format(array))

    if index.startswith("s"):
        index = index.replace("s","")
        output.append("load {} regB".format(index))
        index = "regB"

    if source.startswith("s"):
        source = source.replace("s","")

    output.append("add regA {} regA".format(index))
    output.append("add regA 1 regA".format(index))
    output.append("mem_copy {} regA".format(source))


def compile_ugly_command(tokens,output,counter):
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
    elif command == "ar_get_size":
        compile_array_get_size(tokens,output)
    elif command == "ar_set_size":
        compile_array_set_size(tokens,output,counter)
    elif command == "ar_copy":
        compile_array_copy(tokens,output,counter)
    elif command == "ar_set_idx":
        compile_array_set_index(tokens,output)
    elif command == "ar_get_idx":
        compile_array_get_index(tokens,output)
    elif command == "":
        output.append("# Empty line")
    else:
        output.append("# Failed to compile line command: {}".format(command))

def compile_ugly_lines(lines):
    output = ["store 100000 0"]
    counter = 0
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
        compile_ugly_command(tokens,output,counter)
        counter += 1
        output.append("# Done Interpreting: {}".format(line))
    return output
