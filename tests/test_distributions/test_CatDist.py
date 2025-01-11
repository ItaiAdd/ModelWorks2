from modelworks2.distributions import CatDist


def dummy_func():
    pass

class DummyClass:
    pass


OPTIONS = [dummy_func, DummyClass(), 1, 2, 3, 'a', 'b', 'c']


test_dist = CatDist('test_dist', OPTIONS)


def test_sample():
    n=3
    sample = test_dist.sample(n)

    assert len(sample) == n
    assert all(e in OPTIONS for e in sample)


def test_sample_unique():
    for n  in range(2,len(OPTIONS)):
        sample = test_dist.sample_unique(n)
        assert len(sample) == n
        assert len(set(sample)) == n

    sample = test_dist.sample_unique(len(OPTIONS)+1)
    assert len(sample) == len(OPTIONS)
    assert len(set(sample)) == len(OPTIONS)