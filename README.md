# CQL Interpreter

This project consists of developing an interpreter for the **CQL (Comma Query Language)**, a query language inspired by SQL designed to operate on CSV files. The interpreter is implemented in Python using the [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/) library.
> **Academic Context**  
> This application was developed as part of the “Language Processing” course in the second year of the degree in Computer Systems Engineering (Licenciatura em Engenharia de Sistemas Informáticos) at Instituto Politécnico do Cávado e do Ave.

## 📚 Description

The main goal is to allow users to perform data query and manipulation operations on CSV files using SQL-like commands. The features include:

- **Table import and export**: `IMPORT TABLE`, `EXPORT TABLE`
- **Queries**: `SELECT` with support for `WHERE` and `LIMIT` clauses
- **Table manipulation**: `CREATE TABLE`, `RENAME TABLE`, `DISCARD TABLE`
- **Procedures**: defining and executing procedures with `PROCEDURE` and `CALL`

## 🛠️ Technologies Used

- [Python](https://www.python.org/)
- [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)

## 🚀 How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/David123car7/cql-interpreter.git
   ```
   
2. **Install dependencies::**

   ```bash
   pip install ply
   ```
   
3. **Run the interpreter in Interactive Mode:**
   
    ```bash
   python cql_interpreter.py
    ```

4. **Run the interpreter in File Mode:**
   
      ```bash
   python cql_interpreter.py files/entrada.fca
      ```

## 💻 How to Run Tests
   
- **Test the Interpreter**
   ```bash
   python test/test_interpreter.py
   ```
   
- **Test the Lexer**
   ```bash
   python test/test_lexer.py
   ```
- **Test the Parser**
   ```bash
   python test/test_parser.py
   ```

## 💻 Language Syntax

### Table Commands

- Import a table from a CSV file:
  ```
  IMPORT TABLE tablename FROM "filename.csv"
  ```

- Export a table to a CSV file:
  ```
  EXPORT TABLE tablename AS "filename.csv"
  ```

- Remove a table from memory:
  ```
  DISCARD TABLE tablename
  ```

- Rename a table:
  ```
  RENAME TABLE oldname newname
  ```

- Display a table:
  ```
  PRINT TABLE tablename
  ```

### Query Commands

- Select all columns from a table:
  ```
  SELECT * FROM tablename
  ```

- Select specific columns:
  ```
  SELECT column1, column2 FROM tablename
  ```

- Filter with conditions:
  ```
  SELECT * FROM tablename WHERE column = value
  ```

- Limit the number of results:
  ```
  SELECT * FROM tablename LIMIT 10
  ```

- Combine conditions:
  ```
  SELECT * FROM tablename WHERE column1 = value1 AND column2 > value2
  ```

### Table Creation Commands

- Create a new table from a query:
  ```
  CREATE TABLE newtable SELECT * FROM tablename WHERE condition
  ```

- Join two tables:
  ```
  CREATE TABLE newtable FROM table1 JOIN table2 USING columnname
  ```

### Procedures

- Define a procedure:
  ```
  PROCEDURE name DO
    command1
    command2
    ...
  END
  ```

- Call a procedure:
  ```
  CALL name
  ```


