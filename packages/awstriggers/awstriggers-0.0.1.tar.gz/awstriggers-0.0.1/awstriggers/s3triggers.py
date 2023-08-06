from .exceptions import WrongInputException


class S3Trigger():
    """Get information from a S3 trigger record.

    Args:
        record (dic): trigger record.

    Exceptions:
            WrongInputException
    """

    def __init__(self, record):
        self.__record = record
        try:
            self.__bucket = self.__record['s3']['bucket']['name']
            key = self.__record['s3']['object']['key']
            self.__key = key.replace('+', ' ')
            self.__event = self.__record['eventName']
            self.__timestamp = self.__record['eventTime']
        except Exception:
            raise WrongInputException('S3 record')

    @property
    def bucket(self):
        return self.__bucket

    @property
    def key(self):
        return self.__key

    @property
    def event(self):
        return self.__event

    @property
    def timestamp(self):
        return self.__timestamp
