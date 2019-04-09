class CallError(Exception):

    def __init__(self, *, wrong='', correct='', err='', args=None):
        self.wrong = wrong
        self.correct = correct
        self.error = err
        self.args = args or []
