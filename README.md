# MERCHANT'S GUIDE TO THE GALAXY
## Original problem formulation

You decided to give up on earth after the latest financial collapse 
left 99.99% of the earth's population with 0.01% of the wealth. Luckily,
 with the scant sum of money that is left in your account, you are able 
 to afford to rent a spaceship, leave earth, and fly all over the galaxy
  to sell common metals and dirt (which apparently is worth a lot).  
Buying and selling over the galaxy requires you to convert numbers and
 units, and you decided to write a program to help you.  
The numbers used for intergalactic transactions follows similar 
convention to the roman numerals and you have painstakingly collected 
the appropriate translation between them.  

Roman numerals are based on seven symbols:  
Symbol  Value  
I 1  
V 5  
X 10  
L  50  
C 100  
D 500  
M 1,000  

Numbers are formed by combining symbols together and adding the values.  
For example, MMVI is 1000 + 1000 + 5 + 1 = 2006.  

Generally, symbols are placed in order of value, starting with the 
largest values. When smaller values precede larger values, the smaller 
values are subtracted from the larger values, and the result is added to
 the total.  
For example MCMXLIV = 1000 + (1000 - 100) + (50 - 10) + (5 - 1) = 1944.

The symbols "I", "X", "C", and "M" can be repeated three times in 
succession, but no more. (They may appear four times if the third and 
fourth are separated by a smaller value, such as XXXIX.) "D", "L", and 
"V" can never be repeated. "I" can be subtracted from "V" and "X" only.
 "X" can be subtracted from "L" and "C" only. "C" can be subtracted from
  "D" and "M" only. "V", "L", and "D" can never be subtracted. Only one 
  small-value symbol may be subtracted from any large-value symbol. A 
  number written in [16]Arabic numerals can be broken into digits. For 
  example, 1903 is composed of 1, 9, 0, and 3. To write the Roman 
  numeral, each of the non-zero digits should be treated separately. 
  In the above example, 1,000 = M, 900 = CM, and 3 = III. Therefore, 
  1903 = MCMIII.
(Source: [Wikipedia](http://en.wikipedia.org/wiki/Roman_numerals))

Input to your program consists of lines of text detailing your notes on
 the conversion between intergalactic units and roman numerals.  You are
  expected to handle invalid queries appropriately.

### Test input:
> glob is I  
> prok is V  
> pish is X  
> tegj is L  
> glob glob Silver is 34 Credits  
> glob prok Gold is 57800 Credits  
> pish pish Iron is 3910 Credits  
> how much is pish tegj glob glob ?  
> how many Credits is glob prok Silver ?  
> how many Credits is glob prok Gold ?  
> how many Credits is glob prok Iron ?  
> how much wood could a woodchuck chuck if a woodchuck could chuck wood ?


### Test Output:
> pish tegj glob glob is 42  
> glob prok Silver is 68 Credits  
> glob prok Gold is 57800 Credits  
> glob prok Iron is 782 Credits  
> I have no idea what you are talking about 

## Assumptions and solution algorithm
### Assumptions

- the code will be integrated in a higher-level application,
 e.g. scripting engine of the notepad device used for creating 
 the notes

- the target platform will be able to execute Python 3 code

- the notes would be passed to the code as a text file with name "input.txt" in the working directory

- the code output will be stored for the further use by the
target application in the "output.txt" file in the working directory

- the text files encoding is utf-8

- the names of goods consist of a single word (otherwise a word analysis 
for Intergalactic numerals / nouns should be added + validating- 
and all subsequent functions should be modified)

- the names of goods in the output are capitalized

- the prices can be non-negative integer or floating point, 
decimal separator can be either "." or ","

- the price lines do not contain contradictory entries (otherwise execution stops)

- the price in Credits can be rounded to four decimal places

- the query should start from
  - "how many Credits is" (to obtain a price of certain amount of specified good)
  - "how much is" (to convert numbers from Intergalactic to Arabic numerals)
  
- the query should end with space and question mark
   
- the dictionary part of the notes contains only Intergalactic numerals,
corresponding to single Roman symbol (otherwise additional module for
solving a system of linear equations and checking, whether it is solvable,
should be added)

- the dictionary lines do not contain contradictory entries (otherwise execution stops) 

### Solution algorithm

- read input.txt file as set of lines
- parse the lines into
  - dictionary Intergalactic -> Roman numerals
  - prices of goods in Intergalactic units
  - queries
  - unrecognized lines
- produce Intergalactic -> Roman dictionary
- produce price list for goods (with prices of type float)
- execute the queries
  - find out query type (number converter / price query / unknown)
  - parse query and execute it
- write queries results to the "output.txt" file

## Test-driven development

1) Write initial application test, containing sample input and
sample output from the problem formulation
2) Write tests covering the functionality of the function
3) Write function passing the tests
4) Add tests to cover possible problematic cases
5) Modify function to pass the tests
6) Add more application tests covering possible problematic cases
7) Modify the functions/unit tests to handle the problem


## Running environment

- For execution of the program Python >= 3.7 needed (due to guaranteed keeping order of dictionary entries)
- Place *main.py* code file and *input.txt* file with input lines to the working directory
- Execute *python main.py* in the working directory
- Find query results in the *output.txt* file and erroneous input lines with error messages in the *errors.txt* file
- The code is designed to be platform-independent
- For testing install *pytest* and *testfixtures* packages (*pip install pytest testfixtures*)
- Tests can be run locally with *pytest* command from the package directory (it should be in *PYTHONPATH* environment variable)

