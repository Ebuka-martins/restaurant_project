document.addEventListener('DOMContentLoaded', function() {
    // Time slot selection
    const timeSlots = [
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
        '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
        '20:00', '20:30', '21:00'
    ];

    // Get form elements
    const dateInput = document.getElementById('id_booking_date');
    const timeSelect = document.getElementById('id_booking_time');
    const guestsInput = document.getElementById('id_number_of_guests');
    const bookingForm = document.getElementById('booking-form');
    const editBookingForm = document.getElementById('edit-booking-form');
    const menuContainer = document.querySelector('.menu-container');

    // Populate time slots for both new and edit forms
    function populateTimeSlots(selectElement) {
        if (selectElement) {
            selectElement.innerHTML = '';
            timeSlots.forEach(slot => {
                const option = document.createElement('option');
                option.value = slot;
                option.textContent = slot;
                selectElement.appendChild(option);
            });
        }
    }

    // Populate time slots for both forms
    populateTimeSlots(timeSelect);
    if (editBookingForm) {
        populateTimeSlots(document.getElementById('id_booking_time'));
    }

    // Guest number validation
    function setupGuestValidation(formElement) {
        const guestsInput = formElement.querySelector('input[name="number_of_guests"]');
        if (guestsInput) {
            guestsInput.addEventListener('change', function() {
                const value = parseInt(this.value);
                if (isNaN(value) || value < 1) {
                    this.value = 1;
                } else if (value > 20) {
                    this.value = 20;
                    Swal.fire({
                        title: 'Large Group Booking',
                        text: 'For parties larger than 20, please contact us directly at +353 899 728 953 for special arrangements.',
                        icon: 'info',
                        confirmButtonText: 'Got it!',
                        confirmButtonColor: '#3498db',
                        showClass: {
                            popup: 'animate__animated animate__fadeInDown'
                        },
                        hideClass: {
                            popup: 'animate__animated animate__fadeOutUp'
                        }
                    });
                }
            });
        }
    }

    // Setup validation for both forms
    if (bookingForm) {
        setupGuestValidation(bookingForm);
    }
    if (editBookingForm) {
        setupGuestValidation(editBookingForm);
    }

    // Date validation
    function validateDate(e) {
        const selected = new Date(e.target.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selected < today) {
            Swal.fire({
                title: 'Invalid Date',
                text: 'Please select a future date.',
                icon: 'error',
                confirmButtonColor: '#3498db'
            });
            e.target.value = '';
        }
    }

    // Menu responsiveness
    function adjustMenuLayout() {
        if (menuContainer) {
            if (window.innerWidth < 768) {
                menuContainer.style.padding = '1.5rem';
                menuContainer.style.margin = '1rem';
            } else {
                menuContainer.style.padding = '2.5rem';
                menuContainer.style.margin = '2rem auto';
            }
        }
    }

    // Add event listeners
    window.addEventListener('resize', adjustMenuLayout);
    adjustMenuLayout();

    if (dateInput) {
        const today = new Date();
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 2);
        
        dateInput.min = today.toISOString().split('T')[0];
        dateInput.max = maxDate.toISOString().split('T')[0];
        dateInput.addEventListener('change', validateDate);
    }

    // Form submissions
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            const date = new Date(dateInput.value);
            const guestsInput = this.querySelector('input[name="number_of_guests"]');
            const value = parseInt(guestsInput.value);

            if (date < new Date()) {
                e.preventDefault();
                Swal.fire({
                    title: 'Invalid Date',
                    text: 'Please select a future date.',
                    icon: 'error',
                    confirmButtonColor: '#3498db'
                });
                return;
            }

            if (!timeSelect.value) {
                e.preventDefault();
                Swal.fire({
                    title: 'Time Required',
                    text: 'Please select a time slot.',
                    icon: 'warning',
                    confirmButtonColor: '#3498db'
                });
                return;
            }

            if (value > 20) {
                e.preventDefault();
                guestsInput.value = 20;
                Swal.fire({
                    title: 'Large Group Booking',
                    text: 'For parties larger than 20, please contact us directly at +353 899 728 953 for special arrangements.',
                    icon: 'info',
                    confirmButtonText: 'Got it!',
                    confirmButtonColor: '#3498db'
                });
                return;
            }
        });
    }

    // Edit booking form handling
    if (editBookingForm) {
        editBookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const editDateInput = document.getElementById('id_booking_date');
            const editTimeSelect = document.getElementById('id_booking_time');
            const guestsInput = this.querySelector('input[name="number_of_guests"]');
            const value = parseInt(guestsInput.value);
            
            if (value > 20) {
                guestsInput.value = 20;
                Swal.fire({
                    title: 'Large Group Booking',
                    text: 'For parties larger than 20, please contact us directly at +353 899 728 953 for special arrangements.',
                    icon: 'info',
                    confirmButtonText: 'Got it!',
                    confirmButtonColor: '#3498db'
                });
                return;
            }

            Swal.fire({
                title: 'Confirm Changes',
                text: 'Are you sure you want to update this booking?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Yes, update it!',
                cancelButtonText: 'No, cancel',
                confirmButtonColor: '#4CAF50',
                cancelButtonColor: '#f44336'
            }).then((result) => {
                if (result.isConfirmed) {
                    editBookingForm.submit();
                }
            });
        });
    }
});