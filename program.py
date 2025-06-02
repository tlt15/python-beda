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

    def has_path_to(self, target):
        queue = [self.current_state]
        visited = {self.current_state}
        graph = {
            'Y6': ['Y5'],
            'Y5': ['Y3', 'Y6'],
            'Y3': ['Y5', 'Y1'],
            'Y1': ['Y0', 'Y1'],
            'Y0': ['Y2'],
            'Y2': ['Y4'],
            'Y4': []
        }

        while queue:
            current = queue.pop(0)
            if current == target:
                return True
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False

    def seen_method(self, method):
        return method in self.seen

    def get_current_state(self):
        return self.current_state

def main():
    return MooreMachine()

def _assert_state(machine, expected_state, method_name):
    if method_name == "get_output":
        if machine.get_output() != expected_state:
            raise AssertionError(
                f"Expected output {expected_state} but got {machine.get_output()} after {method_name}"
            )
    else:
        if machine.current_state != expected_state:
            raise AssertionError(
                f"Expected state {expected_state} but got {machine.current_state} after {method_name}"
            )

def _assert_error(method_name, expected_error, actual_error):
    if expected_error:
        if str(actual_error) != expected_error:
            raise AssertionError(f"Expected error '{expected_error}' but got '{actual_error}' for {method_name}")
    else:
        raise AssertionError(f"Unexpected MachineError: {actual_error} for {method_name}")


def _test_transition(machine, method_name, initial_state, expected_state, expected_error, k_value=None):
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
        raise AssertionError(f"Unexpected exception: {e} for {method_name}")
        return
    if expected_error:
        _assert_error(method_name, expected_error, None)
    else:
        _assert_state(machine, expected_state, method_name)

def _test_unsupported_transition(machine, method_name, initial_state, expected_error):
    machine.current_state = initial_state
    try:
        getattr(machine, method_name)()
        raise AssertionError(f"Expected MachineError, but no error was raised for {method_name}")
    except MachineError as e:
        if str(e) != expected_error:
            raise AssertionError(f"Expected error '{expected_error}' but got '{e}'")


def _test_other(machine, test_type, *args):
    if test_type == "has_path_to":
        target, expected_result = args
        if machine.has_path_to(target) != expected_result:
            raise AssertionError(f"has_path_to('{target}') failed")
    elif test_type == "seen_method":
        method_name, should_be_seen = args
        if machine.seen_method(method_name) != should_be_seen:
            raise AssertionError(f"seen_method('{method_name}') failed")

class TestMooreMachine(unittest.TestCase):

    def test_unsupported_transitions(self):
        # Test unsupported transitions first
        machine = main()
        _test_unsupported_transition(machine, "go_hop", 'Y6', "unsupported")
        machine = main()
        _test_unsupported_transition(machine, "go_drag", 'Y6', "unsupported")
        machine = main()
        _test_unsupported_transition(machine, "go_mute", 'Y5', "unsupported")
        machine = main()
        _test_unsupported_transition(machine, "go_tag", 'Y1', "unsupported")

    def test_go_tag_from_non_y5(self):
      machine = main()
      machine.current_state = 'Y1'
      with self.assertRaises(MachineError):
          machine.go_tag()

    def test_transitions(self):
        test_cases = [
            ("go_mute", 'Y6', 'Y5', None, None),
            ("go_tag", 'Y5', 'Y6', None, None),
            ("go_loop", 'Y5', 'Y3', None, None),  # Test go_loop from Y5
            ("assign_k", 'Y6', 'Y6', None, 0),
            ("go_loop", 'Y3', 'Y5', None, 0),  # k=0, after setting k=0 - Удалено
            ("assign_k", 'Y3', 'Y3', None, 1),
            ("go_loop", 'Y3', 'Y1', None, 1),  # k=1, after setting k=1 - Удалено
            ("go_mute", 'Y1', 'Y1', None, None),  # Test go_mute from Y1
            ("go_drag", 'Y1', 'Y0', None, None),
            ("go_drag", 'Y0', 'Y2', None, None),
            ("go_hop", 'Y2', 'Y4', None, None),
        ]

        for test_case in test_cases:
            machine = main()
            _test_transition(machine, *test_case)


    def test_has_path_to(self):
        machine = main()
        _test_other(machine, "has_path_to", 'Y4', True)
        machine = main()
        _test_other(machine, "has_path_to", 'NonExistentState', False)

    def test_seen_method(self):
        machine = main()
        _test_other(machine, "seen_method", 'mute', False)
        machine.go_mute()
        _test_other(machine, "seen_method", 'mute', True)

    def test_assert_error_incorrect_error(self): # Covering _assert_error if error is different
        with self.assertRaises(AssertionError):
            _assert_error("test", "wrong_error", "actual_error")

    def test_assert_error_no_error(self): # Covering _assert_error if no error is raised
        with self.assertRaises(AssertionError):
            _assert_error("test", "expected_error", None)

    def test_assert_state_wrong_output(self):
        machine = main()
        with self.assertRaises(AssertionError):
            _assert_state(machine, "wrong_output", "get_output")

    def test_assert_error_no_expected_error(self):
        with self.assertRaises(AssertionError):
            _assert_error("test", None, "actual_error")

    def test_assert_state_wrong_state(self):
        machine = main()
        with self.assertRaises(AssertionError):
            _assert_state(machine, "wrong_state", "go_mute")

    def test_transition_unexpected_exception(self):
        machine = main()
        def raise_exception():
          raise ValueError("Generic Exception")
        machine.raise_exception = raise_exception
        with self.assertRaises(AssertionError):
            _test_transition(machine, "raise_exception", 'Y6', None, None)

    def test_go_loop_from_y5_to_y3(self):
        machine = main()
        machine.current_state = 'Y5'
        machine.go_loop()
        self.assertEqual(machine.get_current_state(), 'Y3')

    def test_current_state_is_y6(self):
        machine = main()
        self.assertEqual(machine.get_current_state(), 'Y6')

    def test_go_loop_from_y6(self): # for partial coverage
        machine = main()
        machine.go_mute()
        machine.go_loop()
        self.assertEqual(machine.get_current_state(), 'Y3') # added assertion

    def test_go_loop_k_0(self):
        machine = main()
        machine.current_state = 'Y3'
        machine.assign_k(0)
        machine.go_loop()
        self.assertEqual(machine.get_current_state(), 'Y5')

    def test_go_loop_k_1(self):
        machine = main()
        machine.current_state = 'Y3'
        machine.assign_k(1)
        machine.go_loop()
        self.assertEqual(machine.get_current_state(), 'Y1')