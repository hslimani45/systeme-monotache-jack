class functionCall:
    """Génère le code ASM pour function / call / return."""

    def __init__(self):
        self.currentFunction = ''
        self.counter = 0

    def asm(self, command):
        """Dispatch pour Function, Call, return."""
        cmd = command.get('type')
        if cmd in ('function', 'Function'):
            return self._commandfunction(command)
        elif cmd in ('call', 'Call'):
            return self._commandcall(command)
        elif cmd == 'return':
            return self._commandreturn(command)
        else:
            print(f'SyntaxError : {command}')
            exit()

    def _commandfunction(self, command):
        """function f k  => (f) puis k variables locales initialisées à 0."""
        # accept keys produced by different parser variants
        self.currentFunction = command.get('function') or command.get('functionName')
        nLcl = int(command.get('parameter') or command.get('nLcl') or 0)
        lines = [f"// function {self.currentFunction} {nLcl}",
                 f"({self.currentFunction})"]
        for _ in range(nLcl):
            lines.extend([
                "@SP",
                "A=M",
                "M=0",
                "@SP",
                "M=M+1",
            ])
        return "\n".join(lines)

    def _commandcall(self, command):
        """call f n : protocole standard Nand2Tetris."""
        # accept both 'function'/'parameter' and 'functionName'/'nArgs'
        function_name = command.get('function') or command.get('functionName')
        nArgs = int(command.get('parameter') or command.get('nArgs') or 0)
        self.counter += 1
        # Utiliser uniquement des caractères acceptés par tous les émulateurs (pas de $)
        return_label = f"RET_{function_name}_{self.counter}"

        lines = [f"// call {function_name} {nArgs}"]
        # push return-address
        lines.extend([
            f"@{return_label}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ])
        # push LCL
        lines.extend([
            "@LCL",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ])
        # push ARG
        lines.extend([
            "@ARG",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ])
        # push THIS
        lines.extend([
            "@THIS",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ])
        # push THAT
        lines.extend([
            "@THAT",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ])
        # ARG = SP - 5 - nArgs
        lines.extend([
            "@SP",
            "D=M",
            "@5",
            "D=D-A",
            f"@{nArgs}",
            "D=D-A",
            "@ARG",
            "M=D",
        ])
        # LCL = SP
        lines.extend([
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
        ])
        # goto f
        lines.extend([
            f"@{function_name}",
            "0;JMP",
            f"({return_label})",
        ])
        return "\n".join(lines)

    def _commandreturn(self, command):
        """return : protocole standard Nand2Tetris."""
        lines = ["// return"]
        # FRAME = LCL (utilise R13)
        lines.extend([
            "@LCL",
            "D=M",
            "@R13",
            "M=D",
        ])
        # RET = *(FRAME-5) (utilise R14)
        lines.extend([
            "@5",
            "A=D-A",
            "D=M",
            "@R14",
            "M=D",
        ])
        # *ARG = pop()
        lines.extend([
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
        ])
        # SP = ARG+1
        lines.extend([
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D",
        ])
        # THAT = *(FRAME-1)
        lines.extend([
            "@R13",
            "AM=M-1",
            "D=M",
            "@THAT",
            "M=D",
        ])
        # THIS = *(FRAME-2)
        lines.extend([
            "@R13",
            "AM=M-1",
            "D=M",
            "@THIS",
            "M=D",
        ])
        # ARG = *(FRAME-3)
        lines.extend([
            "@R13",
            "AM=M-1",
            "D=M",
            "@ARG",
            "M=D",
        ])
        # LCL = *(FRAME-4)
        lines.extend([
            "@R13",
            "AM=M-1",
            "D=M",
            "@LCL",
            "M=D",
        ])
        # goto RET
        lines.extend([
            "@R14",
            "A=M",
            "0;JMP",
        ])
        return "\n".join(lines)