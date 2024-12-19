document.addEventListener("DOMContentLoaded", () => {
    const prevBtn = document.getElementById("prev-week");
    const nextBtn = document.getElementById("next-week");
    const weekDisplay = document.getElementById("week-display");
    const rotaHeader = document.getElementById("rota-header");
    const rotaBody = document.getElementById("rota-body");

    let weekOffset = 0;

    const fetchRotaData = () => {
        fetch(`/admin/weekly_rota_api/?week_offset=${weekOffset}`)
            .then((response) => response.json())
            .then((data) => {
                // Update week display
                weekDisplay.textContent = `Week Commencing: ${data.start_of_week} to ${data.end_of_week}`;

                // Update rota header
                rotaHeader.innerHTML = "<th>Staff Name</th>";
                data.week_dates.forEach((date) => {
                    const th = document.createElement("th");
                    th.textContent = new Date(date).toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
                    rotaHeader.appendChild(th);
                });

                // Update rota body
                rotaBody.innerHTML = "";
                data.rota_data.forEach((staff) => {
                    const row = document.createElement("tr");
                    const nameCell = document.createElement("td");
                    nameCell.textContent = staff.user;
                    row.appendChild(nameCell);

                    data.week_dates.forEach((date) => {
                        const cell = document.createElement("td");
                        const shift = staff.shifts[date];
                        if (shift) {
                            cell.innerHTML = `${shift.shift_type}<br>${shift.start_time} - ${shift.end_time}`;
                        } else {
                            cell.textContent = "-";
                        }
                        row.appendChild(cell);
                    });

                    rotaBody.appendChild(row);
                });
            });
    };

    // Event listeners for week navigation
    prevBtn.addEventListener("click", () => {
        weekOffset--;
        fetchRotaData();
    });

    nextBtn.addEventListener("click", () => {
        weekOffset++;
        fetchRotaData();
    });

    // Initial fetch
    fetchRotaData();
});
