import orie5270_ozone


def test_package_has_version():
    assert isinstance(orie5270_ozone.__version__, str)
    assert len(orie5270_ozone.__version__) > 0
