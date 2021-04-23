"""
Code assignment for Problem 3: MERCHANT'S GUIDE TO THE GALAXY.
The code reads input.txt file as an input, parse it into
1) dictionary "intergalactic" <-> Roman numbers
2) prices of goods in "intergalactic" units
3) queries for good's prices in arabic numbers
3) unrecognized lines
and writes output.txt file, containing results
of the queries and error messages for unrecognized lines.
Error lines are written to error.txt file. 
"""

import os

roman_to_arabic_digits = {"i": 1, "v": 5, "x": 10, "l": 50,
                          "c": 100, "d": 500, "m": 1000}


def read_input(workdir=""):
    """Read file input.txt in the working directory."""

    with open(os.path.join(workdir, "input.txt"), "r", encoding="utf-8") as f:
        return(f.read())

def sort_lines(input_text):
    """Sort input text to lists of lines, containing
    i) Intergalactic-Roman dictionary; ii) goods prices; 
    iii) queries; iv) unrecognized lines."""

    dict_list = []
    price_list = []
    query_list = []
    unknown_list = []

    for line in input_text.split("\n"):
        words = line.lower().split()

        if not words:
            continue  # skip empty lines

        if len(words) == 3 and words[1] == "is":  # Dictionary line
            dict_list.append(words)
            continue

        if len(words) >= 5 and words[-1] == "credits" and words[-3] == "is":
            price_list.append(words)  # Price list line
            continue

        if words[-1] == "?":   # Query line
            query_list.append(words)
            continue

        # Unrecognized line:
        unknown_list.append(words + ["REJECTED by sort_lines"])

    return(dict_list, price_list, query_list, unknown_list)


def validate_dict(dict_list, unknown_list):
    """Checks whether third position of dictionary
    string contains correct single Roman numeral.
    Correct entries returned as first element of output tuple,
    and incorrect as the second element of output tuple."""

    dict_out = []
    for dict_entry in dict_list:
        if len(dict_entry[2]) != 1 or dict_entry[2] \
           not in roman_to_arabic_digits:
            unknown_list.append(dict_entry + ["REJECTED by validate_dict"])
            continue
        dict_out.append(dict_entry)
    return(dict_out, unknown_list)


def validate_price(price_list, unknown_list, intergal_roman_dict):
    """Checks whether third word of price line from the end contains
    correct non-negative decimal number. Correct entries returned
    as first element of output tuple, and incorrect as the second
    element of output tuple."""

    price_out = []
    for price_entry in price_list:
        quantity_intergalactic = price_entry[0:-4]
        try:
            int_quantity = intergalactic_to_int(quantity_intergalactic,
                                                intergal_roman_dict)
        except ValueError:
            unknown_list.append(price_entry + [
                "REJECTED by validate_price: incorrect Intergalactic quantity "
                "\'{0}\' in validate_price".format(", "
                    .join(quantity_intergalactic))])
            continue
        
        # change "," to "."
        price_entry_dot = price_entry[-2].replace(',', '.', 1)
        try:
            price_float = float(price_entry_dot)
            if price_float >= 0:
                price_out.append(price_entry)
            else:  # negative price: rejecting
                unknown_list.append(price_entry + [
                    "REJECTED by validate_price: negative price"])
                continue
        except ValueError:  # could not convert price to float: rejecting
            unknown_list.append(price_entry + [
                "REJECTED by validate_price: cannot convert price to float"])
            continue
    return(price_out, unknown_list)


def create_intergal_roman_dict(dict_list):
    """Returns dictionary {Intergalactic numerals: Roman symbols}.
    If contradictory dictionary entries exist, execution stops."""

    intergal_roman_dict = {}
    for dict_entry in dict_list:
        if dict_entry[0] not in intergal_roman_dict:
            intergal_roman_dict[dict_entry[0]] = dict_entry[2]
        elif intergal_roman_dict[dict_entry[0]] == dict_entry[2]:
            continue  # diplicating entry in dictionary; do nothing
        else:  # contradicting entries in input dictionary, stop execution
            raise SystemExit("Contradicting entries in input dictionary!")
    return(intergal_roman_dict)


