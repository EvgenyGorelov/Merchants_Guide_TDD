import pytest
from testfixtures import TempDirectory

from main import *


def test_not_in_dict():
    sample_dict = {"glob": "i", "prok": "v",  "pish": "x", "tegj": "l",
                   "fish": "x", "gaa": "m", "c": "c"}

    sample_input = ["glob", "prok",  "pish", "aaa", "123"]
    desired_result = ["aaa", "123"]

    result = not_in_dict(sample_input, sample_dict)
    assert result == desired_result


def test_write_out():
    sample_input = (["pish tegj glob glob is 42",
                     "glob prok Silver is 68 Credits",
                     "glob prok Gold is 57800 Credits",
                     "glob prok Iron is 782 Credits",
                     "I have no idea what you are talking about"])
    sample_file_name = "output.txt"

    with TempDirectory() as d:
        write_out(d.path, sample_file_name, sample_input)
        with open(os.path.join(d.path, sample_file_name), "r",
                  encoding="utf-8") as f:
            written_file = f.read()
            result = written_file.split(sep="\n")
        
    assert result == sample_input


def test_run_queries():
    sample_dict = {"glob": "i", "prok": "v",  "pish": "x", "tegj": "l",
                   "fish": "x", "gaa": "m", "c": "c"}

    sample_prices = {"silver": 17.0, "gold": 14450.0, "iron": 195.5}

    sample_input = [
        ["how", "much", "is", "pish", "tegj", "glob", "glob", "?"],
        ["how", "many", "credits", "is", "glob", "prok", "silver", "?"],
        ["how", "many", "credits", "is", "glob", "prok", "gold", "?"],
        ["how", "many", "credits", "is", "glob", "prok", "iron", "?"],
        ["how", "much", "wood", "could", "a", "woodchuck", "chuck", "if",
         "a", "woodchuck", "could", "chuck", "wood", "?"],
        ["how", "much", "is", "the", "fish", "?"],
        ["how", "many", "credits", "is", "pish", "prok", "qwerty", "?"]]

    desired_result = [
         "pish tegj glob glob is 42",
         "glob prok Silver is 68 Credits",
         "glob prok Gold is 57800 Credits",
         "glob prok Iron is 782 Credits",
         "I have no idea what you are talking about",
         "Invalid Intergalactic number 'the fish' found in the query",
         "No correct price found in input for good 'Qwerty'"]

    result = run_queries(sample_input, sample_dict, sample_prices)
    assert result == desired_result 


def test_calculate_goods_prices():
    sample_dict = {"glob": "i", "prok": "v",  "pish": "x", "tegj": "l",
                   "fish": "x", "gaa": "m", "c": "c"}

    sample_input_list = []
    # price=34/ii=17:
    sample_input_list.append(["glob", "glob", "silver", "is", "34", "credits"])
    # price=57800/iv=14450:
    sample_input_list.append(["glob", "prok", "gold", "is", "57800",
                              "credits"])
    # price=57800/iv=14450:
    sample_input_list.append(["pish", "pish", "iron", "is", "3910", "credits"])

    desired_result = {"silver": 17.0, "gold": 14450.0, "iron": 195.5}

    result = calculate_goods_prices(sample_input_list, sample_dict)
    assert result == desired_result 


def test_int_to_roman():
    sample_input_list = [34, 994, 1999, 2014]
    desired_result = ["xxxiv", "cmxciv", "mcmxcix", "mmxiv"]

    result = [int_to_roman(x) for x in sample_input_list]
    assert result == desired_result


def test_intergalactic_to_int():
    sample_dict = {"glob": "i", "prok": "v",  "pish": "x", "tegj": "l",
                   "fish": "x", "gaa": "m", "c": "c"}

    sample_input_list = []
    sample_input_list.append(["glob", "prok"])  # IV
    sample_input_list.append(["pish", "fish"])  # XX
    sample_input_list.append(["gaa", "c"])      # MC
    sample_input_list.append(["tegj", "glob"])  # LI
    sample_input_list.append(["gaa", "c", "gaa", "glob",
                              "glob", "glob"])  # MCMIII
    sample_input_list.append(["gaa", "tegj"])   # ML

    desired_result = [4, 20, 1100, 51, 1903, 1050]

    result = [intergalactic_to_int(x, sample_dict) for x in sample_input_list]
    assert result == desired_result


