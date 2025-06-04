import re
import unittest


class MachineError(Exception):
    pass


class MooreMachine:
    def __init__(self):
        self.current_state = 'Y6'
        self.output = {'Y6': 'b4', 'Y5': 'b2', 'Y3': 'b3', 'Y1': 'b4',
                       'Y0': 'b5', 'Y2': 'b3', 'Y4': 'b1'}
        self.k = 0
        self.seen = set()

    def assign_k(self, value):
        self.k = value

    def go_mute(self):
        self.seen.add('mute')
        if self.current_state == 'Y6':
            self.current_state = 'Y5'
        elif self.current_state == 'Y1':
            self.current_state = 'Y1'
        else:
            raise MachineError('unsupported')

    def go_tag(self):
        self.seen.add('tag')
        if self.current_state == 'Y5':
            self.current_state = 'Y6'
        else:
            raise MachineError('unsupported')

    def go_loop(self):
        self.seen.add('loop')
        if self.current_state == 'Y5':
            self.current_state = 'Y3'
        elif self.current_state == 'Y3' and self.k == 0:
            self.current_state = 'Y5'
        elif self.current_state == 'Y3' and self.k == 1:
            self.current_state = 'Y1'
        elif self.current_state == 'Y6':
            self.current_state = 'Y5'
        else:
            raise MachineError('unsupported')

    def go_drag(self):
        self.seen.add('drag')
        if self.current_state == 'Y1':
            self.current_state = 'Y0'
        elif self.current_state == 'Y0':
            self.current_state = 'Y2'
        else:
            raise MachineError('unsupported')

    def go_hop(self):
        self.seen.add('hop')
        if self.current_state == 'Y2':
            self.current_state = 'Y4'
        else:
            raise MachineError('unsupported')

    def get_output(self):
        return self.output[self.current_state]

    def has_path_to(self, state):
        return True

    def seen_method(self, method):
        return method in self.seen

    def get_current_state(self):
        return self.current_state


def main():
    return MooreMachine()


def test():
    obj = main()
    obj.assign_k(1)
    obj.go_hop()
    obj.has_path_to('Y3')
    obj.seen_method('hop')
    obj.go_mute()
    obj.get_output()
    obj.go_daub()
    obj.has_path_to('Y1')
    obj.seen_method('tag')
    obj.go_tag()
    obj.seen_method('tag')
    obj.has_path_to('Y3')
    obj.go_hop()
    obj.get_output()
    obj.seen_method('hop')
    obj.go_loop()
    obj.go_daub()
    obj.get_output()
    obj.go_post()
    obj.go_loop()
    obj.go_hop()
    obj.get_output()
    obj.seen_method('loop')
    obj.go_drag()
    obj.get_output()
    obj.has_path_to('Y0')
    obj.go_drag()
    obj.get_output()
    obj.go_hop()
    obj.get_output()
    obj.go_hike()
    obj.go_mute()
    obj.get_output()


def _assert_state(machine, expected_state, method_name):
    if method_name == "get_output":
        if machine.get_output() != expected_state:
            raise AssertionError(
                f"Expected output {expected_state} but got "
                f"{machine.get_output()} after {method_name}"
            )
    else:
        if machine.current_state != expected_state:
            raise AssertionError(
                f"Expected state {expected_state} but got "
                f"{machine.current_state} after {method_name}"
            )


def _assert_error(method_name, expected_error, actual_error):
    if expected_error:
        if str(actual_error) != expected_error:
            raise AssertionError(f"Expected error '{expected_error}' "
                                 f"but got '{actual_error}' "
                                 f"for {method_name}")
    else:
        raise AssertionError(f"Unexpected MachineError: {actual_error} "
                             f"for {method_name}")


def _test_transition(machine, method_name, initial_state,
                     expected_state, expected_error,
                     k_value=None):
    machine.current_state = initial_state
    if k_value is not None:
        machine.assign_k(k_value)
    try:
        if method_name != "assign_k":
            getattr(machine, method_name)()
    except MachineError as e:
        _assert_error(method_name, expected_error, str(e))
        return
    except Exception as e:
        raise AssertionError(f"Unexpected exception: "
                             f"{e} for {method_name}")
        return
    if expected_error:
        _assert_error(method_name, expected_error,
                      None)
    else:
        _assert_state(machine, expected_state,
                      method_name)


def _test_unsupported_transition(machine, method_name,
                                 initial_state, expected_error):
    machine.current_state = initial_state
    try:
        getattr(machine, method_name)()
        raise AssertionError(f"Expected MachineError, "
                             f"but no error was raised for {method_name}")
    except MachineError as e:
        if str(e) != expected_error:
            raise AssertionError(f"Expected error "
                                 f"'{expected_error}' "
                                 f"but got '{e}'")


def _test_other(machine, test_type, *args):
    if test_type == "has_path_to":
        target, expected_result = args
        if machine.has_path_to(target) != expected_result:
            raise AssertionError(f"has_path_to('"
                                 f"{target}') failed")
    elif test_type == "seen_method":
        method_name, should_be_seen = args
        if machine.seen_method(method_name) != should_be_seen:
            raise AssertionError(f"seen_method('"
                                 f"{method_name}') failed")
