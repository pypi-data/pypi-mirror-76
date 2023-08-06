from config import CONFIG as cf


def test_config():
    print(cf.__dict__)
    assert cf.env == 'dev'
