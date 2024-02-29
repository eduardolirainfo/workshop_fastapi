import pytest
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.mark.order(1)
def test_user1_follow_user(api_client_user1, api_client_user2):
    """User 1 follows user 2"""
    response = api_client_user1.post(
        "/follow/2",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user1"
    assert result["following"][0]["username"] == "user2"


@pytest.mark.order(2)
def test_user2_follow_user(api_client_user1, api_client_user2):
    """User 2 follows user 1"""
    response = api_client_user2.post(
        "/follow/1",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user2"
    assert result["following"][0]["username"] == "user1"


@pytest.mark.order(3)
def test_user1_unfollow_user(api_client_user1, api_client_user2):
    """User 1 unfollows user 2"""
    response = api_client_user1.delete(
        "/follow/2",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user1"
    assert result["following"] == []


@pytest.mark.order(4)
def test_user2_unfollow_user(api_client_user1, api_client_user2):
    """User 2 unfollows user 1"""
    response = api_client_user2.delete(
        "/follow/1",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user2"
    assert result["following"] == []


@pytest.mark.order(5)
def test_user1_list_following(api_client_user1, api_client_user2):
    """User 1 list following"""
    response = api_client_user1.get(
        "/user/user1/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user1"
    assert result["following"] == []


@pytest.mark.order(6)
def test_user2_list_following(api_client_user1, api_client_user2):
    """User 2 list following"""
    response = api_client_user2.get(
        "/user/user2/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user2"
    assert result["following"] == []


@pytest.mark.order(7)
def test_user1_list_followers(api_client_user1, api_client_user2):
    """User 1 list followers"""
    response = api_client_user1.get(
        "/user/user1/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user1"
    assert result["followers"] == []


@pytest.mark.order(8)
def test_user2_list_followers(api_client_user1, api_client_user2):
    """User 2 list followers"""
    response = api_client_user2.get(
        "/user/user2/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user2"
    assert result["followers"] == []


@pytest.mark.order(9)
def test_user1_list_following_and_followers(api_client_user1, api_client_user2):
    """User 1 list following and followers"""
    response = api_client_user1.get(
        "/user/user1/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user1"
    assert result["following"] == []
    assert result["followers"] == []


@pytest.mark.order(10)
def test_user2_list_following_and_followers(api_client_user1, api_client_user2):
    """User 2 list following and followers"""
    response = api_client_user2.get(
        "/user/user2/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user2"
    assert result["following"] == []
    assert result["followers"] == []


@pytest.mark.order(11)
def test_user1_list_following_and_not_followers(api_client_user1, api_client_user2):
    """User 1 list following and not followers"""
    response = api_client_user1.get(
        "/user/user1/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user1"
    assert result["following"] == []
    assert result["followers"] == []


@pytest.mark.order(12)
def test_user2_list_following_and_not_followers(api_client_user1, api_client_user2):
    """User 2 list following and not followers"""
    response = api_client_user2.get(
        "/user/user2/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user2"
    assert result["following"] == []
    assert result["followers"] == []


@pytest.mark.order(13)
def test_user1_list_followers_and_not_following(api_client_user1, api_client_user2):
    """User 1 list followers and not following"""
    response = api_client_user1.get(
        "/user/user1/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user1"
    assert result["following"] == []
    assert result["followers"] == []


@pytest.mark.order(14)
def test_user2_list_followers_and_not_following(api_client_user1, api_client_user2):
    """User 2 list followers and not following"""
    response = api_client_user2.get(
        "/user/user2/",
    )
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "user2"
    assert result["following"] == []
    assert result["followers"] == []
