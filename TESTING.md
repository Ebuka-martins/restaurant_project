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
|  |  | Preserve intended destination | Next parameter set to root URL '/' | yes | - |
|  |  | Prevent unauthorized access | No booking list details exposed | Yes | - |
| **Create Booking** | Successful Booking | Successful booking creation | Booking object created in database | Yes | - |
|  |  | Correct booking details | Validate date matches input | Yes | - |
|  |  |  | Verify time matches input | Yes | - |
|  |  |  | Check guest count accuracy | Yes | - |
|  |  | Automatic status assignment | Status set to 'confirmed' | Yes | - |
|  | | Analytics update | Total bookings incremented | Yes | - |
|  |  |  | Total guests count updated | Yes | - |
| **Cancel Booking** | Booking Cancellation | Successful cancellation | Booking status changed to 'cancelled' | Yes | - |
|  |  | Redirect to booking list | HTTP 302 redirect to booking list | Yes | - |
|  |  | Analytics tracking | Cancelled bookings count incremented | Yes | - |
|  | | Database state update | Original booking record modified | Yes | - |
| **Delete All Bookings** | Bulk Deletion | Remove all user bookings | Zero bookings for specific user | Yes | - |
|  |  | Analytics reset | Total bookings count set to 0 | Yes | - |
|  |  | Successful redirection | Redirect to booking list page | Yes | - |
| **Analytics Dashboard** | Dashboard View | Successful page load | HTTP 200 OK status code | Yes | - |
|  |  | Correct template used | 'booking/analytics_dashboard.html' rendered | Yes | - |
| | | Context data availability | Analytics data present | Yes | - |
|  |  |  |  Revenue metrics included | Yes | - |
|  |  | Data accuracy | Matches pre-created test data | Yes | - |

---