def test_package_metadata():
    import nexora
    from nexora import __about__

    assert nexora.__version__ == __about__.__version__
    assert __about__.__version__ == "1.0.0"
    assert __about__.__title__ == "nexora"
