#!/usr/bin/env python2
import subprocess


class Validator(object):
    def validate(self, answer_path, output_path):
        raise NotImplementedError


class DiffValidator(Validator):
    def validate(self, answer_path, output_path):
        return subprocess.call(
            ['diff', '-y', '-d', answer_path, output_path]) == 0


class FloatingPointValidator(Validator):
    absolute_error = None

    def __init__(self, absolute_error):
        self.absolute_error = float(absolute_error)

    def validate(self, answer_path, output_path):
        answer_file = open(answer_path)
        output_file = open(output_path)
        result = True
        print('%-25s %-25s   %-15s' % ('answer', 'output', 'diff'))
        while True:
            answer_line = answer_file.readline()
            output_line = output_file.readline()

            if answer_line == '' and output_line == '':
                break

            answer_line = answer_line.strip()
            output_line = output_line.strip()

            answer_value = float(answer_line)
            output_value = float(output_line)
            ok = False
            diff = output_value - answer_value

            if abs(diff) < self.absolute_error:
                ok = True

            separator = ' '

            if not ok:
                separator = '|'
                result = False

            print('%-25s %-25s %s %-15e %e' %
                  (answer_line, output_line, separator, diff))
        return result
