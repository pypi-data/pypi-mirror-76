from .exceptions import WrongInputException


class SQSTrigger():
    """Get information from a SQS trigger record.

    Args:
        record (dic): SQS trigger record.

    Exceptions:
            WrongInputException
    """

    def __init__(self, record):
        self.__record = record
        try:
            self.__body = self.__record['body']
            self.__attributes = self.__record['messageAttributes']
            self.__id = self.__record['messageId']
            self.__timestamp = self.__record['attributes']['SentTimestamp']
            self.__queue = self.__record['eventSourceARN']
        except Exception:
            raise WrongInputException('Cloudwatch event')

    @property
    def body(self):
        return self.__body

    @property
    def attributes(self):
        return self.__attributes

    @property
    def id(self):
        return self.__id

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def queue(self):
        return self.__queue
