from django.contrib.auth import get_user_model

TEST_USERNAME = "test_user@example.com"
TEST_PASSWORD = "P45290d."

def create_user_util(email=None, password=None):
    """[summary]
    Utility for create a user, returns the create user.
    [description]

    Arguments:
        email {[string]} -- [the user email]
        password {[string]} -- [the user password]
    """
    if email is None:
        email = TEST_USERNAME
    if password is None:
        password = TEST_PASSWORD

    User = get_user_model()
    user = User(
        email=email,
        username=email,
    )

    user.set_password(password)
    user.save()
    return user
