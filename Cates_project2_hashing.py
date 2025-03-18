#Hazelyn Cates
#Started 10/16/22, finished 11/5/22
#EN.605.620.81.FA22
#This program implements various hashing schemes given an input text file and user input

import re
import array as arr
import time

#start recording execution time of entire program
start_time = time.perf_counter()

#Division hashing scheme
def division_hashing(number, m): #takes data from file and modulo value as arguments
    return number % m

#My hashing scheme, multiplication:
def multiplication_hashing1(number, c, M): #c is constant value entered by the user, M is the multiplication value
    return int(M * (number * c % 1))


#Insert functions for when bucket size = 1 for both division and multiplication schemes
#-->
#inserting keys into the hash table using linear probing for collision handling
#Linear probing for division scheme:
def division_insert_linear1(hashTable, nums, m, b): #takes hashtable, numbers from input file, modulo value, and buckete size arguments
    hash_value = 0 #initialize hash value to 0
    hash_value = 0 #new hash that would have to be calculated if collisiono occurs

    hash = arr.array('l') #array to keep track of each hash value to check for duplicates & keeps track of how many values get hashed (by its size)

    #Taking the minimum makes the size dynamic, dependent on the number of values being hashed versus the size of the hash table
    size = min(len(hashTable), len(nums))
    #print(size)
    primary_collisions = 0 #variable to keep track of primary collisions
    secondary_collisions = 0 #variable to keep track of secondary collision (i.e. the newly calculated hash value is already occupied)

    for i in range(0, size):
        hash_value = division_hashing(nums[i], m) #calculate hash value via division hash function

        if hash_value in hash: #if the hash value has already been used, call the collision handling functions
            #Need to run the linear_probing function as many times as necessary before an empty slot is found
            #can't assume the next empty slot is going to be found in just one iteration of "linear_probing"
            #especially the further down the nums array you go and the more full the hash table gets
            primary_collisions += 1 #increase primary collision by 1
            for j in range(0, 120): #loop through size of hash table
                hash_value = linear_probing(hash_value, m, 1) #calculate a new hash value via a call to linear probing function

                if hash_value not in hash: #check to see if this slot is already being used
                    hash.append(hash_value)  #append that new hash value to the hash array to keep track that it's been used
                    hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table
                    break #break out of inner for loop

                #if the new value has been used, continue through inner for loop:
                else:
                    secondary_collisions += 1 #increment secondary collisions by 1
                    continue

        else: #if it's the first time the hash value has been calculated, add it to the "hash" array
            hash.append(hash_value)
            hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table

    hash_count = len(hash)
    #print the hash table by calling the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'D', 'l', hash_count)


#Linear probing for multiplication scheme
def multiplication_insert_linear1(hashTable, nums, m, c, b): #takes hashtable, numbers from input file, multiplication value, and bucket size arguments
    hash_value = 0

    #Taking the minimum makes the size dynamic, dependent on the number of values being hashed versus the size of the hash table:
    size = min(len(hashTable), len(nums))

    hash = arr.array('l')  #array to keep track of each hash value to check for duplicates & keeps track of how many values gets hashed (by its size)
    primary_collisions = 0  # variable to keep track of primary collisions
    secondary_collisions = 0  # variable to keep track of secondary collision (i.e. the newly calculated hash value is already occupied)

    for i in range(0, size):
        hash_value = multiplication_hashing1(nums[i], c, m) #calculate hash value using multiplication hash function

        if hash_value in hash: #if hash value is already present in hash array,
            primary_collisions += 1 #increase primary collision by 1
            for j in range(0, 120): #loop through size of hash table
                hash_value = linear_probing(hash_value, m, 1)  # calculate a new hash value

                if hash_value not in hash:  # check to see if this slot is already being used
                    hash.append(hash_value)  # append that new hash value to the hash array to keep track that it's been used
                    hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table
                    break

                #if the new value has been used:
                else:
                    secondary_collisions += 1 #increment secondary collisions by 1
                    continue

        else:  #if it's the first time the hash value has been calculated, add it to the "hash" array
            hash.append(hash_value)
            hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table

    hash_count = len(hash) #tells you how many values were successfully hashed
    #Call the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'M', 'l', hash_count)


