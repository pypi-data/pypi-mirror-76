import pytest

from seeq import spy
from seeq.sdk import Configuration, UserOutputV1

from . import test_common


@pytest.mark.system
def test_bad_login():
    test_common.login()

    Configuration().retry_timeout_in_seconds = 0

    assert spy.client is not None
    assert isinstance(spy.user, UserOutputV1)
    assert spy.user.username == 'agent_api_key'

    with pytest.raises(RuntimeError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', url='https://bogus')

    assert spy.client is None
    assert spy.user is None

    with pytest.raises(ValueError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', auth_provider='bogus')

    assert spy.client is None
    assert spy.user is None


@pytest.mark.system
def test_good_login():
    test_common.login()


@pytest.mark.system
def test_credentials_file_with_username():
    with pytest.raises(ValueError):
        spy.login('mark.derbecker@seeq.com', 'DataLab!', credentials_file='credentials.key')
