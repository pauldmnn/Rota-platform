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
                weekDisplay.textContent = `Week Commencing: ${data.start_of_week} to ${data.end_of_week}`;
                rotaHeader.innerHTML = "<th>Staff Name</th>";
                rotaBody.innerHTML = "";

                data.week_dates.forEach((date) => {
                    const th = document.createElement("th");
                    th.textContent = new Date(date).toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
                    rotaHeader.appendChild(th);
                });

                data.rota_data.forEach((staff) => {
                    const row = document.createElement("tr");
                    const nameCell = document.createElement("td");
                    nameCell.textContent = staff.user || "Unnamed";
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
            })
            .catch((error) => console.error("Error fetching rota data:", error));
    };

    prevBtn.addEventListener("click", () => {
        weekOffset--;
        fetchRotaData();
    });

    nextBtn.addEventListener("click", () => {
        weekOffset++;
        fetchRotaData();
    });

    fetchRotaData();
});
