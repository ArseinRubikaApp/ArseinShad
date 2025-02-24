from threading import Thread


class GetDataMethod(Thread):
    def __init__(self, target = None, args = ()):
        super().__init__(target = target, args = args)
        self._getdata = None

    def run(self):
        if self._target is not None:
            self._getdata = self._target(*self._args)

    def show(self):
        super().start()
        super().join()
        return self._getdata
