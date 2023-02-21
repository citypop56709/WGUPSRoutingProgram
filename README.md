# WGUPSRoutingProgram
Data Structures and Algorithms II -C950 Project.

Author: Ayun Daywhea

Contact Information

Email: adaywhe@my.wgu.edu


Introduction
“The Programmers' Credo: we do these things not because they are easy, but because we thought they were going to be easy.” – Pinboard
Scenario: The Western Governors University Parcel Service (WGUPS) needs to determine an efficient route and delivery distribution for their Daily Local Deliveries (DLD) because packages are not currently being consistently delivered by their promised deadline. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day. Each package has specific criteria and delivery requirements.
This program accomplishes the goal of delivering packages in an area with each package being delivered on time, and with the total mileage of all the trucks capping out at 140 miles for the day. For me, this program was the greatest example of how something can appear easy until you have to implement it. I have real-life experience with delivery systems in that I used to work as a package handler for FedEx part-time, and I severely discounted the heft of the calculations that we performed without a thought.  People are well-equipped to quickly make decisions. When it comes to sorting packages, deciding locations, placing packages that have to be delivered together, and organizing trucks according to deadlines, humans do all these things intuitively. Computers do nothing intuitively; so, the great challenge of this program is converting human logic to computer logic with Python as the medium.

A. Algorithm Identification

We have a delivery driver named Steve. Steve’s truck is limited in size and has a limited speed. Due to these limitations, Steve has to make choices on what package to deliver and when. Our driver does this based on one rule: What’s the best choice I could make right now?
This is known as a heuristic which is a method of solving a problem quickly when classical methods are too slow. The problem of where to optimally deliver each package is also known as the Travelling Salesman Problem; a problem with time complexity of O(N!), or exponential time (Daniells, 2020). O(N!) is not an ideal time complexity. For the 16 packages that our driver, Steve could carry he would have to do 16! operations using a classical algorithm. This is where our algorithm based on Steve’s rule comes in.
WGUPS uses a self-adjusting greedy, nearest neighbor algorithm to decide what the best choice to make at any given moment is for package delivery. This algorithm is based on what drivers do in real life: They deliver to the closest address and then deliver the closest next package. 
The driver has a starting position, if the driver is starting it will be the hub, if not it will be the ID of the address of the last package delivered. (Logically this makes sense, our driver has just made a delivery and is still there). Packages on the truck are sorted by distance. The closest package is now the current package, and it is delivered causing it to be removed from the packages that are on the truck. The selection of which package will be the current package based on distance is the greedy choice that is being made each time. That package's address becomes the new starting location.
The actual program has to account for a few more things for each package. For example, packages with a deadline have to be delivered so they aren't late, while packages that are specifically meant to be delivered together cannot be delivered apart. The decision-making is still done by checking each package, sorting the packages, and then selecting the package closest while being conscious of unique conditions. All the decision-making is done within the algorithm. None of the package selections are hard-coded.
The main portion of the delivery algorithm is dedicated to finding the next package and returning its distance from the starting position. (All other methods are helper methods to do actions after this is decided.) This method is the self-adjusting heuristic portion of the program.