def int_to_roman(int_input):
    """Convert integer number to Roman
    using straightforvard algorithm."""

    if not isinstance(int_input, int):
        raise ValueError("non-integer input in int_to_roman")
    if int_input < 0 or int_input >= 4000:
        raise ValueError("Roman number should be in 1:3999 range in "
                         "int_to_roman")
    
    # int_roman:sym_roman dictionary:
    dict_int_to_roman = {1000: "m", 900: "cm", 500: "d", 400: "cd", 100: "c",
                         90: "xc", 50: "l", 40: "xl", 10: "x", 9: "ix",
                         5: "v", 4: "iv", 1: "i"}
    out_roman = []
    for (int_roman, sym_roman) in dict_int_to_roman.items():
        # how many times int_roman number fits in input:
        count_roman_symbol = int(int_input / int_roman)
        # add count_roman_symbol of sym_roman symbols to result:
        out_roman.append(sym_roman * count_roman_symbol)
        # decrease input integer by added output number:
        int_input -= int_roman * count_roman_symbol
    return("".join(out_roman))


def not_in_dict(input_list, input_dict):
    """Return elements of input_list not being keys of input_dict."""

    if len(input_list) > 1:  # list with at least 2 elements
        result = [i for i in input_list if i not in input_dict]
    elif len(input_list) == 1:  # list with 1 element
        result = [input_list[0] if input_list[0] not in input_dict else ""]
    else:  # list with no elements
        raise SystemExit("Empty input_list in not_in_dict!")
    return(result)


def intergalactic_to_int(intergalactic_number, intergal_roman_dict):
    """Returns integer representation of the given intergalactic number
    using provided Intergalactic -> Roman dictionary."""

    out_sum = 0
    for i in range(len(intergalactic_number)):

        if not_in_dict([intergalactic_number[i]], intergal_roman_dict) != [""]:
            raise ValueError(
                "intergalactic_to_int: intergalactic numeral \'{0}\' not found"
                " in intergal_roman_dict".format(intergalactic_number[i]))

        # Convert i'th Intergalactic numeral -> Roman numeral -> Integer number
        digit_roman = intergal_roman_dict[intergalactic_number[i]]
        digit_value = roman_to_arabic_digits[digit_roman]

        if i+1 < len(intergalactic_number):  # not the last "digit"

            if not_in_dict(
                    [intergalactic_number[i+1]], intergal_roman_dict) != [""]:
                raise ValueError(
                    "intergalactic_to_int: intergalactic numeral \'{0}\' "
                    "not found in intergal_roman_dict"
                    .format(intergalactic_number[i]))

            # Convert i+1'th Intergalactic -> Roman -> Integer
            digit_roman_next = intergal_roman_dict[intergalactic_number[i+1]]
            digit_value_next = roman_to_arabic_digits[digit_roman_next]

            if digit_value_next > digit_value:
                out_sum -= digit_value  # preceeding larger value, substracting
            else:
                out_sum += digit_value

        else:  # last "digit", only adding possible
            out_sum += digit_value

    # convert Intergalactic input to Roman numeral:
    input_roman = "".join([intergal_roman_dict[x] 
                           for x in intergalactic_number])
    try:
        # correctness check: integer result should be converted back
        # to the same Roman numeral using straightforward algorithm:
        if input_roman == int_to_roman(out_sum):
            return(out_sum)
        else:
            raise ValueError("input is not valid Intergalactic number")
    except ValueError:
        raise ValueError("input number should be in 1:3999 range") 


