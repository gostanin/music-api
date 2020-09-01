from pathlib import Path

from decouple import config


ROOT_DIR = Path(__file__).parent.parent.absolute()

# change True to False for production
DEBUG = config('DEBUG', default=True, cast=bool)
PORT = config('PORT', default=8000, cast=int)

APPLICATION_ROOT = '/api/v1'

ALLOWED_CORS_ORIGINS = config('ALLOWED_CORS_ORIGINS', default='*')
