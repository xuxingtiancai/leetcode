#�Զ���״̬��
class State:
    #NFA״̬id=int, DFA״̬id=set
    def __init__(self, id):
        self.id = id
        self.convert = dict()

#������ʽת��Ϊ�Զ���
class Re2DFA:
    def __init__(self):
        self.state_store = dict()
        self.final_state_id = None
        self.start_state = None

    def show(self):
        for k, state in self.state_store.items():
            print k, [(k, v.id) for k, v in state.convert.items()]
        print 'final_state_id', self.final_state_id
        print 'start_state', self.start_state.id

    def getState(self, id):
        if id not in self.state_store:
            self.state_store[id] = State(id)
        return self.state_store[id]

    #����������ʽ
    def parse(self, p):
        while p != '':
            if len(p) >= 2 and p[1] == '*':
                yield p[0], True
                p = p[2:]
            else:
                yield p[0], False
                p = p[1:]

    #��ó�ʼ��NFA
    def getNFA(self, p):
        self.state_store.clear()
        self.final_state_id = None
        self.start_state = None

        generator = self.parse(p)
        try:
            input, repeat = generator.next()
        except:
            return
        tail = self.getState(0)
        if repeat: tail.convert[input] = tail
        last_input = '' if repeat else input

        for i, (input, repeat) in enumerate(generator, 1):
            state = self.getState(i)
            tail.convert[last_input] = tail = state
            if repeat: state.convert[input] = state
            last_input = '' if repeat else input

        if last_input != '':
            tail.convert[last_input] = tail = self.getState(tail.id + 1)
        self.final_state_id = tail.id

    #��һ��set��Ӧ��empty�հ�
    def empty_closure(self, source_set):
        target_set = set()
        for id in source_set:
            state = self.getState(id)
            while state and state.id not in target_set:
                target_set.add(state.id)
                state = state.convert.get('')
        return frozenset(target_set)

    #��һ��set��Ӧ��input�հ�
    def input_closure(self, source_set, input):
        target_set = set()
        for id in source_set:
            state = self.getState(id)
            if input in state.convert:
                target_set.add(state.convert[input].id)
            elif '.' in state.convert:
                target_set.add(state.convert['.'].id)
        return self.empty_closure(target_set) #frozenset

    #�����뼯��
    def getInput(self, source_set):
        input_set = set()
        for id in source_set:
            input_set |= set(self.getState(id).convert.keys())
        input_set -= set([''])
        return frozenset(input_set)

    #empty-NFAת��ΪDFA
    def compile(self, p):
        self.getNFA(p)
        if len(self.state_store) == 0:
            return
        A = self.getState(self.empty_closure(set([0])))
        self.start_state = A
        queue = [A]
        while queue:
            state = queue.pop(0)
            for input in self.getInput(state.id):
                extend_set = self.input_closure(state.id, input)
                if extend_set in self.state_store:
                    state.convert[input] = self.getState(extend_set)
                else:
                    state.convert[input] = self.getState(extend_set)
                    queue.append(state.convert[input])

    #match�����ַ���
    def match(self, s):
        if len(self.state_store) == 0:
            return s == ''

        state = self.start_state
        for input in s:
            try:
                state = state.convert[input]
            except:
                try:
                    state = state.convert['.']
                except:
                    return False
        return self.final_state_id in state.id