#inserting keys into the hash table using quadratic probing for collision handling
#For division scheme:
def division_insert_quadratic1(hashTable, nums, m, b): #takes same arguments as linear functions above
    hash_value = 0
    hash = arr.array('l') #array to keep track of each hash value to check for duplicates & keeps track of how many values get hashed (by its size)

    #Taking the minimum makes the size dynamic, dependent on the number of values being hashed versus the size of the hash table
    size = min(len(hashTable), len(nums))

    primary_collisions = 0
    secondary_collisions = 0

    for i in range(0, size):
        hash_value = division_hashing(nums[i], m) #calculate hash value using division hash function

        if hash_value in hash: #if the slot is already occupied, calculate a new hash value via the quadratic probing function
            primary_collisions += 1 #increment primary collisions by 1
            for j in range(1, 120): #loop through size of hash table
                hash_value = quadratic_probing(hash_value, m, j) #calculate a new hash value

                if hash_value not in hash: #check to see if this slot is already being used
                    hash.append(hash_value) #append that new hash value to the hash array to keep track that it's been used
                    hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table
                    break

                else:
                    secondary_collisions += 1 #increment secondary collisions by 1
                    continue

        else: #if it's the first time the hash value has been calculated, add it to the "hash" array
            hash.append(hash_value)
            hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table

    hash_count = len(hash) #this gives you how many values were successfully hashed
    #Call the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'D', 'q', hash_count)

#For multiplication scheme:
def multiplication_insert_quadratic1(hashTable, nums, m, c, b): #takes same arguments as division quadratic above, expect m = multiplication value, not modulo
    hash_value = 0

    #Taking the minimum makes the size dynamic, dependent on the number of values being hashed versus the size of the hash table
    size = min(len(hashTable), len(nums))

    hash = arr.array('l') #array to keep track of each hash value to check for duplicates & keeps track of how many values get hashed (by its size)
    primary_collisions = 0
    secondary_collisions = 0

    for i in range(0, size):
        hash_value = multiplication_hashing1(nums[i], c, m) #calculate hash value via multiplication hash function

        if hash_value in hash: #if calculated hash value is already present in hash array,
            primary_collisions += 1 #increment primary collisions by 1
            for j in range(1, 120): #loop through size of hash table
                hash_value = quadratic_probing(hash_value, m, j)  #calculate a new hash value by calling quadratic probing function

                if hash_value not in hash: #check to see if this slot is already being used
                    hash.append(hash_value)  #append that new hash value to the hash array to keep track that it's been used
                    hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table
                    break

                #if the new value has been used:
                else:
                    secondary_collisions += 1 #increment secondary collisions by 1
                    continue

        else: #if it's the first time the hash value has been calculated, add it to the "hash" array
            hash.append(hash_value)
            hashTable[hash_value].append(nums[i]) #append number to new hash value in hash table

    hash_count = len(hash) #gives the number of values successfully hashed
    #Call the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'M', 'q', hash_count)


#Inserting keys into the hash table using chaining for collision handling
#For division scheme:
def division_insert_chaining1(hashTable, nums, m, b): #takes hash table, numbers from input file, modulo value and bucket size are arguments
    hash_value = 0

    #Taking the minimum makes the size dynamic, dependent on the number of values being hashed versus the size of the hash table
    size = min(len(hashTable), len(nums))
    count = arr.array('l', [0 for i in range(0, 120)]) #keep track of how many keys hash to the same slot
    primary_collisions = 0
    secondary_collisions = 0

    for i in range(0, size):
        hash_value = division_hashing(nums[i], m) #calculate hash value by calling division hash function

        chaining(hashTable, hash_value, nums[i]) #call the chaining function to add the value to the correct slot in the hash table

        count[hash_value] += 1 #increment the index in the count array by 1 every time a value gets hashed there
        if count[hash_value] > 1:  #if more than 1 value is hashed to that slot, it's a primary collisions
            primary_collisions += 1 #increment primary collisions by 1
        #any time you hash to the same slot, it's a collision
        #Don't get secondary collisions in hashing w/ chinaing b/c you can hash to a slot that alreay has a value

    count_sum = sum(count) #gives you how many values were successfully hashed
    #Call the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'D', 'c', count_sum)

