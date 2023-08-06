from assistant.bot import assistant_bot


def test__is_clock_in():
    payload = {'code': '0', 'msg': '成功', 'result': [{'time': '2020-08-15', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-14', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-13', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-12', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-11', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-10', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-09', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-08', 'conditions': ['正常状态'], 'tempature': '36 ℃'},
                                                    {'time': '2020-08-06', 'conditions': ['正常状态'], 'tempature': '36 ℃'}
                                                    ]}

    res = assistant_bot._is_clock_in(payload)
    assert res


def test__remind_clockin():
    assistant_bot._remind_clockin()
