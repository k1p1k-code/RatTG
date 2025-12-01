from core.loader import app, dp
from api import register as reg_api
from bot import register as reg_bot, dp

reg_bot(dp)
reg_api(app)

# fastapi dev --host localhost --port 8000