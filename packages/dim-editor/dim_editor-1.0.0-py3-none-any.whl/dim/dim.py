import traceback
from curses import *

from dim.argparser import Argparser
from dim.editor import Editor

def main(stdscr):
    args = Argparser.get_args()
    try:
        Editor(stdscr, args).launch()
    except Exception as e:
        error_type = type(e)
        error_msg = str(e)
        if error_type == SystemError:
            pass
        elif error_type == NotImplementedError:
            print('This feature hasn\'t been implemented yet.\n')
            print('Feature: {error_msg}\n')
        else:
            print('A fatal error has occured.\n')
            if args.debug:
                print(traceback.format_exc())
    finally:
        print('Exited the editor.')

def launch():
    import traceback
    from curses import wrapper
    from dim.argparser import Argparser
    from dim.editor import Editor
    wrapper(main)

if __name__ == '__main__':
    wrapper(main)
