document.addEventListener('DOMContentLoaded', function() {
    // Time slot selection
    const timeSlots = [
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
        '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
        '20:00', '20:30', '21:00'
    ];

    const dateInput = document.getElementById('id_booking_date');
    const timeSelect = document.getElementById('id_booking_time');
    const guestsInput = document.getElementById('id_number_of_guests');
    const bookingForm = document.getElementById('booking-form');

    // Populate time slots
    if (timeSelect) {
        timeSelect.innerHTML = '';
        timeSlots.forEach(slot => {
            const option = document.createElement('option');
            option.value = slot;
            option.textContent = slot;
            timeSelect.appendChild(option);
        });
    }

    // Date validation
    if (dateInput) {
        const today = new Date();
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 2); // Allow booking up to 2 months ahead

        dateInput.min = today.toISOString().split('T')[0];
        dateInput.max = maxDate.toISOString().split('T')[0];

        dateInput.addEventListener('change', validateDate);
    }

    // Guest number validation
    if (guestsInput) {
        guestsInput.addEventListener('change', function() {
            if (this.value < 1) this.value = 1;
            if (this.value > 20) {
                this.value = 20;
                Swal.fire({
                    title: 'Large Group Booking',
                    text: 'For parties larger than 20, please contact us directly at +353 234 567 890 for special arrangements.',
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

    // Form validation
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            const date = new Date(dateInput.value);
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
        });
    }

    function validateDate(e) {
        const selected = new Date(e.target.value);
        const today = new Date();
        
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
});