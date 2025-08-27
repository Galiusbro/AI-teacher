from diagnostic_utils import validate_sample


def test_sample_validates_against_schema():
    assert validate_sample(
        "templates/diagnostic_sample_10yo.json",
        "templates/diagnostic.schema.json",
    )