def test_create_intergal_roman_dict():
    sample_input = [["glob", "is", "i"], ["prok", "is", "v"],
                    ["pish", "is", "x"], ["tegj", "is", "l"],
                    ["fish", "is", "x"], ["gaa", "is", "m"],
                    ["c", "is", "c"]]

    desired_result = {"glob": "i", "prok": "v",  "pish": "x", "tegj": "l",
                      "fish": "x", "gaa": "m", "c": "c"}

    result = create_intergal_roman_dict(sample_input)
    assert result == desired_result


def test_validate_dict():
    sample_input = ([["glob", "is", "i"], ["prok", "is", "v"],
                     ["pish", "is", "x"], ["tegj", "is", "l"],
                     ["fish", "is", "z"], ["gold", "is", "0"]],
                    [["how", "how", "credits", "glob", "glob"]])

    desired_result = ([["glob", "is", "i"], ["prok", "is", "v"],
                       ["pish", "is", "x"], ["tegj", "is", "l"]],
                      [["how", "how", "credits", "glob", "glob"],
                       ["fish", "is", "z", "REJECTED by validate_dict"], 
                       ["gold", "is", "0", "REJECTED by validate_dict"]])
    result = validate_dict(*sample_input)
    assert result == desired_result


def test_validate_price():
    sample_dict = {"glob": "i", "prok": "v",  "pish": "x", "tegj": "l",
                   "fish": "x", "gaa": "m", "c": "c"}

    sample_input = ([["glob", "glob", "silver", "is", "34", "credits"],
                     ["glob", "prok", "gold", "is", "578XX", "credits"],
                     ["pish", "pish", "iron", "is", "-0", "credits"],
                     ["mish", "yish", "wood", "is", "10", "credits"],
                     ["mish", "wood", "is", "10", "credits"],
                     ["fish", "fish", "wood", "is", "39,10", "credits"],
                     ["tegj", "glob", "mud", "is", "39.104", "credits"]],
                    [["how", "how", "credits", "glob", "glob"]])

    desired_result = ([["glob", "glob", "silver", "is", "34", "credits"],
                       ["pish", "pish", "iron", "is", "-0", "credits"],
                       ["fish", "fish", "wood", "is", "39,10", "credits"],
                       ["tegj", "glob", "mud", "is", "39.104", "credits"]],
                      [["how", "how", "credits", "glob", "glob"],
                       ["glob", "prok", "gold", "is", "578XX", "credits",
                        "REJECTED by validate_price: "
                        "cannot convert price to float"],
                       ["mish", "yish", "wood", "is", "10", "credits",
                        "REJECTED by validate_price: incorrect Intergalactic "
                        "quantity 'mish, yish' in validate_price"],
                       ["mish", "wood", "is", "10", "credits",
                        "REJECTED by validate_price: incorrect Intergalactic "
                        "quantity 'mish' in validate_price"]])
 
    result = validate_price(*sample_input, sample_dict)
    assert result == desired_result


def test_sort_lines():
    sample_input = ("glob is I\n"
                    "prok is V\n"
                    "pish is X\n"
                    "tegj is L\n"
                    "glob glob Silver is 34 Credits\n"
                    "glob prok Gold is 57800 Credits\n"
                    "pish pish Iron is 3910 Credits\n"
                    "how much is pish tegj glob glob ?\n"
                    "how many Credits is glob prok Silver ?\n"
                    "how many Credits is glob prok Gold ?\n"
                    "how many Credits is glob prok Iron ?\n"
                    "how much wood could a woodchuck chuck if a woodchuck "
                    "could chuck wood ?\n"
                    "how many Credits is glob prok Cadmium !!!\n")

    desired_result = ([
        ["glob", "is", "i"], ["prok", "is", "v"],
        ["pish", "is", "x"], ["tegj", "is", "l"]], [
        ["glob", "glob", "silver", "is", "34", "credits"],
        ["glob", "prok", "gold", "is", "57800", "credits"],
        ["pish", "pish", "iron", "is", "3910", "credits"]], [
        ["how", "much", "is", "pish", "tegj", "glob", "glob", "?"],
        ["how", "many", "credits", "is", "glob", "prok", "silver", "?"],
        ["how", "many", "credits", "is", "glob", "prok", "gold", "?"],
        ["how", "many", "credits", "is", "glob", "prok", "iron", "?"],
        ["how", "much", "wood", "could", "a", "woodchuck", "chuck", "if",
         "a", "woodchuck", "could", "chuck", "wood", "?"]], [
        ["how", "many", "credits", "is", "glob", "prok", "cadmium", "!!!",
         "REJECTED by sort_lines"]])

    result = sort_lines(sample_input)
    assert result == desired_result


