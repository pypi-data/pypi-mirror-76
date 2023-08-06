import signal
import sys
from lollygag.app import LollygagApplication


def ctrl_c_capture(sig, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, ctrl_c_capture)
    App = LollygagApplication()
    App.run()

if __name__ == "__main__":
    main()
