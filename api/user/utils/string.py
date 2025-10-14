import secrets
import string


def generate_random_string(length: int = 32) -> str:
    """
    Generates a cryptographically secure random string.

    Args:
        length: The length of the random string to generate.

    Returns:
        A random string of the specified length.
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))