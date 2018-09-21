
class MemoryBoard:
    def set_owner(self, owner):
        self._owner = owner

    def post_message(self, message):
        """This will post a message to the board."""

    def get_message(self):
        """This will get the next message from the board.
        Boards act like queues, and allow multiple clients
        to write to them.
        """

    def __init__(self):
        self._board = []

    def post_message(self, message):
        self._board.append(message)

        self._board = sorted(self._board,
                             key=lambda a: a.timestamp, reverse=True)

    def get_message(self):
        if(len(self._board) > 0):
            return self._board.pop()
        else:
            return None
