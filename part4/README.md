# Holberton BnB - Project

The **Holberton BnB** project is a platform designed to manage bookings. This project focuses on building a scalable, RESTful API using **Flask** and **flask-restx**. It includes functionality for managing users, places, reviews, and amenities.

This README provides an overview of the project, including how to set up and run the application.

## Table of Contents

- [Project Description](#project-description)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Business Logic Layer](#business-logic-layer)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Project Description

The **Holberton BnB** project is a backend API designed to handle user accounts, places (e.g., apartments, hotels), reviews, and amenities (e.g., Wi-Fi, pool). The application is modular, using the **Facade pattern** to separate the logic into layers for better maintainability and scalability.

### Technologies Used:
- **Python** (Flask for web framework)
- **flask-restx** (for building RESTful APIs)
- **In-memory repository** (for data storage, will be replaced with SQLAlchemy in future phases)

### Features:
- Create and manage users
- Create and manage places
- Add reviews and amenities to places
- Get detailed information about users, places, reviews, and amenities

## Setup Instructions

Follow these steps to set up the project locally:

### 1. Clone the repository:
```bash
git clone https://github.com/neonbloo25/holbertonschool-hbnb.git
cd holbertonschool-hbnb
