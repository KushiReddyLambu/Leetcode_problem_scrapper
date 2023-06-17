import re  # Required for pattern matching
arr = []  # Array to store the lines of the file
# Open the file
with open("lc_links.txt", "r") as file:
    # Read each line one by one
    for line in file:
        # Process the line
        arr.append(line)  # You can perform any operation on the line here

# function to remove unwanted links which are not problem links
def remove_elements_with_pattern(array, pattern):
    new_array = []
    for element in array:
        # looping over each link in the array
        if pattern not in element:  # checking if it contains the pattern
            # if pattern not present, then we append the link
            new_array.append(element)
        else:
            # else we do not append the link
            print("Removed: " + element)
    return new_array

# removing the links which contain "/solution" in them
arr = remove_elements_with_pattern(arr, "/solution")

# removing any duplicate links
arr = list(set(arr))
print(len(arr))

with open('lc_problem_links.txt', 'a') as f:
    # Iterate over each link in your final list
    for j in arr:
        # Write each link to the file, followed by a newline thus creating a final file of problem links
        f.write(j)
