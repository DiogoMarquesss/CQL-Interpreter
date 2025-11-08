import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from interpreter import Interpreter

interpreter = Interpreter()

commands = [
    'IMPORT TABLE cidades FROM "cidades.csv";',
    'EXPORT TABLE cidades AS "cidades.csv";',
    'RENAME TABLE cidades "kazzio";',
    'PRINT TABLE kazzio;',
    'SELECT * FROM kazzio;',
    'SELECT Freguesias FROM kazzio;',
    'SELECT * FROM kazzio WHERE Pessoas > "10";',
    'CREATE TABLE kazzio2 SELECT * FROM kazzio;',
    'CREATE TABLE kazzio3 SELECT * FROM kazzio WHERE Pessoas > "10";',
    'DISCARD TABLE kazzio;',
    'PROCEDURE procedureTest DO IMPORT TABLE cidades FROM "cidades.csv"; END',
    'CALL procedureTest;'
]

for command in commands:
    print("Input:", command)
    output = interpreter.run(command, True)
    if output:
        print(output)
    print("-------------------------------------")