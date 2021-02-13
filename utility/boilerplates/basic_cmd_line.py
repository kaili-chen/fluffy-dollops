import argparse

def main():
    pass

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    # positional arguments
    ap.add_argument('input', help='an input')

    # optional arguments
    ap.add_argument('-o', '--optional', help='optional flag')

    args = vars(ap.parse_args())

    print(args)

    # accessing input
    print(args['input'])

    # accessing optional
    print(args['optional'])