#For multiplication scheme:
def multiplication_insert_chaining1(hashTable, nums, m, c, b): #hashTable1, nums, multiplicaiton values, constant, and bucket size arguments
    hash_value = 0

    #Taking the minimum makes the size dynamic, dependent on the number of values being hashed versus the size of the hash table
    size = min(len(hashTable), len(nums))
    count = arr.array('l', [0 for i in range(0, 120)]) #keep track of how many keys hash to the same slot
    primary_collisions = 0
    secondary_collisions = 0

    for i in range(0, size):
        hash_value = multiplication_hashing1(nums[i], c, m) #calculate hash value by callinng multiplication hash function

        chaining(hashTable, hash_value, nums[i]) #call the chaining function to add the value to the hash table
        count[hash_value] += 1 #increment the index in the count array by 1 every time a value gets hashed there
        if count[hash_value] > 1: #if more than 1 value is hashed to that slot, it's a primary collisions
            primary_collisions += 1 #increment primary collisions by 1
        #any time you hash to the same slot, it's a collision
        #Don't get secondary collisions in hashing b/c there's no limit to how many values you can hash to a single slot in the table

    count_sum = sum(count) #gives you how many values were successfully hashed
    #Call the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'M', 'c', count_sum)


#Functions for when bucket size = 3: have to keep track of how many keys have been hashed to each slot
#-->
#Both functions are for the division scheme only:
#Linear probing:
def division_insert_linear3(hashTable, nums, m, b): #hashTable1, numbers from input file, modulo value, bucket size

    #Taking the minimum makes the size, dependent on the number of values being hashed versus the size of the hash table
    size = min(len(hashTable), len(nums))

    count = arr.array('l', [0 for i in range(0, 40)]) #array to keep track of how many values get hashed to each slot in the hash table
    not_hashed = 0 #keep track how many values couldn't be hashed
    primary_collisions = 0
    secondary_collisions = 0

    for i in range(0, size):
        hash_value = division_hashing(nums[i], m) #calculate the hash value by calling division hash function
        if hash_value > 39: #meaning that the value cannot be hashed b/c its hash value exceeds the size of the hash table
            hash_value = linear_probing(hash_value, m, 1) #would this be a call to linear probing or just division hashing again??
            #b/c a collision didn't occur, the hash value was just over 39

        if count[hash_value] == 3: #meaning that the three buckets at that slot are full...
            primary_collisions += 1 #if slot is full, increment primary collisions by 1
            for j in range(0, 40):
                hash_value = linear_probing(hash_value, m, 1) #...then call the linear probing function to find next available slot
                if hash_value > 39: #check the hash value again
                    continue #continue calculating new hash values

                if count[hash_value] < 3: #if space is still available in that slot, add the key to that slot,
                    chaining(hashTable, hash_value, nums[i]) #add the key to that slot
                    count[hash_value] += 1 #increment count array by 1 at the slot
                    break #break out of inner loop once empty slot is found

                else: #if the newly hashed slot is also full, continue through the inner for loop
                    secondary_collisions += 1 #increment secondary collisions by 1
                    continue

        else: #if there's still an empty bucket in the slot,
            chaining(hashTable, hash_value, nums[i])  #call the chaining function to append the key to the given slot in the hash table
            count[hash_value] += 1  #keep track of how many values have been hashed to the specific slot by using a counter

    count_sum = sum(count) #gives how many values were successfully hashed
    #Call the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'D', 'l', count_sum)

#Quadratic probing:
def division_insert_quadratic3(hashTable, nums, m, b):
    primary_collisions = 0
    secondary_collisions = 0

    #Taking the minimum of the two values makes the size dynamic, dependent on the number of values being hashed versus the size of the hash table
    size = min(len(hashTable), len(nums))
    count = arr.array('l', [0 for i in range(0, 40)]) #array to keep track of how many values get hashed to each slot in the hash table
    not_hashed = 0

    for i in range(0, size):
        hash_value = division_hashing(nums[i], m)  #calculate the hash value via division hash function
        if hash_value > 39:
            hash_value = quadratic_probing(hash_value, m, i) #would this be the probing or just another call to division hashing???
            #Cause a collision didn't occur....

        if count[hash_value] == 3:  #meaning that the three buckets at that slot are full...
            primary_collisions += 1
            for j in range(0, 40):
                hash_value = quadratic_probing(hash_value, m, j)  #then call the quadratic probing function to find next available slot
                if hash_value > 39: #keep calculating hash values
                    continue

                if count[hash_value] < 3: #meaning there's still space left in the slot
                    chaining(hashTable, hash_value, nums[i]) #call the chaining function to add value to that slot
                    count[hash_value] += 1 #increment corresponding index in count array by 1
                    break

                else: #meaning that the slot is full
                    secondary_collisions += 1 #increment secondary collisions by 1
                    continue #and continue calculating a new hash value

        else:  #if there's still an empty bucket in the slot,
            chaining(hashTable, hash_value, nums[i])  #call the chaining function to append the key to the given slot in the hash table
            count[hash_value] += 1  #keep track of how many values have been hashed to the specific slot by using a counter

    count_sum = sum(count) #gives you how many values were successfully hashed
    #Call the print_hashTable function
    print_hashTable(hashTable, nums, b, primary_collisions, secondary_collisions, m, 'D', 'q', count_sum)


