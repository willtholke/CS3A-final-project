""" This program has been modified since its last version such that
the new global string object called 'filename' (which refers to the
new airbnb data source, 'AB_NYC_2019.csv') is utilized in load_file(),
the new method in the DataSet class that loads data from filename.

Date: 03/21/2021

Error Notes: added InvalidDataLength class to the DataSet class
(lines 96, 97) as a logical error to be raised (lines 178-180) if the
length of the file referred to by 'filename' is not 48895.

Other Notes: set global variable line_count equal to len(self.data) to
avoid "Expected type 'Sized', got 'None' instead" error that occurred
when attempting to print len(self.data) on line 477. The value of
line_count is manipulated twice in the program, which does not affect
the output in any unintended way.
"""

from copy import deepcopy
from enum import Enum
from statistics import mean
import csv
import time


class style:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ITALICS = '\033[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


""" Global Variables. """
filename = './AB_NYC_2019.csv'
home_currency = ""
line_count = 0
conversions = {
    "USD": 1,
    "EUR": .9,
    "CAD": 1.4,
    "GBP": .8,
    "CHF": .95,
    "NZD": 1.66,
    "AUD": 1.62,
    "JPY": 107.92
    }

with open("main.py", "r") as file:
    for line in file:
        if line != "\n":
            line_count += 1

help_command = {
    "header": "must be less than 30 characters in length",
    "lines": "there are " + style.DARKCYAN + str(line_count) +
             style.END + " lines of code in " + file.name +
             "! (including docstrings)",
    "contact": style.BOLD + style.UNDERLINE + "Email:" + style.END +
              " tholkewilliam@fhda.edu"
}


