Hey There !!!

This is the simple python package for generating fake id's. You can fetch upto 5 MILLION fake id's. The id generated contains 4 elements 'First Name', 'Last Name', 'Email Id' and 'Mobile Number'. This package provides indian id's.


Input:

n: Number of required fake id's
0 < n < 5000000


Output:

List: List of Json objects which contain the details of the id i.e. first name, last name, email id and mobile number.


Installation:

pip install faker-ids


Code: 

import faker_ids
print(faker_ids.get_ids(n))



