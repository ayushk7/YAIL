# emojilang
Programming language where you can code using emojis 😌

#### To install dependencies
```bash
pip install -r requirements.txt
```

### Current Syntax
#### Variable Declaration
````
    decl a
    decl b=5, c, d=6
    decl e=5+c*4
````
#### Assignments
````
    a = 3
    b = (c*4)+5 / d
````
#### Flow Control
````
    while(a <= 5*b){
        #this is how you use comments
        #statements
    }
    while(){
        #infinite looop
    }
    for(decl i=0, j=7, k; i < a*5; i = i+1, b=b*(28 +)){
        #declared i, j, k and assigned values to i and j
        #statements
    }
    for( ; ; ){
        #all three statements can be skipped
    }
    if(a == 5){
        #statements
    }
    elif(a<5){
        #statements
    }
    elif(a>5 || a&b|c){
        #statements
        #it supports 
        #BITWISE OPERATORS
        #bitwise and        :  &
        #bitwise or         :  |
        #bitwise xor        : ^, xor
        #bitwise complement : ~
        
        #LOGICAL OPERATORS
        #logical and : and, &&
        #logical or  : or, ||
        #logical not : not, !
        #logical xor : xor, ^


    }
    else{
        #statements
    }k

````

### Invalid Syntaxes
````
    #INVALID
    if(a==5)
        print(a)
    
    #VALID
    if(a==5){
        print(a)
    }
    

    #similarly for other blocks like for and while
````
