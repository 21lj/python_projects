# BookMySnacks 

## Project Overview
BookMySnacks is a web-based platform designed to streamline the snack ordering process in movie theaters. It enables users to pre-order snacks linked to their theater & showtime, reducing intermission queues and improving the overall cinema experience.

## Core Ideas
- **Pre-Ordering System**: Users can order snacks before or during the movie, minimizing rush and wait times.
- **Snacks Identification**: Based on 4 digit unique id user can take their snacks
- **Real-Time Management**: Shop admins and theater managers can manage orders, inventory, and show schedules in real time.
- **Modular Architecture**: The system is divided into four key modules:
  - **User Module**: Browse menu, place orders, track status, and view history.
  - **Partners Module**: Divided into two parts:
    - **Shop Admin Module**: Manage snack inventory, accept/reject orders, and view revenue.
    - **Theater Module**: Handle showtimes, seat mapping, and shop assignments.
  - **Super Admin Module**: Oversee user verification, system data, and platform integrity.

## Key Features
- Contactless, digital snack ordering
- Real-time order tracking and status updates
- Secure authentication and role-based access
- Theater-specific snack menus
- Centralized dashboard for all stakeholders

## Technology Stack
- **Frontend**: HTML, CSS & JavaScript
- **Backend**: Python (Django framework)
- **Database**: PostgreSQL
- **Platform**: Web-based application
- **Operating System**: Windows 11 (development environment)

## Software Engineering Approach
- **Development Model**: Waterfall Model (sequential phases: requirements, design, implementation, testing, maintenance)
- **Design Methodologies**:
  - Entity-Relationship (ER) Diagrams for database design
  - Data Flow Diagrams (DFD) for system process visualization
  - UML Diagrams including Use Case, Class, Sequence, Activity, and Deployment diagrams
- **Database Design**: Normalized up to Third Normal Form (3NF) to reduce redundancy and ensure data integrity

## Security Measures
- Encrypted database connections (SSL/TLS)
- Hashed passwords using secure algorithms (bcrypt/PBKDF2)
- Protection against SQL injection, CSRF, and XSS attacks
- Role-based access control and session management
- Logging and monitoring of suspicious activities

## Testing Strategy
- **Unit Testing**: Validation of individual components and functions
- **Integration Testing**: Ensuring seamless interaction between modules
- **System Testing**: End-to-end testing of the complete system
- **Test Cases**: Defined for all user roles (User, Shop Admin, Theater, Super Admin)

## Future Enhancements
- Digital queue management with live updates
- Personalized snack recommendations based on user history
- UPI and digital wallet payment integration
- Multilingual interface support
- Analytics dashboard for sales and user behavior insights
- Guest ordering without registration
- Real-time theater announcements and offers

## System Planning & Scheduling
- **Gantt Chart**: For tracking task timelines and progress
- **PERT Chart**: To identify task dependencies and critical path
- Agile-inspired iterative planning with defined milestones
