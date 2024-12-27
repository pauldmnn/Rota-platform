document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.shift-select').forEach(select => {
        select.addEventListener('change', function () {
            const cell = this.closest('td');
            const customInput = cell.querySelector('.custom-time-input');
            if (this.value === 'Custom') {
                customInput.style.display = 'block';
            } else {
                customInput.style.display = 'none';
            }
            updateRota(cell);
        });
    });

    document.querySelectorAll('.start-time, .end-time').forEach(input => {
        input.addEventListener('change', function () {
            const cell = this.closest('td');
            updateRota(cell);
        });
    });

    function updateRota(cell) {
        const userId = cell.getAttribute('data-user-id');
        const date = cell.getAttribute('data-date');
        const shiftType = cell.querySelector('.shift-select').value;
        const startTime = cell.querySelector('.start-time') ? cell.querySelector('.start-time').value : '';
        const endTime = cell.querySelector('.end-time') ? cell.querySelector('.end-time').value : '';

        fetch(cell.getAttribute('data-update-url'), {
            method: 'POST',
            headers: {
                'X-CSRFToken': cell.getAttribute('data-csrf-token'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                date: date,
                shift_type: shiftType,
                start_time: startTime,
                end_time: endTime,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'success') {
                alert(data.message || 'Failed to update shift');
            }
        })
        .catch(error => console.error('Error:', error));
    }
});


