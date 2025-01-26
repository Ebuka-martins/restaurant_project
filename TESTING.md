# Phantom Restaurant Booking System Testing

Return to [README](README.md).

## SYSTEM Testing

I conducted both automated and manual testing for the
- **Booking List**
- **Create Booking**
- **Cancel Booking**
- **DeleteAll Bookings**
- **Analytics Dashboard**

### Manual Testing Table

In total I constructed 5 tests to test the majority of the functions within the Table, broken down into 5 sections:

 | **Category** | **Test Method**| **Expected Outcome** | **Detailed Validation Criteria** | **passed** | **comments** |
| --- | --- | --- | --- | --- | --- |
| **Booking List** | Authenticated View |  HTTP 200 OK status code |  Verify response is successful | Yes | - |
|  |  |  Correct template rendered |  Check 'booking/booking_list.html' is used | Yes | - |
|  |  |  Booking details displayed |  Validate table number appears | Yes | - |
|  |  |   |  Confirm guest count shown | Yes | - |
|  |  |   |  Check booking status visible | Yes | - |
|  |  | Correct booking in context  |  Verify single booking object | Yes | - |
|  |  |   |  Check booking matches created instance | Yes | - |
| **Booking List** | Unauthenticated View | Redirect to login page |  HTTP 302 redirect status | Yes | - |
|  |  |  | Yes | Yes | - |
| Help | Click on the "Help" link | The user is redirected to the help page section | Yes | Yes | - |
| Main Page | | | | | |
| Home | Click on the "Home" link | The user is redirected to the booking page section immediately they fill out the form | Yes | Yes | - |
| Booking | Click on the "Booking" link | The user is redirected to the responsive page section immediately they have filled out the forms below, this shows they have booked for their flight | Yes | Yes | - |
| Contact | Click on the "Contact" link | The user is redirected to the contact page section where every contact is meant| Yes | Yes | - |
| Help | Click on the "Help" link | The user is redirected to the help page section where they can get a quick answers to their compaint | Yes | Yes | - |
| Footer | | | | | |
| Twitter x icon in the footer | Click on the Twitter x icon | The user is redirected to the Twitter x page | Yes | Yes | - |
| Facebook icon in the footer | Click on the Facebook icon | The user is redirected to the Facebook page | Yes | Yes | - |
| YouTube icon in the footer | Click on the YouTube icon | The user is redirected to the YouTube page | Yes | Yes | - |
| Instagram icon in the footer | Click on the Instagram icon | The user is redirected to the instagram page | Yes | Yes | - |
| Home page Section | | | | | |
| Username name input | Enter the username name | The username name is entered | Yes | Yes | If user doesn't enter the first name, the message saying you should fill out this field will appears |
| Password input | Enter the Password | The password is entered | Yes | Yes | If user doesn't enter the password, the message saying you should fill out this field will appears |
| input Label | Tick the radio | Tick radio is required | Yes | Yes | If user doesn't tick the radio, the message please select one of these options will appear |
| From and Return Dates | Click on the dates | The dates brings out the date of choice | Yes | Yes | These dates are required to enable the users decide the time of their choice|
| "Submit" button | Click on the "Submit" button | The user is redirected to the booking page section | Yes | Yes | - |
| Booking page Section| | | | | |
| First name input | Enter the first name | The first name is entered | Yes | Yes | If user doesn't enter the first name, the message saying you should fill out this field will appears appears |
| Last name input | Enter the last name | The last name is entered | Yes | Yes | If user doesn't enter the last name, the message saying you should fill out this field will appears |
| Email input | Enter the email | The email is entered | Yes | Yes | If user doesn't enter the email, the error message appears. which says you should fill out the required field |
| Destination input | Select the destination | Destination choice is entered | Yes | Yes | If user doesn't enter the destination, the error message appears. which says you should fill out the required field |
| input Label | Tick the Ticket type | Tick type is required | Yes | Yes | If user doesn't tick the radio, the message please select one of these options will appear |
| input Checkbox | Tick the Checkbox | Checkbox is required | Yes | Yes | If user doesn't tick the radio, the message please check this box if you want to proceed will appear |
| "Submit" button | Click on the "Submit" button | The user is redirected to the responsive page section | Yes | Yes | - |
| "Reset" button | Click on the "Reset" button | The user is allowed to refresh their booking application if they fill they have make a error | Yes | Yes | - |
| Help page Section| | | | | |
| Details and Summary | Click the Details | Click the summary box is required | Yes | Yes | If user clicked the summary the solution to the quastion will come up |