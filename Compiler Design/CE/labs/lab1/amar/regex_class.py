'''
Program to check if the string is accepted by the regular expression
Name: Amar Kumar Mandal
Group: CE (4th Year/ 1st Sem)
Question number#2
'''


class PatternMatcher:
    def __init__(self, pattern, operations):
        self.pattern = pattern
        self.operations = operations

    def is_valid_string(self, input_string):
        n = len(input_string)
        m = len(self.pattern)

        def dp(i, j):
            # if pattern reaches their end
            if j == m:
                return i == n
            match = i < n and (input_string[i] == self.pattern[j]
                               or self.pattern[j] in self.operations)
            if j + 1 < m and self.pattern[j + 1] in self.operations:
                return dp(i, j + 2) or (match and dp(i + 1, j))
            return match and dp(i + 1, j + 1)

        return dp(0, 0)


print('''
Supported Operations: {*, .}\n
    . (period) which matches any single character\n
    * (asterisk) which matches zero or more of the preceding element.\n
    Instrucion: Write a regular expression combining these operations\n
''')
print("***********Program Starts*******************\n\n")
pattern = input("Enter the required pattern: ")
inp_str = input("Enter required string to validate separated by comma: ")
inp_str = inp_str.split(',')
operations = ["*", "."]
matcher_obj = PatternMatcher(pattern, operations)

for w in inp_str:
    print(matcher_obj.is_valid_string(w.strip()))
