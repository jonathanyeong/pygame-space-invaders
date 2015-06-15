import sys
from getopt import *
from space_invader import *

def main(argv):
    try: 
        opts, args = getopt(argv, 'f')
    except GetoptError as err:
        print str(err)
        sys.exit(2)

    print opts
    Pyvader(opts).main_loop()

if __name__ == "__main__":
    main(sys.argv[1:])
