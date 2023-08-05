"""Console script for python_benforder."""
import argparse
import sys
import python_benforder as pb


def main():
    """Console script for python_benforder."""
    parser = argparse.ArgumentParser()
    #parser.add_argument('_', nargs='*') # part of the cookie cutter template. detele

    # Optionally, accept input from a file
    parser.add_argument("-f", "--filename", action="store", dest="filename", default=False)
            
    args = parser.parse_args()

    if args.filename:
        # Then ignore stdout and use the file input instead
        with open(args.filename) as data:
            # To clean the data, we make it into an object that cleans each line. 
            # And it will also count the lines and the length
            cleandata = pb.LenGeneratorFile(data)
            print(pb.calculate(cleandata)) # TODO: Pretty print
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