class DataSet:
    copyright = "No copyright has been set."

    def __init__(self, header=""):
        self.data = None
        self._labels = {
            DataSet.Categories.LOCATION: set(),
            DataSet.Categories.PROPERTY_TYPE: set()
        }
        self._active_labels = {
            DataSet.Categories.LOCATION: set(),
            DataSet.Categories.PROPERTY_TYPE: set()
        }
        try:
            self._header = header
        except ValueError:
            pass

    class EmptyDatasetError(Exception):
        pass

    class NoMatchingItems(Exception):
        pass

    class InvalidDataLength(Exception):
        pass

    class Categories(Enum):
        LOCATION = 0
        PROPERTY_TYPE = 1

    class Stats(Enum):
        MIN = 0
        AVG = 1
        MAX = 2

    @staticmethod
    def bubble_sort(list_to_sort: list):
        """ Recursively sort the parameter list_to_sort. """
        sorted_list = list_to_sort[:]
        iteration_num = 0
        for n in range(len(sorted_list) - 1):
            if sorted_list[n] > sorted_list[n + 1]:
                sorted_list[n], sorted_list[n + 1] = sorted_list[n + 1], \
                                                     sorted_list[n]
                iteration_num += 1
        if iteration_num == 0:
            return sorted_list
        else:
            return DataSet.bubble_sort(sorted_list)

    @property
    def header(self):
        """ Return self._header. """
        return self._header

    @header.setter
    def header(self, header: str):
        """ Check whether the proposed header is a string and has
        length equal to 0 or 30.
        """
        if len(header) != 0 and len(header) <= 30:
            self._header = header
        else:
            raise ValueError

    def load_file(self):
        """ Load data from 'AB_NYC_2019.csv' into self._data. """
        try:
            with open(filename, 'r', newline='') as data:
                reader = csv.reader(data)
                self.data = [(i[1], i[2], int(i[3])) for i in reader if i[3] != "price"]
            self._initialize_sets()
        except FileNotFoundError:
            raise FileNotFoundError

    def load_default_data(self):
        """ Assign list of tuples to self._data. """
        self.data = [("Staten Island", "Private room", 70),
                     ("Brooklyn", "Private room", 50),
                     ("Bronx", "Private room", 40),
                     ("Brooklyn", "Entire home / apt", 150),
                     ("Manhattan", "Private room", 125),
                     ("Manhattan", "Entire home / apt", 196),
                     ("Brooklyn", "Private room", 110),
                     ("Manhattan", "Entire home / apt", 170),
                     ("Manhattan", "Entire home / apt", 165),
                     ("Manhattan", "Entire home / apt", 150),
                     ("Manhattan", "Entire home / apt", 100),
                     ("Brooklyn", "Private room", 65),
                     ("Queens", "Entire home / apt", 350),
                     ("Manhattan", "Private room", 98),
                     ("Brooklyn", "Entire home / apt", 200),
                     ("Brooklyn", "Entire home / apt", 150),
                     ("Brooklyn", "Private room", 99),
                     ("Brooklyn", "Private room", 120)]
        self._initialize_sets()

    def _initialize_sets(self):
        """ Raise error if no data is loaded. Otherwise, assign set
        comprehension of locations and property types from self.data
        to the key of each object within self._labels & set
        self.active_labels to a deepcopy of self._labels.
        """
        global line_count
        line_count = len(self.data)
        if line_count != 48895:
            self.data = None
            raise DataSet.InvalidDataLength
        if self.data is None:
            raise DataSet.EmptyDatasetError
        self._labels[DataSet.Categories.LOCATION] = {location[0] for
                                                     location in
                                                     self.data}
        self._labels[DataSet.Categories.PROPERTY_TYPE] = {prop_type[1] for
                                                          prop_type in
                                                          self.data}
        self._active_labels = deepcopy(self._labels)

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        """ Use list comprehension to create list of rents for all
        properties that match parameters, then return minimum, average,
        and max rent rounded to the hundredth decimal place in tuple.
        """
        if self.data is None:
            raise DataSet.EmptyDatasetError
        rent_list = [descriptor[2] for descriptor in self.data if
                     descriptor[0] == descriptor_one and
                     descriptor[1] == descriptor_two]
        if not rent_list:
            raise DataSet.NoMatchingItems
        return format(float(min(rent_list)), '.2f'), format(
            float(mean(rent_list)), '.2f'), format(
            float(max(rent_list)), '.2f')

    def _table_statistics(self, row_category: Categories, label: str):
        """ Given valid parameters, calculate the min, max, and avg
        rent for properties within those parameters.
        """
        a, b = (0, 1) if row_category == DataSet.Categories.LOCATION else \
            (1, 0)
        rent = [item[2] for item in self.data if item[a] in
                self._active_labels[row_category] and label == item[b]]
        if len(rent) == 0:
            raise ValueError
        else:
            return format(float(min(rent)), '.2f'), format(
                float(mean(rent)), '.2f'), format(
                float(max(rent)), '.2f')

    def display_field_table(self, rows: Categories):
        """ Display a table of the min, max, and avg rent for each
        item in that category.
        """
        location = DataSet.bubble_sort(
            list(self._labels[DataSet.Categories.LOCATION]))
        prop_list = DataSet.bubble_sort(
            list(self._labels[DataSet.Categories.PROPERTY_TYPE]))
        if self.data is None:
            raise DataSet.EmptyDatasetError
        else:
            print("The following data are from properties matching these"
                  " criteria:")
            for x in self.get_active_labels(rows):
                print(f'- {x}')
            if len(self.get_active_labels(rows)) == 0:
                print("- No active criteria")
            print(f'{"Minimum":>27}{"Average":>16}{"Maximum":>16}')
            iterable = prop_list if rows == DataSet.Categories.LOCATION else \
                location
            for item in iterable:
                print(f'{item:20}', end='')
                for iteration_num in range(0, 3):
                    try:
                        call = self._table_statistics(rows, str(item))
                        print(f'$ {call[iteration_num]:14}',
                              end='')
                    except ValueError:
                        print(f'{"N/A":16}', end='')
                print()
            print()

    def get_labels(self, category: Categories):
        """ Return a list of the items in _labels[category]. """
        return list(self._labels[category])

    def get_active_labels(self, category: Categories):
        """ Return a list of the items in _active_labels[category]. """
        return list(self._active_labels[category])

    def toggle_active_label(self, category: Categories, descriptor: str):
        """ Add or remove labels from _active_labels. """
        if descriptor not in self._labels[category]:
            raise KeyError
        elif descriptor not in self._active_labels[category]:
            self._active_labels[category].add(descriptor)
        elif descriptor in self._active_labels[category]:
            self._active_labels[category].remove(descriptor)

    def display_cross_table(self, stat: Stats):
        """ Convert the key of each object in _active_labels from
        set to list, order lists 'location' and 'x' independently,
        and print a table of rates for each borough & property type
        depending on whether stat is Stats.MIN, Stats.AVG, or
        Stats.MAX.
        """
        location = DataSet.bubble_sort(
            list(self._labels[DataSet.Categories.LOCATION]))
        property_type = DataSet.bubble_sort(
            list(self._labels[DataSet.Categories.PROPERTY_TYPE]))
        if self.data is None:
            raise DataSet.EmptyDatasetError
        else:
            print(f'{"":15}', end='')
            for item in property_type:
                print(f'{item:21}', end="")
            print()
            for item_1 in location:
                print(f'{item_1:15}', end='')
                for item_2 in property_type:
                    try:
                        call = self._cross_table_statistics(item_1, item_2)
                        print(f'$ {call[stat.value]:19}', end='')
                    except DataSet.NoMatchingItems:
                        print(f'{"N/A":21}', end='')
                print()
        print()


