from resources.user.User import User


def is_able_to_login(username: str, hash_password: str) -> bool:
    with open('../../app_conf_files/username.txt', 'rt') as file:
        for line in file.readline():
            if username == line.split(' ')[0] and hash_password == line.split(' ')[1]:
                return True
    return False


def get_user(username: str, hash_password: str, ssh_password: str = None) -> User | None:
    if not is_able_to_login(username, hash_password):
        return None

    if ssh_password is None:
        return User(username=username)

    return User(username=username, ssh_password=ssh_password)
