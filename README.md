

# Rule Engine with Abstract Syntax Tree (AST)

## Overview

This project is a 3-tier rule engine application designed to determine user eligibility based on specific attributes like age, department, income, spend, etc. The engine uses Abstract Syntax Tree (AST) for representing conditional rules, allowing dynamic rule creation, combination, and modification. The application includes:
- A backend for managing rule structures and data storage
- An API for rule operations
- A simple UI to interact with the engine

The application accepts JSON data to evaluate user eligibility by combining custom rules using the AST.

## Features
1. **AST Representation**: Uses a tree-like data structure for logical rules.
2. **Dynamic Rule Management**: Rules can be created, combined, and modified.
3. **Data Validation and Error Handling**: Ensures rules and data formats are correct.
4. **Eligibility Evaluation**: Evaluates user eligibility based on the combined rules.
5. **Bonus Features**: Includes catalog validation and support for user-defined functions.

## Requirements
- Python 3.8+
- Django 4.x
- SQLite (or another database of choice for rule storage)

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/rule-engine-ast.git
cd rule-engine-ast
```

### 2. Install Dependencies
Use `pip` to install the necessary libraries.
```bash
pip install -r requirements.txt
```

### 3. Set Up Database
The project uses SQLite by default. To initialize it:
```bash
python manage.py migrate
```

### 4. Run the Application
To start the development server, run:
```bash
python manage.py runserver
```
The application should now be running at `http://127.0.0.1:8000`.

## Project Structure

- **UI Layer**: Simple interface to test rule creation, combination, and evaluation.
- **API Layer**: Exposes endpoints to create, combine, and evaluate rules.
- **Backend**: Manages AST data structures and interactions with the database.

## Data Structure

### Node Structure
The AST is represented by a `Node` data structure with the following fields:
- `type`: Identifies if a node is an "operator" (AND/OR) or an "operand" (conditions).
- `left`: Reference to the left child node.
- `right`: Reference to the right child node.
- `value`: Holds operand values, such as numbers or strings, for comparisons.

## Database Schema
The database stores rules and metadata. A sample schema for storing rules might look like this:

| Column       | Type     | Description                     |
|--------------|----------|---------------------------------|
| id           | Integer  | Primary key                    |
| rule_string  | Text     | Original rule as a string      |
| ast_json     | JSON     | JSON representation of the AST |

## API Endpoints

### 1. Create Rule
- **Endpoint**: `/api/create_rule/`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
  }
  ```
- **Description**: Takes a rule string, parses it into an AST, and stores it as a `Node` object.

### 2. Combine Rules
- **Endpoint**: `/api/combine_rules/`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "rules": [
      "((age > 30 AND department = 'Sales'))",
      "(salary > 20000 OR experience > 5)"
    ]
  }
  ```
- **Description**: Combines multiple rules into a single AST. Returns the root node of the combined AST.

### 3. Evaluate Rule
- **Endpoint**: `/api/evaluate_rule/`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "ast_json": { ... },
    "user_data": {
      "age": 35,
      "department": "Sales",
      "salary": 60000,
      "experience": 3
    }
  }
  ```
- **Description**: Evaluates the combined rule's AST against provided user data and returns `true` or `false`.

Here's a structured representation of rules using a tree diagram format for clarity. This structure uses the `Node` format and displays logical operations (`AND`, `OR`) along with conditions in a hierarchical tree, which mirrors the structure of an AST (Abstract Syntax Tree).

For each rule, the tree begins with a root operator (like `AND` or `OR`) and branches out to represent each condition or sub-condition.

---

### Structural Representation for Sample Rules

1. **Rule 1**: `"((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"`

   ```
                    AND
                 /       \
               OR         OR
            /      \     /       \
         AND       AND  salary > 50000  experience > 5
        /    \     /   \
   age > 30   department = 'Sales'   age < 25   department = 'Marketing'
```
 
 ```
2. **Rule 2**: `"((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"`

   ```
                AND
              /       \
           AND         OR
         /      \      /   \
     age > 30  department = 'Marketing'   salary > 20000   experience > 5
   ```

3. **Combined Rules**: Assuming both rules (Rule 1 and Rule 2) are combined with an `AND` operator.

   ```
                AND
            /          \
          Rule 1      Rule 2
   ```

### Explanation of the Structure
```
- **Root Node**: Each rule structure starts with a root logical operator (`AND` or `OR`).
- **Branching Nodes**: Each logical condition (`AND`, `OR`) leads to branches that represent sub-conditions or other logical operations.
- **Leaf Nodes**: Conditions (like `age > 30` or `department = 'Marketing'`) are leaf nodes, representing the end points for evaluation.
 ```

### Usage
 ```
### 1. Creating a Rule
Use the `create_rule` endpoint with a rule string to generate a rule AST. Sample rule strings:
- `"((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"`
- `"((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"`

### 2. Combining Rules
Use the `combine_rules` endpoint with multiple rule strings to create a single, combined rule AST. This reduces redundancy and optimizes rule checks.

### 3. Evaluating Rules
With `evaluate_rule`, pass the combined rule's AST and user data to verify eligibility.
 ```
## Test Cases

### Sample Test Cases
 ```
#### Test Case 1: Create Rule
 ```
- **Rule**: `"age > 50 AND salary < 30000"`
- **Expected Output**: `{ "AST": { "type": "AND", "left": { "type": "age > 50" }, "right": { "type": "salary < 30000" } } }`

#### Test Case 2: Combine Rules
- **Rules**: `"(age > 30)"` and `"(experience > 10)"`
- **Expected Output**: `{ "AST": { "type": "AND", "left": { "type": "age > 30" }, "right": { "type": "experience > 10" } } }`

#### Test Case 3: Evaluate Rule
- **Rule**: `"salary < 20000 OR experience < 2"`
- **User Data**: `{ "salary": 25000, "experience": 3 }`
- **Expected Output**: `{"eligible": false}`

## Error Handling
The application includes basic error handling for invalid rule strings and data formats. If a rule string is incorrect or data is missing attributes, the API returns an error message.

## Advanced Features (Bonus)
- **Catalog Validation**: Ensures that all attributes used in rules belong to a predefined list.
- **User-Defined Functions**: Support for advanced rule functions.
- **Rule Modification**: Modify existing rules by adjusting operators, values, or adding/removing nodes.

## Contribution
Contributions are welcome! Please create an issue or pull request on GitHub.

## License
This project is licensed under the MIT License.
