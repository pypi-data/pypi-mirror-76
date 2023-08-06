import MESAPC._MESAPC.MESAPC as mpc
import sys

def main(argv):
    if argv[-1] in ['tracker', 'Tracker']:
        import MESAPC._MESAPC.Tracker
    else:
        mpc.MESAPC()

if __name__ == '__main__':
  main(sys.argv)
