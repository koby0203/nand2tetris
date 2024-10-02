import os

# コマンドタイプ定義
A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2


class Parser:
    def __init__(self, filename, root_dir='.'):
        self.filename = filename
        self.root_dir = root_dir
        self.filepath = self.find_file()
        if self.filepath is None:
            raise FileNotFoundError(f'File {filename} not found in {root_dir}')
        self.lines = self.get_lines()
        self.next_line = 0
        self.current_command = None

    def find_file(self):
        for dirpath, _, filenames in os.walk(self.root_dir):
            if self.filename in filenames:
                return os.path.join(dirpath, self.filename)
        return None

    def get_lines(self):
        # 空行とコメント行（行頭が//）は削除したリストを返す
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()
                 and not line.startswith('//')]
        # 途中の空白やコメントも削除
        lines = [line.split('//')[0].strip() for line in lines]
        return lines

    def has_more_commands(self):
        return self.next_line < len(self.lines)

    def advance(self):
        self.current_command = self.lines[self.next_line]
        self.next_line += 1

    def command_type(self):
        if self.current_command.startswith('@'):
            return A_COMMAND
        elif self.current_command.startswith('('):
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        if self.command_type() == A_COMMAND:
            return self.current_command[1:]
        elif self.command_type() == L_COMMAND:
            return self.current_command[1:-1]
        else:
            raise ValueError('symbol() called for C_COMMAND')

    def dest(self):
        if '=' in self.current_command:
            return self.current_command.split('=')[0]
        else:
            return None

    def comp(self):
        if '=' in self.current_command:
            return self.current_command.split('=')[1]
        else:
            return self.current_command

    def jump(self):
        if ';' in self.current_command:
            return self.current_command.split(';')[1]
        else:
            return None


if __name__ == '__main__':
    # Parserクラスのテストコード
    parser = Parser('test.txt')
    while parser.has_more_commands():
        parser.advance()
        commandType = parser.command_type()
        if commandType == A_COMMAND or commandType == L_COMMAND:
            print(f'{parser.symbol()}')
        # elif commandType == C_COMMAND:
        #     print(f'C_COMMAND: {parser.current_command}')
        # elif commandType == L_COMMAND:
        #     print(f'L_COMMAND: {parser.symbol()}')
        # else:
        #     print('Unknown command type')