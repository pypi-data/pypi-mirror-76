# microstate 

Simple REST state storage tied to a write key

### You need a key 

    from microstate import MicroStateWriter
    write_key = MicroStateWriter.create_key(difficulty=11) # Takes a while! 
   
to instantiate a writer
    
    writer = MicroStateWriter(write_key=write_key)

### Usage pattern 1

Assume we have data taking the form of a dictionary

    data = {'age':17,'model':'my model','params':{'mean':17,'std':10}
    
Store data: 

    writer.set(value=data)
    
Retrieve data:

    data = writer.get()     
    
### Usage pattern 2 (using a logical memory location from 0 to 99)

Store data with a location index

    writer.set(value=data, k=34)
    
Retrieve data with a location index

    data = writer.get(k=34) 
    
### Other data types (caution!)

- Tuples will be converted to lists
- int, float to string

To preserve types use dict or list 

### Partial support for tuple

Tuples can be stored but will be converted to list. 
    
### Memory limits 

Assuming a write key of difficulty at least 11:

    location  0      holds    320 kb
    locations 1-319  hold       1 kb each 
    
 