def manage_filters(dataset: DataSet, category: DataSet.Categories):
    """ Print a menu-like list of all labels for the 'category'
    parameter, test whether its active, and allow user to change
    its status.
    """
    if dataset.data is None:
        raise DataSet.EmptyDatasetError
    enum_list = {}
    if len(enum_list) != 0:
        enum_list = {}
    val = DataSet.get_labels(dataset, category)
    val.sort()
    print("The following labels are in the dataset:")
    for a, b in enumerate(val, 1):
        if b in DataSet.get_active_labels(dataset, category):
            print(f'{a}: {b:20} ACTIVE')
        else:
            print(f'{a}: {b:20} INACTIVE')
        enum_list[a] = b
    while True:
        error = style.RED + f'Please enter a number between 1 ' \
                                 f'and {len(enum_list)}!' + style.END
        user_input = input("Please select an item to toggle or enter a "
                           "blank line when you are finished: ")
        if user_input == "":
            print()
            break
        try:
            int_input = int(user_input)
            if int_input in enum_list:
                dataset.toggle_active_label(category, enum_list[int_input])
                print("The following labels are in the dataset:")
                for a, b in enumerate(val, 1):
                    if b in DataSet.get_active_labels(dataset, category):
                        print(f'{a}: {b:20} ACTIVE')
                    else:
                        print(f'{a}: {b:20} INACTIVE')
            else:
                print(error)
        except ValueError:
            print(error)


def main():
    """ Set DataSet.copyright, obtain the user's name if not guest
    user, print it in a welcome statement, allow the user to access
    help menu, call @header.setter to confirm user header entry,
    obtain the user's home currency, and call menu().
    """
    DataSet.copyright = "-- Copyright © 2021 by William Tholke --"
    air_bnb = DataSet()
    global home_currency
    user_name = input("Welcome to the airbnb database! To get started, "
                      "please enter your name: ")
    if user_name == "":
        print(f"Logged in as {style.DARKCYAN}guest user{style.END}.")
        user_name = "Guest User"
    else:
        print(f"Welcome {style.DARKCYAN + user_name + style.END}!", end=" ")
    user_input = None
    input_msg = "Enter /help or enter a header: "
    while user_input is None:
        try:
            user_input = input(input_msg)
            if user_input == "/help":
                print(style.ITALICS + "* type /help {command} for help\n" +
                      style.END + style.UNDERLINE + "Help Menu:" + style.END)
                for a, (b, c) in enumerate(help_command.items(), 1):
                    print(f'{a}) {b}')
            if "/" in user_input:
                args = user_input.split(' ')
                if args[0] == '/help':
                    try:
                        if args[1] in help_command.keys():
                            print(f'- {help_command[args[1]]}')
                            user_input = None
                        else:
                            print("Invalid help command.")
                            user_input = None
                    except IndexError:
                        user_input = None
                elif user_input[0] != "/":
                    pass
                elif user_input.count("/") > 1:
                    print("I don't recognize that command.")
                    user_input = None
                    continue
                else:
                    print("I don't recognize that command.")
                    user_input = None
                    continue
            else:
                air_bnb.header = user_input
        except ValueError:
            print(f'Invalid entry!', end=" ")
            user_input = None
    while True:
        home_currency = input("Please enter your home currency: ")
        if home_currency.upper() in conversions:
            break
        elif len(home_currency) == 0:
            print(f'Invalid entry.', end=" ")
            continue
        else:
            print(f'[{home_currency}] is an invalid currency.')
            continue
    print(f"Loading {user_name}'s currency table", end="")
    delayed_loading(0.7, 0.2), print(), menu(air_bnb)


