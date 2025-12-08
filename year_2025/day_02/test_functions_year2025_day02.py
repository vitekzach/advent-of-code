import pytest

from year_2025.day_02.functions import IdInvalidator


@pytest.mark.parametrize(
    ["start", "end", "invalid_ids"],
    (
        ("11", "22", [11, 22]),
        ("95", "115", [99]),
        ("998", "1012", [1010]),
        ("1188511880", "1188511890", [1188511885]),
        ("222220", "222224", [222222]),
        ("1698522", "1698528", []),
        ("446443", "446449", [446446]),
        ("38593856", "38593862", [38593859]),
        ("1", "2", []),
    ),
)
def test_generate_duplicated_id(
    start: str,
    end: str,
    invalid_ids: list[int],
):
    inf = IdInvalidator()
    inf.crack_duplicated_id(start, end)
    assert inf.invalid_ids == invalid_ids


@pytest.mark.parametrize(
    ["start", "end", "invalid_ids"],
    (
        ("11", "22", [11, 22]),
        ("95", "115", [99, 111]),
        ("998", "1012", [999, 1010]),
        ("1188511880", "1188511890", [1188511885]),
        ("222220", "222224", [222222]),
        ("1698522", "1698528", []),
        ("446443", "446449", [446446]),
        ("38593856", "38593862", [38593859]),
        ("565653", "565659", [565656]),
        ("824824821", "824824827", [824824824]),
        ("1", "2", []),
    ),
)
def test_crack_any(
    start: str,
    end: str,
    invalid_ids: list[int],
):
    inf = IdInvalidator()
    inf.crack_duplicated_ids_any_length(start, end)
    assert inf.invalid_ids_any == invalid_ids
