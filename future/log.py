import logging
import sys

root_logger = logging.getLogger()

formatter = logging.Formatter(
    "%(asctime)s %(pathname)s:%(lineno)s %(funcName)s [%(process)d] %(message)s"
)
# log_file = sys.stdout
# file_handler = logging.FileHandler(log_file)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logging.info('haha')
