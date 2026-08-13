# FoxInventory

FoxInventory is a small command-line inventory management application written in Python with SQLite.

I built the project as a learning exercise to develop my Python skills and gain practical experience working with relational databases and separating application logic from database operations.

## Features

- Add, view, update and delete products
- Track product quantities and stock movements
- Prevent stock levels from falling below zero
- Set reorder levels for individual products
- Generate a low-stock report
- Categorise low-stock products by severity
- Persistent storage using SQLite
- Input validation for common invalid inputs

## Low Stock Reporting

FoxInventory includes a stock report that separates products into:

- **Out of stock** — products with a quantity of zero
- **Very low stock** — products below 35% of their reorder level
- **Other low stock** — products at or below their reorder level

## Project Structure

`main.py`  
Contains the command-line interface, user input handling and reporting.

`db.py`  
Handles SQLite database operations including product creation, retrieval, updates, deletion and stock movement.

`models.py`  
Contains the `Product` model used throughout the application.

## Running FoxInventory

FoxInventory requires Python 3.

Clone the repository and run:

```bash
python main.py
