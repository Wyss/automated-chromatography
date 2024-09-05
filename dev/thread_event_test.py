import threading
import time


class MyClass:
    def __init__(self):
        super(MyClass, self).__init__()
        self.event = threading.Event()


    def delay(self):
        time.sleep(1.2)
        self.event.set()
        return

    def looper(self):
        granularity = 4
        for x in range(4*granularity):
            time.sleep(1.0/granularity)
            print(self.event.is_set())
            if self.event.is_set():
                return
        return

    def auto(self):
        self.event.clear()
        thread1 = threading.Thread(target=self.looper)
        thread2 = threading.Thread(target=self.delay)
        thread1.start()
        time.sleep(0.5)
        thread2.start()
        return

mc = MyClass()
mc.auto()
