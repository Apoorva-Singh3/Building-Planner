# Building Planner

## Objective

Design and build a web application that allows users to select, draw, and annotate building plans.

## Description

The Building Planner application provides a drawing area and a toolbar with the following tools:

1. **Draw Tools**: Enables users to create shapes such as lines, rectangles, circles, and other shapes to design their building plans.
2. **Select Tool**: Allows users to move, resize, or delete the created shapes.
3. **View Tool**: Provides the option to show or hide annotations. Annotations include dimensions such as length and breadth that users can add to their drawings.

## Features

- **Drawing Area**: Interactive space for creating and editing building plans.
- **Toolbar**: Contains tabs for Draw Tools, Select Tool, and View Tool.
- **Annotations**: Users can add and manage annotations for dimensions and comments on shapes.

## Store

The application uses a PostgreSQL database to store drawing details. The database schema includes tables for drawing, shapes, and annotations.

## Interface

The frontend of the application is built using Vue.js, providing a simple and minimal interface. It includes the drawing area and toolbar for an intuitive user experience.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Apoorva-Singh3/Building-Planner.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd building-planner
    ```

3. **Install dependencies**:

    For the backend:
    
    ```bash
    pip install -r requirements.txt
    ```

    For the frontend:
    
    ```bash
    cd frontend
    npm install
    ```

4. **Set up the database**:

    Configure your PostgreSQL database and update the database settings in the configuration file.

5. **Run the application**:

    For the backend:
    
    ```bash
    python run.py
    ```

    For the frontend:
    
    ```bash
    npm run serve
    ```

## Usage

1. Open the application in your browser.
2. Use the Draw Tools to create shapes on the drawing area.
3. Use the Select Tool to move, resize, or delete shapes.
4. Use the View Tool to toggle annotations on or off.

## Testing

The test cases for all APIs has been added in `tests/test_api.py` file. You can run the test cases using `pytest` command.

## Technology Used

- Vue.js for the frontend framework
- Flask for the backend framework
- PostgreSQL for the database