#Collision handling functions: linear probing, quadratic probing, and chaining within the table:
def linear_probing(hash_value, m, i): #linear probing, returns a new index value for the hash table
    return (hash_value + i) % m


def quadratic_probing(hash_value, m, i): #quadratic probing, returns a new index value for the hash table
    #Use c1 = c2 = 0.5 values from the homework problem
    return int((hash_value + (0.5*i) + (0.5*(i**2))) % m)


def chaining(hashTable, hash_value, num):
    #the goal with this is to create a linked list for every slot in the table to handle collisions
    #as well as when bucket size = 3 (which are mutually exclusive cases in this project)
    hashTable[hash_value].append(num)


def print_hashTable(hashTable, nums, b, p, s, m, scheme, col, total): #prints the hash table and any numbers unable to be hashed
    results_file = open("output.txt", "a")
    load_factor = float(len(nums) / 120)
    input_size = nums.buffer_info()[1]

    results_file.write("Input size: %d\n" % input_size)

    #For bucket size of 1:
    if b == 1:
        if scheme == 'D':  #using division hash function
            if col == 'l':  #meaning using linear probing
                results_file.write("Bucket size: %d\n" % b)
                results_file.write("Method: %s, mod %d\n" % ("Division", m))
                results_file.write("Collision handling: Linear probing\n")
                results_file.write("Number of primary collisions: % d\n" % p)
                results_file.write("Number of secondary collisions: %d\n" % s)

            elif col == 'q':
                results_file.write("Bucket size: %d\n" % b)
                results_file.write("Method: %s, mod %d\n" % ("Division", m))
                results_file.write("Collision handling: Quadratic probing\n")
                results_file.write("Number of primary collisions: % d\n" % p)
                results_file.write("Number of secondary collisions: %d\n" % s)

            else:  #last one is chaining
                results_file.write("Bucket size: %d\n" % b)
                results_file.write("Method: %s, mod %d\n" % ("Division", m))
                results_file.write("Collision handling: Chaining\n")
                results_file.write("Number of primary collisions: % d\n" % p)
                results_file.write("Number of secondary collisions: %d\n" % s)


        elif scheme == 'M':  #using multiplication hash function
            if col == 'l':
                results_file.write("Bucket size: %d\n" % b)
                results_file.write("Method: %s, multiplication value %d\n" % ("Multiplication", m))
                results_file.write("Collision handling: Linear probing\n")
                results_file.write("Number of primary collisions: % d\n" % p)
                results_file.write("Number of secondary collisions: %d\n" % s)

            elif col == 'q':
                results_file.write("Bucket size: %d\n" % b)
                results_file.write("Method: %s, multiplication value %d\n" % ("Multiplication", m))
                results_file.write("Collision handling: Quadratic probing\n")
                results_file.write("Number of primary collisions: % d\n" % p)
                results_file.write("Number of secondary collisions: %d\n" % s)

            else:  # chaining collision handling
                results_file.write("Bucket size: %d\n" % b)
                results_file.write("Method: %s, multiplication value %d\n" % ("Multiplication", m))
                results_file.write("Collision handling: Chaining\n")
                results_file.write("Number of primary collisions: % d\n" % p)
                results_file.write("Number of secondary collisions: %d\n" % s)

        results_file.write("\n")

        for i in range(0, len(hashTable), 5): #range of 0 to size of hash table, increments by 5 in each step
            values = hashTable[i:i+5] #values is a list containing 5 elements from the hash table
            results_file.write("Bucket %d - %d:  " % (i, i+5))

            for j in range(0, 5):
                if len(values[j]) == 0:  #meaning the slot in the hash table is empty
                    results_file.write("  XXXXXX  ")
                else:
                    for v in values[j]:
                        results_file.write("[%d]" % v)
                    results_file.write("  ")
            results_file.write("\n")

    #For bucket size of 3:
    if b == 3:
        if col == 'l':
            results_file.write("Bucket size: %d\n" % b)
            results_file.write("Method: %s, mod %d\n" % ("Division", m))
            results_file.write("Collision handling: Linear probing\n")
            results_file.write("Number of primary collisions: % d\n" % p)
            results_file.write("Number of secondary collisions: %d\n" % s)

        elif col == 'q':
            results_file.write("Bucket size: %d\n" % b)
            results_file.write("Method: %s, mod %d\n" % ("Division", m))
            results_file.write("Collision handling: Quadratic probing\n")
            results_file.write("Number of primary collisions: % d\n" % p)
            results_file.write("Number of secondary collisions: %d\n" % s)

        results_file.write("\n")

        for i in range(0, 40):  #range of 0 to size of hash table
            values = hashTable[i]  #values is a list containing 3 elements from the hash table at index i
            #print(len(values))
            j = i * 3 + 1
            results_file.write("Bucket %d - %d:  " % (j, j+2))

            if len(values) == 0: #meaning the slot is completely empty
                results_file.write("XXXXXX  XXXXXX  XXXXXX")

            elif len(values) == 1: #only a value in the first slot in the bucket
                results_file.write("%d  " % values[0])
                results_file.write("XXXXXX  XXXXXX")

            elif len(values) == 2: #there are 2 values in the bucket
                results_file.write("%d  " % values[0])
                results_file.write("%d  " % values[1])
                results_file.write("XXXXXX")

            else: #all 3 slot in the bucket are filled
                results_file.write("%d  " % values[0])
                results_file.write("%d  " % values[1])
                results_file.write("%d  " % values[2])

            results_file.write("\n")

    #output the load factor
    results_file.write("\nLoad factor: %.2f" % load_factor)
    results_file.write("\n")

    results_file.write("\n---------------------------------------\n")

    #For bucket sizes 1 and 3:
    if len(nums) >= len(hashTable): #if the size of the input is greater than or equal to the size of the hash table
        not_hashed = (len(hashTable) - total) #where total is the total number of values hashed in each scheme

    elif len(nums) < len(hashTable): #for all inputs size less than 120
        not_hashed = len(nums) - total

    results_file.write("%d values unable to be hashed\n\n" % not_hashed)

    results_file.write("\n")
    print("\n")
    results_file.close()


