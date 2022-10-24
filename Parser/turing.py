import collections

class State:
    def __init__(self, state):
        self.state = state.value
        self.fail = False
        self.success = False
        self.transfers = dict()

    def final(self):
        return self.fail or self.success


class Transfer:
    def __init__(self, state, ch, move):
        self.state = state
        self.ch = ch
        self.move = 1 if move == 'right' else -1 if move == 'left' else 0


def position(token):
    return '(Line:' + token.lineno + ':' + token.lexpos + ')'


class TuringMachine:
    def __init__(self, alphabet, extra_alphabet, states, blank, start, fail, success, function):
        self.states = dict()
        self.alphabet = dict()
        for ch in alphabet:
            if ch.value not in self.alphabet:
                self.alphabet[ch.value] = ch
        for ch in extra_alphabet:
            if ch.value not in self.alphabet:
                self.alphabet[ch.value] = ch
        for state in states:
            if state.value not in self.states:
                self.states[state.value] = State(state)
        self.check_char(blank)
        self.blank = blank.value
        self.check_state(start)
        self.start = self.states[start.value]
        for f in fail:
            self.check_state(f)
            self.states[f.value].fail = True
        for s in success:
            self.check_state(s)
            self.states[s.value].success = True
        for transfer in function:
            self.check_state(transfer[0])
            self.check_char(transfer[1])
            self.check_state(transfer[2])
            self.check_char(transfer[3])
            self.states[transfer[0].value].transfers[transfer[1].value] = Transfer(
                self.states[transfer[2].value],
                transfer[3].value, transfer[4].value)

    def check_char(self, ch):
        if ch.value not in self.alphabet:
            print('Char is not in alphabet ' + position(ch))
            exit(1)

    def check_state(self, state):
        if state.value not in self.states:
            print('Undefined state ' + position(state))
            exit(1)

    def run(self, values, verbous):
        pos = 0
        pos0 = 0
        dq = collections.deque()
        for value in values:
            if value not in self.alphabet:
                print('Error: Undefined value provided: ' + value)
                exit(1)
            dq.append(value)
        state = self.start
        if len(values) == 0:
            dq.append(self.blank)
        step = 0
        if verbous:
            data = collections.deque(dq)
            data[pos] = '(' + data[pos] + ')'
            print('Step ' + str(step) + ': ' + state.state + ' : ' + ' '.join(data))
        while not state.final():
            ch = dq[pos]
            if ch not in state.transfers:
               print('State ' + state.state + 'is not terminal and there are no transition by char ' + ch)
               exit(1)
            transfer = state.transfers[ch]
            dq[pos] = transfer.ch
            state = transfer.state
            pos += transfer.move
            if pos < 0:
                dq.appendleft(self.blank)
                pos = 0
                pos0 += 1
            if pos == len(dq):
                dq.append(self.blank)
            step += 1
            if verbous:
                data = collections.deque(dq)
                data[pos] = '(' + data[pos] + ')'
                print('Step ' + str(step) + ': ' + state.state + ' : ' + ' '.join(data))

        while len(dq) > 0 and dq[0] == self.blank:
            dq.popleft()
            pos0 -= 1
        while len(dq) > 0 and dq[len(dq) - 1] == self.blank:
            dq.pop()

        print('Final state ' + state.state + ':' + (' Success' if state.success else ' Error'))
        print(*dq)
