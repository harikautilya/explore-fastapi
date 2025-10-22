from api.core.singleton import Singleton

class SingletonFake(Singleton):
    pass

class SingletonDisbaledFake:
    pass

def test_singleon():

    model_one = SingletonFake()
    model_two = SingletonFake()

    assert model_one == model_two
    assert model_one is model_two


    model_non_singleton_one = SingletonDisbaledFake()
    model_non_singleton_two = SingletonDisbaledFake()

    assert model_non_singleton_one is not model_non_singleton_two