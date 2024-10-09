import pytest

@pytest.mark.parametrize("current_id,get_id", [
    (1, 1)
])
async def test_temp(current_id, get_id):
    assert current_id == get_id