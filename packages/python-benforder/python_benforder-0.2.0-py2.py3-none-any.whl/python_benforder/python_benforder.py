"""Main module."""

import collections


BENFORD_PERCENTAGES = [0, 0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]



import itertools

class LenGeneratorFile(object):
    """ A generator that counts it's lenght as it goes 
    take a file and convert it to  a generator, using readline and cleaning the input.
    """
    def __init__(self,gen):
        """ Take a file IO object as input """
        self._input=gen

    def __iter__(self):
        self.length=0
        return self

    def __next__(self):
        """ Python 3 compat """
        return self.next()

    def next(self):
        self.length = self.length + 1
        line = self._input.readline()
        if line != "":
            return line
        else:
            raise StopIteration("End of the file")

    def _gen(self):
        """ The internal generator that will do the magics """
        line = self._input.readline()
        self.length = self.length + 1
        print(self._input.tell())
        yield line.strip()

    def __len__(self):
        return self.length


def calculate(data):

    """
    Calculates a set of values from the numeric list
    input data showing how closely the first digits
    fit the Benford Distribution.
    Results are returned as a list of dictionaries.
    """

    results = []

    # Take the data, put it in a special generator that counts lenght,
    # make it a string, take the 1st digit, and put it on a list.
    first_digits = list(map(lambda n: str(n)[0], data))
    first_digit_frequencies = collections.Counter(first_digits)

    for n in range(1, 10):

        data_frequency = first_digit_frequencies[str(n)]
        data_frequency_percent = data_frequency / len(data)
        benford_frequency = len(data) * BENFORD_PERCENTAGES[n]
        benford_frequency_percent = BENFORD_PERCENTAGES[n]
        difference_frequency = data_frequency - benford_frequency
        difference_frequency_percent = data_frequency_percent - benford_frequency_percent

        results.append({"n": n,
                        "data_frequency":               data_frequency,
                        "data_frequency_percent":       data_frequency_percent,
                        "benford_frequency":            benford_frequency,
                        "benford_frequency_percent":    benford_frequency_percent,
                        "difference_frequency":         difference_frequency,
                        "difference_frequency_percent": difference_frequency_percent})

    return results
