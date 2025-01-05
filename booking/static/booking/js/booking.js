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
                alert('For parties larger than 20, please contact us directly.');
            }
        });
    }

    // Form validation
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            const date = new Date(dateInput.value);
            if (date < new Date()) {
                e.preventDefault();
                alert('Please select a future date.');
                return;
            }

            if (!timeSelect.value) {
                e.preventDefault();
                alert('Please select a time slot.');
                return;
            }
        });
    }

    function validateDate(e) {
        const selected = new Date(e.target.value);
        const today = new Date();
        
        if (selected < today) {
            alert('Please select a future date.');
            e.target.value = '';
        }
    }
});