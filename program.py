class MachineError(Exception):
    pass


class MooreMachine:
    def __getattr__(self, name):
        raise MachineError("unknown")

    def __init__(self):
        self.current_state = 'Y6'
        self.output = {'Y6': 'b4', 'Y5': 'b2', 'Y3': 'b3', 'Y1': 'b4',
                       'Y0': 'b5', 'Y2': 'b3', 'Y4': 'b1'}
        self.k = 0
        self.seen = set()

    def assign_k(self, value):
        self.k = value

    def go_mute(self):
        if self.current_state == 'Y6':
            self.current_state = 'Y5'
            self.seen.add('mute')
        elif self.current_state == 'Y1':
            self.current_state = 'Y1'
            self.seen.add('mute')
        elif self.current_state == 'Y4':
            self.current_state = 'Y5'
            self.seen.add('mute')
        else:
            raise MachineError('unsupported')

    def go_tag(self):
        if self.current_state == 'Y5':
            self.current_state = 'Y5'
            self.seen.add('tag')
        else:
            raise MachineError('unsupported')

    def go_loop(self):
        if self.current_state == 'Y5':
            self.current_state = 'Y3'
            self.seen.add('loop')
        elif self.current_state == 'Y3' and self.k == 0:
            self.current_state = 'Y6'
            self.seen.add('loop')
        elif self.current_state == 'Y3' and self.k == 1:
            self.current_state = 'Y1'
            self.seen.add('loop')
        else:
            raise MachineError('unsupported')

    def go_drag(self):
        if self.current_state == 'Y1':
            self.current_state = 'Y0'
            self.seen.add('drag')
        elif self.current_state == 'Y0':
            self.current_state = 'Y2'
            self.seen.add('drag')
        else:
            raise MachineError('unsupported')

    def go_hop(self):
        if self.current_state == 'Y2':
            self.current_state = 'Y4'
            self.seen.add('hop')
        else:
            raise MachineError('unsupported')

    def get_output(self):
        return self.output[self.current_state]

    def has_path_to(self, state):
        return True

    def seen_method(self, method):
        return method in self.seen


def main():
    return MooreMachine()


def test():
    obj = main()
    obj.assign_k(1)
    try:
        obj.go_hop()
    except MachineError as e:
        assert str(e) == "unsupported"
    obj.has_path_to('Y3')
    obj.seen_method('hop')
    obj.go_mute()
    obj.get_output()
    try:
        obj.go_doub()
    except MachineError as e:
        assert str(e) == "unknown"
    obj.has_path_to('Y1')
    obj.seen_method('tag')
    obj.go_tag()
    obj.seen_method('tag')
    obj.has_path_to('Y3')
    obj.get_output()
    obj.seen_method('hop')
    obj.go_loop()
    try:
        obj.go_doub()
    except MachineError as e:
        assert str(e) == "unknown"
    obj.get_output()
    try:
        obj.go_post()
    except MachineError as e:
        assert str(e) == "unknown"
    obj.go_loop()
    obj.get_output()
    obj.seen_method('loop')
    obj.go_drag()
    obj.get_output()
    obj.has_path_to('Y0')
    obj.go_drag()
    obj.get_output()
    obj.go_hop()
    obj.get_output()
    try:
        obj.go_hike()
    except MachineError as e:
        assert str(e) == "unknown"
    obj.go_mute()
    obj.get_output()
    obj.current_state = "Y4"
    try:
        obj.go_tag()
    except MachineError as e:
        assert str(e) == "unsupported"
    try:
        obj.go_loop()
    except MachineError as e:
        assert str(e) == "unsupported"
    try:
        obj.go_drag()
    except MachineError as e:
        assert str(e) == "unsupported"
    obj.current_state = "Y2"
    try:
        obj.go_mute()
    except MachineError as e:
        assert str(e) == "unsupported"
    obj.current_state = "Y3"
    obj.assign_k(0)
    obj.go_loop()
    obj.current_state = "Y1"
    obj.go_mute()
