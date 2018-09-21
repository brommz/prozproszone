from BaseMessage import BaseMessage


class RequestVoteMessageResponse(BaseMessage):
    _type = BaseMessage.RequestVoteResponse

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data)