Breakdown of how it works:

   1. The truck has a starting location at the address of the previously delivered package. If no packages have been delivered, then it will start at the hub.
   2. The truck sorts the packages that are in three separate categories:
       A. Packages with a deadline get sorted by their deadline.
       B. Packages that are co-packages and have to be delivered together are sorted by their distance from the current location if they do not.
       C. Packages without special conditions are in a list called options and are sorted by distance from the current location.
   3. If they are co-packages in the co-package list then they will be selected first to be delivered. This is because all co-packages have to be delivered together.
   4. Otherwise, if they are no co-packages if the options list, the list of packages that could be delivered without any special conditions, is empty then there is no candidate. Otherwise, the first package from the options list is the candidate to be delivered. (It's the package that the driver thinks is the closest).
   5. If they are packages that have a deadline, and that package is not the same as the candidate that was just selected, then that package with a deadline is the new package that the truck will deliver. Logically, this makes sense. Packages that have a deadline must be delivered before those without.
   6. The current package is set to the results of the previous conditional statements, and the time for delivery is calculated based on how long it will take for the driver to get the package's address from the current position.
   7. The algorithm returns that distance.

B1. Logic Comments

Class Truck:
Class Attributes:
package current = current package
list<package> currentPackages = list of all the packages currently on the truck
list<package> deadlinePackageList = list of all the packages that have a deadline
list<package> coPackages = list of all the packages that must be delivered together
list<package> options = list of possible options for delivery. These are packages with no special conditions.
time currentTime = current time before the driver begins driving with the selected package.
list<float, time> totalMiles = total miles the truck has driven that day.

Class Methods:
void deliverPackages()
void processPackages()
void returnToHub()
float getNextPackage()
boolean checkLeftoverPackages()

Implementation:
#Function is called while packages in currentPackages
float getNextPackage():
    start = 0 if current else current.address.id
    if deadlinePackages:
        sort(deadLinePackages)
    if coPackages:
        sort(coPackages)
    if options:
        sort(options)
    candidate = Null
    candidateDistance = Null
    if coPackages:
        candidate = coPackages[0]
        candidateDistance = candidate.address.distanceList[start]
    else:
        candidate = options.isEmpty() ? options[0]: Null
        candidateDistance = candidate == Null: candidate.address.distanceList[start]: Null
        if deadlinePackages:
            deadlinePackage = deadlinePackages[0]
            if deadLinePackage != candidate:
                candidate = deadLinePackage
                candidateDistance = candidate.address.distanceList[start]
        current = candidate
        current.enRouteTime = currentTime
        current.deliveryTime = getTime(currentTime, candidateDistance)
        return candidateDistance

B2. Development Environment
The program was written using PyCharm 2022.3.1 as the main IDE, and GitHub for version control. I used Visual Studios Code 1.75.0 to help with prototyping ideas. For hardware, I used my M1 MacBook Air with 8GB RAM, 256 GB storage, and Mac OS Ventura 13.1 as my operating system.

B3. Space-Time and Big-O
The algorithm does the following things:
	Perform the getNextPackage() function while they are packaged in the current packages list.
	Sorted lists are used to see what packages are on the truck and for packages with special conditions.
	Finds the distance for the package’s address from the start location.
	Performs the algorithm on each package to deliver everything that needs to be delivered.
	Removes the package from any associated list.

The overall time complexity for the nearest neighbor algorithm is O(n2) because the truck has to perform the getNextPackage() function for each package in the current packages list.
The operation with the highest time complexity in the getNextPackage() function itself is the algorithm sorting each list. The Python sort algorithm, TimSort, has a time complexity of O(n log n) (Auger et al., 2018). This is the slowest part of the algorithm by far.
Each package has an address object as a class attribute, and the address object has a distance list that contains values for the distance to each possible address. Looking up a value for an index in a list has an O(1) time complexity.
Looking up the distance for each package in the list is an O(n) because the Truck has to iterate through each package using a while loop.
Removing the package from the list has a time complexity of O(n) in the worst case because the other item list must be shifted to the left if an item is removed from the front of the list. (Python Wiki).
The overall space complexity is O(n) the reason why is that even if it takes O(n2) operations to find the nearest neighbor; the neighbors are still stored linearly.

B4. Scalability and Adaptability

A hash table is a data structure that stores information in key-value pairs. This enables the value to be retrieved by inputting a key. The hash table in this program is used for two things: To store a street address as keys and the address object as values and to store package IDs as keys with the associated package object as a value.
The hash table in the program is implemented as a chaining hash table that creates an array of buckets. The key is hashed with the hashed value reduced to the hashed value modulo the number of array buckets in the hash table. If a key that is hashed when reduced has the same value as another key, then its value can be appended to the end of the same array as the other key. This is known as chaining. The hash table then uses linear probing to return the appropriate value for the given key.
This particular implementation of the chaining hash table has a few features that differentiate it from a standard one. First, keys and values are stored together in the array buckets. The reason for this is to enable the hash table to retrieve a value based on any given key. It checks each key-value tuple in the array bucket and only retrieves the key that matches what was passed in.
The chaining hash table is scalable because the number of arrays to serve as buckets can be passed into whatever is needed. This reduces the number of probes the algorithm has to perform when linear probing.

B5. Software Efficiency and Maintainability

The WGUPS program is efficient because it delivers all the given packages on time, and with a mileage of under 140 for the entire day.
The program does not need to be maintained because it does not use any external libraries that would require occasional work to ensure that the libraries are still being maintained. Technically, the program could have been designed with all the classes and logic built into one main.py file. The program's modules are separated into packages to make it easier to make modifications as needed. The python packages are organized so that each class has its python package when it makes sense.

B6. Self-Adjusting Data Structures

Unlike arrays that have a fixed size with each value in the error occupying a consecutive block in memory, the chaining hash table is self-adjusting; you can add or remove values from it, and it can adjust its size accordingly. The main strength of self-adjusting structures in general is that they can accept values dynamically. This makes it easy to use without having to worry about running into an Index Error from trying to access an index that's out of bounds. Another advantage is that you can store keys and values together while with an array or list, you have to access values using only indexes. This is incredibly useful for just about anything. In this program one way I used it was to store addresses and tie them with an address object to make associating packages with the correct address object possible
 The main negative is that hash tables take up a substantial amount more memory than an array. The hash table has to include memory for each array bucket, and the value for each key-value pair stored in the array buckets.
The other negative is that hash tables are much slower than arrays because worst case the key-value pair is stored at the end of an array bucket, and each value in the bucket has to be searched giving a time complexity of O(n) compared to the array's time complexity of O(1).

C. Original Code

The program runs on a standard installation of Python 3 and requires no external libraries. The interface runs through the console, but no additional arguments need to be passed in to get it working.

C1. Identification Information

The main.py file includes first name, last name, and student ID in the initial comments.

C2. Process and Flow Comments

The program includes comments in the code explaining the process and flows for each major block of code.

D. Data Structure	

The program includes a Hash Table data structure that can store and retrieve package information. It is self-adjusting dynamically according to input. It includes a function put() that inserts packages into the hash table, and includes a function, put() that stores package data in the Hash Table, and a function called status_lookup() that retrieves the most up-to-date status information based on the package ID passed in.

D1. Explanation of Data Structure

A hash table is a data structure that stores information in key-value pairs. This particular implantation is a chaining hash table that creates an array of buckets using Python’s list data structure. Each bucket is a list as well. 
The hash table stores keys and values as tuples. The reason for this is that in a chaining hash table, the key is hashed and then reduced using the length of the array buckets in the table, then is appended to the end of the list whose index corresponds to the key’s hashed value. The hash table uses linear probing to search through the array to find the appropriate value for the given key. Keys and values are stored as tuples to make it easy to retrieve a list of all the keys in the hash table and all the values in the hash table. It also makes it simpler to ensure that the correct value for the key is retrieved from the hash table.
Packages are added to the hash table using the put() method to input a key-value pair into the table with the package ID as the key, and the package object as the value. The package information is retrieved from the CSV file using the object class PackageTools which has a class method named update_packages_from_csv. This method parses the CSV data and then uses the put() function in the hash table to insert the package into the data structure.
To retrieve the data we can use the get() function to retrieve the package object using the package id as a key. If we want to retrieve the status of the package instead, the hash table has a lookup function named status_lookup() that gets the package's status information using the package ID as a key. The method gets the data for whatever time the delivery function is in its route so it can get give accurate information so the user can see if the package is at the hub, en route, etc. 

E. Hash Table

The hash table has an insertion function named put that stores a package with an ID as a key and an object named Package that contains all the appropriate package data from the CSV file as a value. The hash table also includes a function named get() that can retrieve the package object given the package ID, and a function named status_lookup() that can retrieve the most up-to-date package status information given a package ID.

F. Look-Up Function

The hash table has a look-up function named status_lookup that retrieves the most up-to-date package status information for the time in the delivery algorithm. It also has a function named get() that retrieves the package data as an object named package.

G. Interface

The interface is implemented using the console. It can check if all packages were delivered on time with a total mileage of under 140 miles using option 1.
 
H. Screenshots of Code Execution

A screenshot of code execution showing the total mileage and the packages being delivered is displayed below.
 
I1. Strengths of Chosen Algorithm

The greedy nearest neighbor algorithm's biggest strength, and the reason why I chose it, is its flexibility in dealing with unexpected outcomes. The algorithm is only focused on finding the shortest distance for the next package, because of this it can work even if the list of packages changes, or package priority needs to change. It runs every time so it can be accurate regardless of what happens to the packages in the truck.

I2. Verification of Algorithm

Verification Notes:
	The program delivers all the packages with a total mileage of 131.4 miles.
	The program delivers all the packages on time.
	Packages can be verified to show that they’re on time because the deadline of each package is displayed with every package status.
	Mileage, package delivery, and package deadlines are verifiable and visible through the user interface.

I3. Other possible Algorithms

The two other algorithms that could have been used to deliver packages are Dijkstra’s Algorithm and the Bellman-Ford Algorithm.

I3A. Algorithm Differences

Unlike our greedy nearest-neighbor algorithm which only finds the node with the shortest path for the current node, Dijkstra’s Algorithm finds the shortest path for every reachable node. (Sryheni, 2022) So, if it was implemented it could run to find all possible shortest paths, and then that set route could have been utilized. A huge strength of Dijkstra's algorithm compared to the greedy nearest neighbor algorithm that I used is that instead of having to run an algorithm for every package, I could run Dijkstra's once.
The reason why I chose not to use it is that the shortest path is only one of the conditions for delivering packages. Because of the special conditions, I had to spend far more time working with deadlines than I did with distance. Also, I had to account for when to return to get packages, and more. Due to the special conditions, it did not seem worth it to spend the effort developing an implementation of Dijkstra's algorithm for the project.
Bellman-Ford algorithm is designed to find the shortest path in a graph where there could be negative weights (Sryheni, 2022). The negative weights could represent anything, for example, the graph nodes can be accounts, and negative weights on edges can represent withdrawals while positive weights can represent deposits. The main advantage of this is that I could create negative weight edges to represent deadlines so the algorithm could ensure that packages were always delivered on time. This would enable the algorithm to be only run once instead of for every package like the algorithm I used.
The reason why I chose to not use the Bellman-Ford algorithm is the extra time it would have taken to consider all the possible edge cases. I would have had to consider a way to calculate negative weight edges for deadlines, and co-packages, and find a way to calculate when the truck should go back to get more packages. If this was a program where the only special condition was deadlines, then it would be worth it.

J. Different Approach

If I could redo the project the one thing that I would do is save time by hard-coding the way the trucks were loaded. I designed a system to load the trucks using a loop and series of if statements which more than do the job, but I could have saved considerable time hard coding.
The other thing that I would have done differently would be to use a different hash table algorithm. If I had the time, I would design one that used open addressing and was more efficient than a chaining hash table.

K1. Verification of Data Structure

All requirements were met for the project, the packages were delivered on time, and the total combined distance was 134.1 miles. There is a lookup function that accurately returns the package ID, delivery address, deadline, city, zip code, weight, and status for a package in the hash table.

K1A. Efficiency

Overall, adding packages does not greatly affect the lookup function. The slowest part of the lookup function is getting the package from the hash table using the ID. If the hash table has an unusually large number of packages as key-value pairs, and the initial capacity was not appropriate for the size; it could slow down the linear probing because it would be probing through incredibly long lists. For the user to notice though it would have to be a very large number of packages.

K1B. Overhead

The goal to improve performance should always be to have the length of the array buckets to be as small as possible.  This can be done by appropriately initializing the number of array buckets when the data structure is initialized. Adding packages affects the data structure's space usage because each package has to be added to an array bucket, so if the intent is to add a large number of packages, then initializing the appropriate capacity is key to reducing overhead.

K1C. Implications

Adding trucks will not affect the look-up function because it's based more on the number of packages in the hash table as far as time complexity. Extra trucks would not affect the time complexity of the delivery algorithm, but it would make delivery easier since it would require fewer trips back to the depot to deliver all the packages.
Extra cities would not affect hash table performance because the hash table’s performance is based on the number of packages. What it would affect is the time of each delivery if the cities were far apart. In my area, there are a lot of cities very close together, so most delivery drivers end up delivering to three or four cities, but they are only a few miles apart.

K2. Other Data Structures

Potential other data structures that could have worked for the program include a hash table that uses double hashing and a hash table that uses quadratic probing.

K2a. Data Structure Differences

A hash table that uses double hashing, is a hash table that stores key-value pairs and resolves collisions using double hashing. Double hashing is a technique where whenever there are collisions where a key hash to an index that points to the same array bucket as an existing value, the key is hashed again and then added to that corresponding array bucket. The point of double hashing is to avoid clustering to have a more uniform distribution of keys to help result in fewer collisions in the first place.
Compared to chaining where it’s more or less, assumed that there will be collisions, double hashing is concerned about preventing collisions in the first place. This could have reduced the time complexity of retrieving values because they could be stored in a single array instead of a 2D array.
A hash table with quadratic probing is a hash table that has an array of buckets that can store values. Unlike the chaining hash table where these buckets are lists, essentially making a chaining hash table a 2D array, the hash table using quadratic probing is a 1D array. Quadratic probing appropriately places values by implementing an open addressing scheme that applies the formula (H+c1*i+c2*i^2), to the key to find a position in the hash table to insert the value without causing collisions (Miller, 2016).
Compared to linear probing, quadratic probing is much faster when it comes to retrieving the information from the hash table because it does not have to search through each value in each array bucket.
The reason why I went with the chaining hash table is to make it easier if more values than the length of array buckets are added. With chaining hash tables if the length of the table is 16 and the program adds 40 items, the extra key-value pairs are chained to the appropriate array bucket. It could have been possible to combine both approaches and have a chaining hash table that also used quadratic probing with linear probing, or a hash table that uses double hashing and linear probing, but the speed increase was not worth it for me.

M. Professional Communication

This document, as well as the major comments in the program, have been checked using Grammarly.com to ensure that the terminology is used correctly and conveys the intended meaning.

L. Sources - Works Cited

Daniells, L. (2020, April 21). The traveling salesman problem – Libby Daniells - Lancaster university. Libby Daniells - Lancaster University. Retrieved February 6, 2023, from https://www.lancaster.ac.uk/stor-i-student-sites/libby-daniells/2020/04/21/the-travelling-salesman-problem/ 
Auger, N., Jugé, V., Nicaud, C., & Pivoteau, C. (2018, August 14). On the worst-case complexity of Timsort. DROPS. Retrieved February 10, 2023, from https://drops.dagstuhl.de/opus/volltexte/2018/9467/ 
TimeComplexity. TimeComplexity - Python Wiki. (n.d.). Retrieved February 10, 2023, from https://wiki.python.org/moin/TimeComplexity 
Sryheni, S. (2022, November 17). Dijkstra's vs Bellman-Ford Algorithm. Retrieved February 12, 2023, from https://www.baeldung.com/cs/dijkstra-vs-bellman-ford
Miller, B, & Lysecky, R. (2016, August). C949: Data Structures and Algorithms I. zyBooks. 
Retrieved Feb 16, 2023, from https://learn.zybooks.com/zybook/WGUC9492018/chapter/13/section/4
