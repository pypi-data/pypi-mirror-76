import pytest

@pytest.fixture(autouse=True)
def salt_factories_cache_clean(salt_factories):
    yield salt_factories
    for key in salt_factories.cache:
        salt_factories.cache[key].clear()
