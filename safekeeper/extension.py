from common_utils.logger import ActionLogger

from safekeeper.infras.db.connection import DBConnectionHandler

action_logger = ActionLogger()
db = DBConnectionHandler()
