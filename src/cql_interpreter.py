from interpreter import Interpreter
import sys

class Main:
    interpreter = Interpreter()

    with open("Input/procedures.fca", "r") as file:
                    contents = file.read()
                    interpreter.run(contents, False)
    
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as file:
                contents = file.read()
                result = interpreter.run(contents, False)
        except Exception as e:
            print(e)    
    else:
        print("CQL Interpreter (type 'EXIT' to quit)")
        for expr in iter(lambda: input(">> "), ""):
            try:
                if(expr.strip().upper() == "EXIT"):
                    break
                
                result = interpreter.run(expr, False)
            except Exception as e:
                print(e)



