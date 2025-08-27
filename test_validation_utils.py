import validation


def test_validate_uuid_accepts_uppercase():
    assert validation.validate_uuid('95EF01B7-EBFD-4320-A41B-9550E88551B5')
    assert validation.validate_uuid('95ef01b7-EBFD-4320-A41B-9550e88551b5')


def test_validate_uuid_rejects_invalid():
    assert not validation.validate_uuid('not-a-uuid')
    assert not validation.validate_uuid('123')
