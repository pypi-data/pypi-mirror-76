import os
import threading
import signal


class ActivityWatcher:
    def __init__(self, timeout):
        self._timeout = timeout
        self._inactive = True
        self._inactive_lock = threading.Condition()
        self._inactive_check_running = True

    def keep_alive(self):
        self._inactive = False

    def start(self):
        threading.Thread(target=self.auto_close).start()

    def stop(self):
        with self._inactive_lock:
            self._inactive_check_running = False
            self._inactive_lock.notify()

    def auto_close(self):
        with self._inactive_lock:
            while self._inactive_check_running:
                self._inactive_lock.wait(self._timeout)

                if self._inactive:
                    print('\nClosed due to inactivity')
                    os.kill(os.getpid(), signal.SIGINT)
                    break

                self._inactive = True