def calculate_goods_prices(price_list, intergal_roman_dict):
    """"Returns dictionary {name of good: price of good unit (float)}.
    If contradictory price entries exist, execution stops."""

    goods_prices = {}
    for price_entry in price_list:
        if price_entry[-4] not in goods_prices:  # new good found in price_list
            good_name = price_entry[-4]
            price_total = float(price_entry[-2])
            quantity_intergalactic = price_entry[0:-4]
            quantity_int = intergalactic_to_int(quantity_intergalactic,
                                                intergal_roman_dict)
            price_of_unit = price_total / quantity_int
            goods_prices[good_name] = price_of_unit

        else:  # the good already exist in the price list
            # Check whether the unit price is the same 
            # as in previous entry for the specified good.
            price = float(price_entry[-2])
            quantity_intergalactic = price_entry[0:-4]
            quantity_int = intergalactic_to_int(quantity_intergalactic,
                                                intergal_roman_dict)
            price_of_unit = price_total / quantity_int
            if (price_of_unit == goods_prices[price_entry[-4]]):
                continue  # the price is the same, do nothing
            else:  # contradicting entries in input prices, stop execution
                raise SystemExit("Contradicting entries in input prices!")

    return(goods_prices)


def run_queries(query_list, intergal_roman_dict, goods_prices):
    """Determines type of query (number conversion or price query),
       validate query and return query results and error messages"""

    out_txt = []
    for query in query_list:
        if query[0:3] == ["how", "much", "is"]:  # number conversion
            try:
                out_number = intergalactic_to_int(query[3:-1],
                                                  intergal_roman_dict)
                out_txt.append(" ".join(query[3:-1]) +
                               " is " + str(out_number))
            except ValueError:
                error_message = "Invalid Intergalactic number \'{0}\' found "\
                                "in the query".format(" ".join(query[3:-1]))
                out_txt.append(error_message)

        elif query[0:4] == ["how", "many", "credits", "is"]:  # price query
            unpriced_goods = not_in_dict([query[-2]], goods_prices)
            if unpriced_goods != [""]:
                error_message =\
                    "No correct price found in input for good \'{0}\'"\
                    .format(", ".join([x.capitalize()
                            for x in unpriced_goods]))
                out_txt.append(error_message)
                continue
            try:
                good = query[-2]
                quantity_intergalactic = query[4:-2]
                price_total = goods_prices[good] * intergalactic_to_int(
                    quantity_intergalactic, intergal_roman_dict)

                if price_total % 1 == 0:  # integer price
                    price_out = str(int(price_total))
                else:
                    price_out = "{:.4f}".format(price_total)

                out_txt.append(" ".join(quantity_intergalactic) + " " +
                               good.capitalize() + " is " +
                               price_out + " Credits")
            except ValueError:
                error_message =\
                    "Invalid Intergalactic number \'{0}\' found in "\
                    "the query".format(" ".join(query[4:-2]))
                out_txt.append(error_message)

        else:  # unrecognized query type
            err_msg_query = "I have no idea what you are talking about"
            out_txt.append(err_msg_query)

    return(out_txt)


def write_out(workdir, file_name, out_txt):
    """Write output to 'file_name' file in workdir directory"""

    with open(os.path.join(workdir, file_name), "w", encoding="utf-8") as f:
        f.write("\n".join(out_txt))
    pass


def main(workdir=""):
    """Entry point to the app"""

    # Read input file:
    input_text = read_input(workdir)

    # Sort lines of the input to dictionary, prices, queries and unrecognized:
    dict_list, price_list, query_list, unknown_list = sort_lines(input_text)

    # Validate dictionary lines:
    dict_list, unknown_list = validate_dict(dict_list, unknown_list)

    # Create Intergalactic numeral -> Roman Numeral dictionary:
    intergal_roman_dict = create_intergal_roman_dict(dict_list)

    # Validate price lines:
    price_list, unknown_list = validate_price(price_list, unknown_list,
                                              intergal_roman_dict)
   
    # Calculate unit prices for all goods with valid price lines:
    goods_prices = calculate_goods_prices(price_list, intergal_roman_dict)

    # Execute queries:
    out_txt = run_queries(query_list, intergal_roman_dict, goods_prices)

    # Write query responces to the output.txt file: 
    write_out(workdir, "output.txt", out_txt)

    # Write erroneous input lines with error messages to the errors.txt file:
    merged_unknown_list = [" ".join(x) for x in unknown_list] + ["\n"]
    write_out(workdir, "errors.txt", merged_unknown_list)

    return(0)


if __name__ == "__main__":
    """ The code is executed from the command line """
    main()

