

from program.ProgramVar import ProgramVar

class LoopProgram:

    def __init__(self):
        self.vars = []
        self.conditions = []
        self.statements = []
        self.smt_conditions = []
        self.smt_statements = []
        self.template = None

    def add_var(self, name, tp):
        self.vars.append(ProgramVar(name, tp))

    def get_var(self, index):
        if len(self.vars) > index >= 0:
            return self.vars[index]
        else:
            return None

    def get_num_var(self):
        return len(self.vars)

    def get_num_condition(self):
        return len(self.conditions)

    def add_loop_condition(self, expr):
        self.conditions.append(expr)

    def add_loop_statement(self, expr):
        self.statements.append(expr)

    def get_loop_condition(self, index=0):
        if len(self.conditions) > index >= 0:
            return self.conditions[index]
        else:
            return None

    def get_loop_statement(self, index=0):
        if len(self.conditions) > index >= 0:
            return self.statements[index]
        else:
            return None

    def add_loop_smt_condition(self, expr):
        self.smt_conditions.append(expr)

    def add_loop_smt_statement(self, expr):
        self.smt_statements.append(expr)

    def get_loop_smt_condition(self, index=0):
        if len(self.smt_conditions) > index >= 0:
            return self.smt_conditions[index]
        else:
            return None

    def get_loop_smt_statement(self, index=0):
        if len(self.smt_statements) > index >= 0:
            return self.smt_statements[index]
        else:
            return None

    def set_template(self, template):
        self.template = template

    def __str__(self):
        result = ''
        start = True
        for i in range(len(self.conditions)):
            pre = ''
            if not start:
                pre = ' OR '
            result += pre + ' Loop( ' + self.smt_conditions[i].__str__() + ', ' + self.smt_statements[i].__str__() + ') '
        return result

    def __repr__(self):
        return self.__str__()
