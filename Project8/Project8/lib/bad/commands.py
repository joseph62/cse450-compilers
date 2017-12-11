# Command Objects for bad language instructions

class Command:
    def __init__(self,instruction,arguments,usage):
        self._arguments = arguments
        self._reads = []
        self._writes = []
        self._instruction = instruction
        for use,argument in zip(usage,arguments):
            if use == "r":
                self._reads.append(argument)
            elif use == "w":
                self._writes.append(argument)

    def __str__(self):
        result =  "{}".format(self._instruction)
        for argument in self._arguments:
            result = result + " {}".format(argument)
        return result

    __repr__ = __str__

    @property
    def reads(self):
        return self._reads

    @property
    def writes(self):
        return self._writes

    @property
    def instruction(self):
        return self._instruction

    def variable_is_written(self,variable):
        return variable in self._writes

    def variable_is_read(self,variable):
        return variable in self._reads


class CommandFactory:

    @staticmethod
    def make_command(instruction,arguments):
        usages = {
                "val_copy" : "rw",
                "random" : "rw",
                "add" : "rrw",
                "sub" : "rrw",
                "mult" : "rrw",
                "div" : "rrw",
                "test_less" : "rrw",
                "test_gtr" : "rrw",
                "test_equ" : "rrw",
                "test_nequ" : "rrw",
                "test_gte" : "rrw",
                "test_lte" : "rrw",
                "jump_if_0" : "rw",
                "jump_if_n0" : "rw",
                "jump" : "r",
                "out_char" : "r",
                "out_val" : "r",
                "pop" : "w",
                "push" : "r",
                "nop" : "",
                "ar_get_idx" : "rrw",
                "ar_set_idx" : "wrr",
                "ar_get_size" : "rw",
                "ar_set_size" : "wr",
                "ar_copy" : "rw",
                "ar_pop" : "w",
                "ar_push" : "r",
                # target is a special instruction for tag lines
                "target" : "r",
                }

        if instruction not in usages:
            raise ValueError("Instruction {} usage not specified!".format(instruction))

        return Command(instruction,arguments,usages[instruction])
