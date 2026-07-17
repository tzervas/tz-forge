def test_import() -> None:
    import {{project_snake}}  # noqa: F401

    assert {{project_snake}}.__version__
