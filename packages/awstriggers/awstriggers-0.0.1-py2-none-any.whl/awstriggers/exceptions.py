

class WrongInputException(Exception):
    msg = 'Wrong trigger. This is not a {}.'

    def __init__(self, trigger_type):
        super(WrongInputException, self).__init__(
            self.msg.format(trigger_type)
        )
