import bcrypt
import sys
import argparse
import getpass

class PasswordPrompt(argparse.Action):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, parser, args, values, option_string=None):
        try:
            setattr(args, self.dest, getpass.getpass())
        except:
            print('>> Interrupted <<', file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--password', dest='password', help='The password to hash')
parser.add_argument('-P', '--password-prompt', dest='password', action=PasswordPrompt, type=str, nargs=0, help='Prompt for the password to hash')
parser.add_argument('-v', '--verify', type=str, help='Verify with the provided hash.')
args = parser.parse_args()

if not args.password:
    print('Error: Please provide a password.', file=sys.stderr)
    parser.print_usage()
    sys.exit(2)
password = args.password.encode('utf-8')
salt = bcrypt.gensalt()
if args.verify:
    verify = args.verify.encode('utf-8')
    try:
        verify = bcrypt.checkpw(password = password , hashed_password = verify)
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
        sys.exit(1)
    if verify:
        print('Success!', file=sys.stderr)
        sys.exit(0)
    else:
        print('Passwords did not match.', file=sys.stderr)
        sys.exit(1)
else:
    bhash = bcrypt.hashpw(password=password, salt=salt)
    print(bhash.decode(), end='', flush=True)
    print(file=sys.stderr)