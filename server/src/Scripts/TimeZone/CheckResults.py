import csv

wrong = 0
right = 0
with open("out.csv") as f:
    reader = csv.reader(f)

    for row in reader:

        if(row[0] != row[1]):
            wrong += 1
        else:
            right += 1
print wrong
print right