def test_read_input():
    sample_input = ("glob is I\n"
                    "prok is V\n"
                    "pish is X\n"
                    "tegj is L\n"
                    "glob glob Silver is 34 Credits\n"
                    "glob prok Gold is 57800 Credits\n"
                    "pish pish Iron is 3910 Credits\n"
                    "how much is pish tegj glob glob ?\n"
                    "how many Credits is glob prok Silver ?\n"
                    "how many Credits is glob prok Gold ?\n"
                    "how many Credits is glob prok Iron ?\n"
                    "how much wood could a woodchuck chuck if a "
                    "woodchuck could chuck wood ?\n")

    with TempDirectory() as d:
        d.write("input.txt", sample_input, encoding="utf-8")
        result = read_input(d.path)
        assert result == sample_input


def test_app_minimal():
    sample_input = ("glob is I\n"
                    "prok is V\n"
                    "pish is X\n"
                    "tegj is L\n"
                    "glob glob Silver is 34 Credits\n"
                    "glob prok Gold is 57800 Credits\n"
                    "pish pish Iron is 3910 Credits\n"
                    "how much is pish tegj glob glob ?\n"
                    "how many Credits is glob prok Silver ?\n"
                    "how many Credits is glob prok Gold ?\n"
                    "how many Credits is glob prok Iron ?\n"
                    "how much wood could a woodchuck chuck if a woodchuck "
                    "could chuck wood ?")

    sample_output = (
        "pish tegj glob glob is 42\n"
        "glob prok Silver is 68 Credits\n"
        "glob prok Gold is 57800 Credits\n"
        "glob prok Iron is 782 Credits\n"
        "I have no idea what you are talking about\n")


def test_app_sample():
    sample_input = ("glob is I\n"
                    "prok is V\n"  
                    "pish is X\n"  
                    "tegj is L\n"
                    "MMM  is M\n"
                    "111  is I\n" 
                    "glob glob Silver is 34 Credits\n"
                    "glob prok Gold is 57800 Credits\n"
                    "pish pish Iron is 3910 Credits\n"
                    "pish fish Iron is 3910 Credits\n"
                    "glob prok Ttg is 998 Credits\n"
                    "how much is pish tegj glob glob ?\n"
                    "how many Credits is glob prok Silver ?\n"
                    "how many Credits is glob prok Gold ?\n"
                    "how many Credits is glob prok Iron ?\n"
                    "how much wood could a woodchuck chuck if a woodchuck "
                    "could chuck wood ?\n"
                    "how much is MMM MMM MMM MMM MMM ?\n"
                    "how many credits is glob ffg gold ?\n"
                    "how many credits is tegj MMM Iron ?\n"
                    "how many credits is MMM tegj gold ?\n"
                    "how many credits is tegj glob Ggggg ?\n"
                    "prok mud is 333 Credits\n"
                    "how many Credits is glob glob mud ?")

    sample_output = (
        "pish tegj glob glob is 42\n"
        "glob prok Silver is 68 Credits\n"
        "glob prok Gold is 57800 Credits\n"
        "glob prok Iron is 782 Credits\n"
        "I have no idea what you are talking about\n"
        "Invalid Intergalactic number 'mmm mmm mmm mmm mmm' found "
        "in the query\n"
        "Invalid Intergalactic number 'glob ffg' found in the query\n"
        "Invalid Intergalactic number 'tegj mmm' found in the query\n"
        "mmm tegj Gold is 15172500 Credits\n"
        "No correct price found in input for good 'Ggggg'\n"
        "glob glob Mud is 133.2000 Credits")

    with TempDirectory() as d:
        d.write("input.txt", sample_input, encoding="utf-8")
        main(d.path)
        result = d.read("output.txt", encoding="utf-8")
        assert result == sample_output

