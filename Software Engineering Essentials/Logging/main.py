import logging
import logging_config

logger=logging.getLogger(__name__)

password="123456"
logger.info(f"User entered password: {password}")
logger.info("User logged in with password=Super$ecret123!")
logger.info("password=my_secure_password!@# should be hidden")
logger.info("password: P@ssw0rd2025")