#Main:
#File input
print("Enter full name of text file:")
file_name = input()
open_file = open(file_name, "r")

#file to write results to, open in append mode
results_file = open("output.txt", "a")
#have to clear it whenever a new function gets called b/c it will just keep adding to the end

print("Insert bucket size: 1 or 3")
bucket = int(input())
while bucket != 3 and bucket != 1:
    print("Insert bucket size:")
    bucket = int(input())

#initialize empty array to store numbers in file that need to be hashed
nums = arr.array('l')

#Create hash tables with with 120 addressable slots:
hashTable1 = [[] for i in range(0, 120)] #for bucket size = 1
hashTable2 = [[] for i in range(0, 120)] #for bucket size = 3, creates hash table with a length of 40 with 3 addressable slots per index

for line in open_file:
    #print(line.strip())
    #if the numbers have a newline above them
    if (re.findall("^[0-9]+$", line)): #only access numbers from file input
        nums.append(int(line.strip()))

    else:
        continue

#Calling the functions:
if bucket == 1:
    print("Division or multiplication scheme? Enter D or M:")
    scheme = str(input())
    if scheme != 'D' and scheme != 'M':
        print("Division or multiplication scheme? Enter D or M:")
        scheme = str(input())
    if scheme == 'D':
        print("Choose modulo value: 120, 113:")
        modulo = int(input())
        if modulo != 120 and modulo != 113:
            print("Please choose modulo value: 120, 113:")
            modulo = int(input())

        #record execution time of division scheme
        start_division = time.perf_counter()

        #for a bucket size of 1 and a chosen modulo value, perform all three collision handling techniques:
        #record execution time of linear probing for division hashing scheme
        start_time_division_l = time.perf_counter()
        #call insert functions for division scheme and record the execution times for each collision handling method
        division_insert_linear1(hashTable1, nums, modulo, bucket)
        end_time_division_l = time.perf_counter()
        time_division_l = end_time_division_l - start_time_division_l
        #have to reset the hashtable after every calls
        for i in range(0, 120):
            hashTable1[i].clear()

        #recrod execution time of quadratic probing for division hashing scheme
        start_time_division_q = time.perf_counter()
        division_insert_quadratic1(hashTable1, nums, modulo, bucket)
        end_time_division_q = time.perf_counter()
        time_division_q = end_time_division_q - start_time_division_q

        for i in range(0, 120):
            hashTable1[i].clear()

        #record execution time of chaining for division hashing scheme
        start_time_division_c = time.perf_counter()
        division_insert_chaining1(hashTable1, nums, modulo, bucket)
        end_time_division_c = time.perf_counter()
        time_division_c = end_time_division_c - start_time_division_c

        for i in range(0, 120):
            hashTable1[i].clear()
        end_division = time.perf_counter()
        total_division = end_division - start_division
        results_file.write("\nExecution time for linear probing via division scheme mod %d: %.2e seconds\n" % (modulo, time_division_l))
        results_file.write("\nExecution time for quadratic probing via division scheme mod %d: %.2e seconds\n" % (modulo,time_division_q))
        results_file.write("\nExecution time for chaining via division scheme mod %d: %.2e seconds\n" % (modulo, time_division_c))
        results_file.write("\nExecution time for entire division scheme mod %d: %.2e seconds\n" % (modulo, total_division))

    #this will be for the hashing schemes I write, which will be multiplication:
    if scheme == 'M':
        print("Enter value greater than 0 and less than 1:")
        constant = float(input())
        if constant < 0 and constant > 1:
            print("Enter value greater than 0 and less than 1:")
            constant = float(input())
        m = 120
        #record execution time of multiplication scheme
        start_multiplication = time.perf_counter()

        #record execution time for each collision handling method in multiplication scheme
        start_time_mul_l = time.perf_counter()
        multiplication_insert_linear1(hashTable1, nums, m, constant, bucket)
        end_time_mul_l = time.perf_counter()
        time_mul_l = end_time_mul_l - start_time_mul_l

        for i in range(0, 120):
            hashTable1[i].clear()

        start_time_mul_q = time.perf_counter()
        multiplication_insert_quadratic1(hashTable1, nums, m, constant, bucket)
        end_time_mul_q = time.perf_counter()
        time_mul_q = end_time_mul_q - start_time_mul_q

        for i in range(0, 120):
            hashTable1[i].clear()

        start_time_mul_c = time.perf_counter()
        multiplication_insert_chaining1(hashTable1, nums, m, constant, bucket)
        end_time_mul_c = time.perf_counter()
        time_mul_c = end_time_mul_c - start_time_mul_c

        end_multiplication = time.perf_counter()
        total_multiplication = end_multiplication - start_multiplication
        results_file.write("\nExecution time for linear probing via multiplication scheme value %d: %.2e seconds\n" % (m, time_mul_l))
        results_file.write("\nExecution time for quadratic probing via multiplication scheme value %d: %.2e seconds\n" % (m, time_mul_q))
        results_file.write("\nExecution time for chaining via multiplication scheme value %d: %.2e seconds\n" % (m, time_mul_c))
        results_file.write("\nExecution time for entire multiplication scheme value %d: %.2e seconds\n" % (m, total_multiplication))

