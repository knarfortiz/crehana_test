from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a given password using the best available hash algorithm.

    This function will automatically upgrade the hash when the default
    algorithm changes. It also allows for the use of other hash algorithms
    if needed.

    :param password: The password to be hashed
    :return: The hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against its hashed version.

    This function uses the hash algorithm defined in the CryptContext
    to check whether the provided plain password matches the given hashed password.

    :param plain_password: The plain text password to verify
    :param hashed_password: The hashed password to compare against
    :return: True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
