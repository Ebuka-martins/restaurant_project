# PHANTOM RESTAURANT BOOKING SYSTEM
The Restaurant Booking System is a sophisticated Django-based web application designed to streamline restaurant table reservations and management. This system offers a seamless experience for both customers and restaurant staff, featuring real-time table availability, booking management, and comprehensive analytics.
The platform allows registered users to make restaurant reservations, manage their bookings, and provide feedback about their dining experience. For restaurant staff, it provides powerful tools to track bookings, analyze customer patterns, and monitor revenue metrics through an intuitive dashboard.

 Here is the link to the Restaurant Booking System-heroku where every bookings are being made [link](https://restaurant-project-524b51fc1cda.herokuapp.com/)



  ![Phantom Restaurant Booking System](booking/static/booking/image/front-page.png)

### This is Portfolio Project 4 for Full Stack Developer Diploma taught through Code Institute

# Key Features
- User authentication and personalized booking management
- Real-time table availability checking
- Automated booking confirmation system
- Detailed analytics and revenue tracking
- Customer feedback collection
- Comprehensive booking management (create, view, cancel, delete)
- Staff dashboard for monitoring business metrics

## Table of Contents

- [Introduction](#Intoduction)
- [Key Features](#Key-Features)
- [UX - layout](#UX-layout)
   - [Login Page](#Login-Page)
   - [Main Page](#Main-Page)
   - [Make Booking Page](#Make-Booking-Page)
   - [My Booking Page](#My-Booking-Page)
   - [Booking Analytics Page](#Booking-Analytics-Page)
   - [NavBar](#NavBar)
   - [Analytical Dashboard](#Analytical-Dashboard)
   - [Admin Dashboard](#Admin-Dashboard)
   - [Delete All Bookings](#Delete-All-Bookings)
- [Installation and Setup](#Installation-and-Setup)
   - [Prerequisites](#Prerequisites)
   - [Clone the Repository](#Clone-the-Repository)
   - [Environment Setup](#Environment-Setup)
   - [Database Configuration](#Database-Configuration)
   - [Running the Application](#Running-the-Application)
   - [Running Tests](#Running-Tests)
- [Usage](#Usage)
- [Stretch Goals for the Django Restaurant Booking System](#Stretch-Goals-for-the-Django-Restaurant-Booking-System)
   - [Client-Based Stretch Goals ](#Client-Based-Stretch-Goals)
   - [Developer-Based Stretch Goals](#Developer-Based-Stretch-Goals)
- [Development Plan for Phantom Restaurant System](#Development-Plan-for-Phantom-Restaurant-System)
- [Entity Relationship Diagram](#Entity-Relationship-Diagram)
   - [DBdiagram Charts](#DBdiagram-Charts)
   - [Relationship](#Relationship)




## UX - layout
   ### Login Page
   This is the first page you see when opening the site, it has a responsive design so that it displays differently for different sized screens, the version shown here is for a Large screen.

   ![Login Page for full sized screen](booking/static/booking/image/login-page.png)

   ### Main Page
   This is the next and the main booking page you will see after logging into the website with username and password.

   ![Main Page for full sized screen](booking/static/booking/image/main-page.png)

   ### Make Booking Page
   This is the page where every bookings are being made, and it is linked to User and Table, which includes ```Booking_date, Booking_time, and Number_of_guests``` and after the data has been inputted a ```status with options: confirmed or cancelled.```

   ![Make Booking Page for full sized screen](booking/static/booking/image/make-booking.png)

   ### My Booking Page
   This page is where all my bookings are being stored and it is a page where I can also cancel any bookings that the customers don't need anymore. It is also the page where I can delete and cancel all bookings if the customers dont need the bookings.

   ![My Booking Page for full sized screen](booking/static/booking/image/my-bookings.png)

   ### Booking Analytics Page
   This is the page that Summarizes every booking trends such as the ```total_bookings, confirmed_bookings, cancelled_bookings,Customer_Feedback such as (rating (1-5 scale) and optional comment.), RevenueMetrics such as (Daily revenue, average revenue per booking, and per guest.)```
   This page also provides the insights into customer behavior such as the Total bookings, cancellations, spending, and dining preferences.

   ![My Booking Page for full sized screen](booking/static/booking/image/analytical-page.png)

   ### NavBar
   It has a fully functional navbar:
   Large screen version
   ![NavBar full sized screen](booking/static/booking/image/navbar.png)

   Small screen version

   ![Small screen NavBar](booking/static/booking/image/small-size.png)

   You can see that every icons still appears on the NavBar, such as making a booking, viewing every of your booking confirmations you have made, and view the analytical page for every booking trends you have made so far, such as Total Revenue, Average Revenue per Booking and Total Guests etc.
   Everytime a booking is made, it says ```booking confirmed! Check your Email for details```

   ![big screen NavBar](booking/static/booking/image/navbar-confirmationbig.png)

   immediately you received the confirmation email, it will automatically be updated on the admin panel, and the analytical dashboard

   ### Analytical Dashboard
   ![analytical dashboard](booking/static/booking/image/analytical-page.png)

   ### Admin Dashboard
   ![admin dashboard](booking/static/booking/image/dashboad.png)

   ### Delete All Bookings
   Although if the customer want to cancel every booking, you have to scroll down to my bookings page, by highlighting ```Delete All Bookings```button below which will take you to a warning page for confirmation, before making a final decision.

   ![analytical dashboard](booking/static/booking/image/delete-bookings.png)


## Installation and Setup

   ### Prerequisites
   The following tools were installed during the cost of building this site.
   - Python 3.8+
   - Django 4.x
   - PostgreSQL (or SQLite for development)
   - Git
   - pip

   ### Clone the Repository
   I had to clone the repository to my local machine using 
   ```https://github.com/Ebuka-martins/restaurant_project.git ```

   ````
   cd restaurant_project
   `````

   ### Environment Setup
    I had to Create a virtual environment and activate it
    ```
    python3 -m venv env
    source env/bin/activate 
    ```
   I had to install dependencies, during the cause of creating this site 
   ```pip3 install -r requirements.txt```

   Furthermore I had to create an env.py file and configure environment variables directly:
   ```
   import os
   os.environ["SECRET_KEY"] = "my-secret-key"
   os.environ["DEBUG"] = "True"  # Set to "False" 
   os.environ["DATABASE_URL"] = "my-database-url"  
   ```
   ### Database Configuration
   By default, the system supports both PostgreSQL (preferred for production) and SQLite (default fallback).
   and Apply database migrations: 
   ```
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
   ### Running the Application
   Start the development server by ```python3 manage.py runserver```
   
   ### Running Tests
   Run the test suite by ```python3 manage.py test```

## Usage
During the creation of my site, I had to state a simple usage steps for simple users which are as follows:
   - Register or log in as a user.
   - Navigate to the booking page to reserve a table.
   - Use the dashboard to view, update, or cancel reservations.
   - Restaurant admins can manage tables and analyze customer trends.

## Stretch Goals for the Django Restaurant Booking System
### Client-Based Stretch Goals   
These goals focus on enhancing the user experience and meeting client expectations.
 #### 1. Dynamic Table Availability Visualization
   - Add a real-time visual representation of table availability using a graphical layout of the restaurant.
   - Highlight available, booked, and reserved tables.
 #### 2. Loyalty Program Integration
   - Implement a rewards system where customers earn points for every booking or feedback submission.
   - Allow customers to redeem points for discounts or exclusive offers.   
 #### 3. Mobile App Compatibility
   - Develop a companion mobile app to make bookings, view menus, and provide feedback more conveniently.
   - Add push notifications for booking reminders and promotions.   
 #### 4. Personalized Recommendations
   - Use customer insights (e.g., preferred dining times and average group size) to offer personalized booking time slots or menu suggestions.   
 #### 5. Feedback-Based Promotions
   - Analyze customer feedback and automatically send personalized promotions or apologies based on ratings.
 #### 6. Special Event Bookings      
   - Allow customers to book tables for special occasions (e.g., birthdays, anniversaries) with customization options such as decorations and special menus.
 #### 7. Special Event Bookings    
   - Seamless Payment Integration
   - Include options for split payments or paying for the meal in advance.
### Developer-Based Stretch Goals
These goals focus on system scalability, maintainability, and developer experience.
#### 1. Automated Testing Suite
   - Develop a comprehensive automated testing framework to cover unit, integration, and end-to-end tests.
   - Include stress tests to simulate high booking traffic.
#### 2. Improved Analytics Dashboard
   - Add more advanced analytics such as customer retention rates, average revenue growth, and peak booking hours.
#### 3. Performance Optimization  
   - Implement caching (e.g., using Redis) for frequently accessed data like table availability and menu items.

## Development Plan for Phantom Restaurant System
### 1.  Models Implementation
   ### Tables:
   ✅ Design Table models to manage table capacity and availability.
   ### Bookings:
   ✅ Create Booking models with fields for user details, table assignment, date, time, and status. Enforce constraints to prevent double-booking via unique_together.
   ### Feedback:
   ✅ Include a CustomerFeedback model for users to rate their experiences and leave comments.
   ### Analytics:
   ✅ Add BookingAnalytics and RevenueMetrics models to track operational data, such as booking trends and revenue. Include a CustomerInsights model for user-specific metrics.
### 2. Forms
   ✅ Develop BookingForm to collect user inputs for reservations and validate data (e.g., number of guests).
### 3. Views
   ### Make Booking:
   ✅ Implement the make_booking view to handle reservation logic.

   ✅ Match guest count with table capacity.

   ✅ Ensure availability for the selected time and date.

   ✅ Automatically update analytics and revenue data after successful booking.
   ### Booking List:
   ✅ Allow users to view their upcoming and past reservations with the booking_list view.
   ### Cancel Booking:
   ✅ Provide a mechanism to cancel reservations and reflect these changes in analytics.
   ### Delete All Bookings:
   ✅ Add functionality to allow users to delete all their bookings, while updating related metrics and feedback records.
   ### Analytics Dashboard:
   ✅ Create an admin dashboard (AnalyticsDashboardView) for viewing and analyzing booking trends, feedback ratings, and revenue over time.

## Entity Relationship Diagram   
   **DBdiagram Charts**
      * The starting point for the entity relationships was drawn up as a entity relationship diagram using [dbdiagram charts](https://dbdiagram.io/home), and was shown as follows below
     
   ![dbdiagram dashboard](booking/static/booking/image/booking-table.png)
    **Relationship**
   - **User** → **Booking:** One user can make multiple bookings.
   - **Table** → **Booking:** One table can be associated with multiple bookings.

As part of this process I used a kanban board to monitor user stories, and ensure I complete everything the client wanted, as Shown below is a screenshot of the kanban board I created for this project.   

| ![booking/static/booking/image/kanban-board.png](booking/static/booking/image/kanban-board.png) | ![booking/static/booking/image/kanban-issue.png](booking/static/booking/image/kanban-issue.png) |
|:-------------------------------------------:|:-------------------------------------------:|
| **Kanban board** | **Kanban Issue** |


## Design 
### Color Design




  