if bucket == 3: #only executes the division hashing scheme
    modulo = 41
    #record execution time of division scheme
    start_bucket3 = time.perf_counter()

    #record time for each collision handling scheme used when bucket size = 3
    start_time_div3_l = time.perf_counter()
    division_insert_linear3(hashTable2, nums, modulo, bucket)
    end_time_div3_l = time.perf_counter()
    time_div3_l = end_time_div3_l - start_time_div3_l

    #have to reset the hashtable after every calls
    for i in range(0, 41):
        hashTable2[i].clear()

    start_time_div3_q = time.perf_counter()
    division_insert_quadratic3(hashTable2, nums, modulo, bucket)
    end_time_div3_q = time.perf_counter()
    time_div3_q = end_time_div3_q - start_time_div3_q

    for i in range(0, 41):
        hashTable2[i].clear()

    end_bucket3 = time.perf_counter()
    #time of entire scheme
    total_bucket3 = end_bucket3 - start_bucket3
    results_file.write("\nExecution time of linear probing via division scheme mod %d when bucket size = 3: %.2e seconds\n" % (modulo, time_div3_l))
    results_file.write("\nExecution time of quadratic probing via division scheme mod %d when bucket size = 3: %.2e seconds\n" % (modulo, time_div3_q))
    results_file.write("\nExecution time for entire division scheme mod %d when bucket size = 3: %.2e seconds\n" % (modulo, total_bucket3))

end_time = time.perf_counter() #record execution time of entire program
total_time = end_time - start_time

results_file.write("\n.........................................................\n")
results_file.write("\nExecution time of entire program run: %.2e seconds\n" % total_time)
results_file.write("\n************************************Next Run************************************\n")
open_file.close()
results_file.close()
