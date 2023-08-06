# microstate 

Simple REST state storage tied to a write key

## Creating a state writer 

    from microstate import MicroStateWriter
    from microprediction import new_key
    write_key = new_key(difficulty=11) # Takes a while! 
    msw = MicroStateWriter(write_key=write_key)

### Usage pattern 1

Assume we have data taking the form of a dictionary

    data = {'age':17,'model':'my model','params':{'mean':17,'std':10}
    
Store data: 

    msw.set(value=data)
    
Retrieve data:

    data = msw.get()     
    
### Usage pattern 2 (using a logical memory location from 0 to 99)

Store data with a location index

    msw.set(value=data, k=34)
    
Retrieve data with a location index

    data = msw.get(k=34) 
    
### Other data types

In addition to dict, or list, data may be str, int or float. 
However it will be stored internally as a binary string. Be aware of this when
retrieving the data. 

### Partial support for tuple

Tuples can be stored but will be converted to list. 
    
### Memory limits 

Assuming a write key of difficulty at least 11:

    location  0      holds    320 kb
    locations 1-319  hold       1 kb each 
    
 