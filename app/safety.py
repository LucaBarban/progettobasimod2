from flask_bcrypt import Bcrypt as Bcrypt  # type: ignore
from flask_wtf.csrf import CSRFProtect as CSRFProtect  # type: ignore

# __all__ = ['bcrypt', 'csrf']

bcrypt: Bcrypt = Bcrypt()
csrf: CSRFProtect = CSRFProtect()