def delayed_loading(sleep_time: float, reduce_time: float):
    """ Print 3 periods with increasing frequency to emphasize
    loading.
    """
    for x in range(0, 3):
        time.sleep(sleep_time)
        print(f".", end="")
        sleep_time -= reduce_time
    print()


def menu(dataset: DataSet):
    """ Call currency_options(home_currency), print the copyright,
    print the header at the top of the menu, convert user input to int,
    catch the error if user input is inconvertible, and allow user to
    choose from menu.
    """
    currency_options(home_currency)
    print(f'{DataSet.copyright}', "\n")
    output = None
    while True:
        print(dataset.header)
        print_menu()
        if output is not None:
            print(output)
        user_input = input("Please input a choice from the menu above: ")
        print("\n")
        try:
            int_answer = int(user_input)
        except ValueError:
            output = "Please enter a number from the menu."
            continue
        if int_answer == 1:
            try:
                dataset.display_cross_table(dataset.Stats.AVG)
                output = None
            except dataset.EmptyDatasetError:
                output = "Please load data."
        elif int_answer == 2:
            try:
                dataset.display_cross_table(dataset.Stats.MIN)
                output = None
            except dataset.EmptyDatasetError:
                output = "Please load data."
        elif int_answer == 3:
            try:
                dataset.display_cross_table(dataset.Stats.MAX)
                output = None
            except dataset.EmptyDatasetError:
                output = "Please load data."
        elif int_answer == 4:
            try:
                dataset.display_field_table(dataset.Categories.PROPERTY_TYPE)
                output = None
            except dataset.EmptyDatasetError:
                output = "Please load data."
        elif int_answer == 5:
            try:
                dataset.display_field_table(dataset.Categories.LOCATION)
                output = None
            except dataset.EmptyDatasetError:
                output = "Please load data."
        elif int_answer == 6:
            try:
                manage_filters(dataset, dataset.Categories.LOCATION)
                output = None
            except dataset.EmptyDatasetError:
                output = "Please load data."
        elif int_answer == 7:
            try:
                manage_filters(dataset, dataset.Categories.PROPERTY_TYPE)
                output = None
            except dataset.EmptyDatasetError:
                output = "Please load data."
        elif int_answer == 8:
            if dataset.data is None:
                try:
                    dataset.load_file()
                    output = f'{line_count} lines loaded!'
                except FileNotFoundError:
                    output = f'{filename} does not exist!'
                except DataSet.InvalidDataLength:
                    output = f'{filename} not 48895 lines!'
            else:
                output = "You have already loaded this data."
        elif int_answer == 9:
            print("Program has been quit.")
            exit(0)
        else:
            output = "Please enter a number between 1 and 9."


def currency_converter(quantity: float, source_curr: str, target_curr: str):
    """ Calculate value after converting money from one currency to
    another.

    quantity -> a float representing the amount of currency to convert
    source_curr -> a three letter currency identifier string from the
        conversions dictionary
    target_curr -> a three letter currency identifier string from the
        conversions dictionary
    """
    return(quantity * conversions[target_curr]) / conversions[source_curr]


def currency_options(base_curr: str):
    """ Print out a table of options for converting base_curr to all
    other currencies with quantities from 10 to 90.
    """
    print(f'Options for converting from {base_curr.upper()}:')
    print(f'{base_curr.upper():12}', end="")
    for key in conversions:
        if key == base_curr.upper():
            continue
        print(f'{key:12}', end="")
    print()
    for q in range(10, 100, 10):
        print(f'{q:<12.2f}', end="")
        for tc in conversions:
            if tc == base_curr.upper():
                continue
            print(f'{currency_converter(q, base_curr.upper(), tc):<12.2f}',
                  end="")
        print()
    print()


def print_menu():
    """ Print out nine choices. """
    print("Main Menu:")
    print("1 - Print Average Rent by Location and Property Type")
    print("2 - Print Minimum Rent by Location and Property Type")
    print("3 - Print Maximum Rent by Location and Property Type")
    print("4 - Print Min/Avg/Max by Location")
    print("5 - Print Min/Avg/Max by Property Type")
    print("6 - Adjust Location Filters")
    print("7 - Adjust Property Type Filters")
    print("8 - Load Data")
    print("9 - Quit")


if __name__ == "__main__":
    main()
