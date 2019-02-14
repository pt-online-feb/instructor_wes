# Note from Wes - I'm going to convert this into a better format soon.

# understand the problem
    # look for keywords like "takes", "given", "accepts"
    # get to the core of function structure
    # determine inputs and outputs
    # helpful hint
        # turn the problem into a concrete example
    # consider edge cases and outcomes for multiple cases in general

# break your solution down into discrete steps or subsets of steps
    # good places to look, something that accomplishes one task
    # start writing comments to a 4 year old as high-level chunks so we can break them down into really small steps
    # helpful hint
        # break down your process of doing it as a person on a whiteboard into the smallest possible steps
        # write down each step
    # helpful hint 2
        # write our high-level "medium sized" chunks out in order
        # start writing questions to yourself about how you accomplish small tasks within this chunk?
    
# think about applying abstraction
# def flexible_countdown(high_num, low_num, mult):
#     for i in range(high_num, low_num - 1, -1):
#         if i % mult == 0:
#             print(i)

# flexible_countdown(9, 3, 3)

# writing code
    # initialize variables
    # descriptive variable names
    # comments
    # print statements TEST WHAT WE DO AS WE GO

# testing/debugging
    # know our test inputs and expected outputs
    # run it in a debugger/read the errors
        # look at line numbers and google error message

    # identify where in the code things are going wrong
    # T-DIAGRAMS
    # using what we know should be happening, track the data through the code and find exactly where that data is not what we expect
    # identify possible causes of the unexpected result
        # always have 1 or 2 things in mind that might be causing the problem
    # figure out how we test those assumptions
    # figure out, based on our tests, whether or not our assumption was correct
    # if we're right
        # fix the issue
    # if we're wrong
        # look for new reasons why the problem might be occurring and start over
    # ASK SOMEONE

# asking for help
    # here's what I expect to happen
    # here's what's actually happening
    # here's what I've done so far to solve the problem

# apply what we've learned
    # WHY did the problem occur in the first place?