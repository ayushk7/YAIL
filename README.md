# emojilang
Programming language where you can code using emojis 😌

#### To install dependencies
```bash
pip install -r requirements.txt
```

### Current Syntax

#### Operators
|Operation | Symbol|
|---------|-----|
|unary not|not<br>!|
|unary complement|~|
|bitwise and|        &|
|bitwise or|  \| |
|bitwise xor| ^<br> xor
|bitwise complement | ~
|logical and | and <br> &&
|logical or  | or <br> \|\| |
|logical not | not <br> !
|logical xor | xor <br> ^|

#### Operators Precedence
<mark>Operators With Highest Priority On Top</mark><br>
|Description|Operators|
|----|-----|
|unary oprators|not, !, ~ |
|arithmatic|*, /, %|
|arithmatic|+, -|
|comparison|==, !=, <=, <, >, => <br><mark>*Python's Precedence</mark>|
|bitwise and|&|
|bitwise xor|^, xor|
|bitwise or|\||
|logical and|and, &&|
|logical or|or, \|\||


#### Variable Declaration

````
    decl a
    decl b=5, c, d=6
    decl e=5+c*4
    decl t = true, f
````
#### Assignments
````
    a = 3
    b = (c*4)+5 / d
    f = false
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
````
#### Branching
````
    if(a == 5){
        #statements
    }
    elif(a<5){
        #statements
    }
    elif(a>5 || a&b|c){
        #statements
    }
    else{
        #statements
    }
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
