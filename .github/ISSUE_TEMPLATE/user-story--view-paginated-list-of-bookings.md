---
name: 'USER STORY: View Paginated List of Bookings'
about: View Paginated List of Bookings
title: ''
labels: ''
assignees: ''

---

As a logged-in user **I want to** view a paginated list of my bookings
**So that** I can track all my restaurant reservations

**Acceptance Criteria**
> **AC1** Given I am logged in. 
> **AC2** When I access the booking list page.
> **AC1** Then I see all my bookings ordered by date and time.
> **AC2** And each booking shows table number, date, time, and status.
> **AC1** And bookings are paginated if there are many.

**Technical Notes**
> **AC1** Uses existing `booking_list` view
> **AC2** Leverages `Booking` model with fields: user, table, booking_date, booking_time, status.
> **AC1** Currently implements `@login_required` decorator
