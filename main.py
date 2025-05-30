# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def hello_world():
    print('hello world!')

# create a recursive function to reverse a string
def reverse_string(s):
    if len(s) == 0:
        return s
    else:
        return reverse_string(s[1:]) + s[0]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('shaurya')
    hello_world()
    print(reverse_string('tacocat1'))


