# !/usr/bin/env python3
# YOU SHOULD NOT MODIFY THIS FILE
# 
# test_a1p2.py version 2021.02.24
#
# Vrinda Mathur

import route
from subprocess import TimeoutExpired, CalledProcessError

def validate_route(answer, args):
    arg_start, arg_end, arg_cost = args
    assert isinstance(answer, dict), "get_route() is not returning a dictionary"
    assert len(answer) == 5, "Too few parts: returned dictionary should have 5 keys"

    segments, miles = answer['total-segments'], answer['total-miles']
    hours, safe, route_taken = answer['total-hours'], answer['total-expected-accidents'], answer['route-taken']

    assert isinstance(segments, int), '"%s" is not an int: total-segments must be int' % segments
    assert segments >= 0, '"%s" < 0: total-segments must be positive' % segments
    assert isinstance(miles, float), '"%s" is not an int: total-miles must be float' % miles
    assert miles >= 0, '"%s" < 0: total-miles must be positive' % miles
    assert isinstance(hours, float), '"%s" is not an int: total-hours must be int' % hours
    assert hours >= 0, '"%s" < 0: total-hours must be positive' % hours
    assert isinstance(safe, float), '"%s" is not an float: Any probability must be float' % safe
    assert safe >= 0, '"%s" < 0: Probability of an accident must be positive' % safe
    assert len(route_taken) == segments, 'Route taken does not correspond to total number of segments'
    # assert route_taken[0][0] == arg_start, '"%s" is not "%s": start-city is wrong' % (route_taken[0][0], arg_start)
    assert route_taken[segments - 1][0] == arg_end, '"%s" is not "%s" not the end-city' % (route_taken[segments - 1][0], arg_end)
    return segments, miles, hours, safe


def test_part2_case1():
    script_path = 'route.py'
    for script_args in [('Bloomington,_Indiana', 'Indianapolis,_Indiana', x) for x in
                        ('distance', 'segments', 'time', 'safe')]:
        print("Testing ./%s %s" % (script_path, ' '.join(script_args)))

        try:
            output = route.get_route(*script_args)
            assert isinstance(output, dict), "get_route() is not returning a dictionary"
        except TimeoutExpired:
            print('Timeout')
            continue
        except CalledProcessError as e:
            print('An error occurred running your code:')
            print(e.output.decode('utf8'))
            continue

        optimal_ans, calculated = {"segments": 3, "distance": 51.0, "time": 1.07949,"safe": 0.000102}, {}
        calculated['segments'], calculated['distance'], calculated['time'], calculated['safe'] = validate_route(output, script_args)
        assert calculated[script_args[2]] <= optimal_ans[script_args[2]],'Output format is correct but optimal %s cost is %s' % (script_args[2], optimal_ans[script_args[2]])

