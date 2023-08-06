from .exceptions import WrongInputException


class CloudwatchTrigger():
    """Get information from a Cloudwatch trigger.

    Args:
        event (dic): trigger event.

    Exceptions:
            WrongInputException
    """

    def __init__(self, event):
        self.__event = event
        try:
            self.__source = self.__event['source']
            self.__resource = self.__event['resources']
            self.__timestamp = self.__event['time']
            self.__id = self.__event['id']
            self.__detail = self.__event['detail']
        except Exception:
            raise WrongInputException('Cloudwatch event')

    @property
    def source(self):
        return self.__source

    @property
    def resource(self):
        return self.__resource

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def id(self):
        return self.__id

    @property
    def detail(self):
        return self.__detail
