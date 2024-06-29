document.addEventListener('DOMContentLoaded', function() {
    const calendarBody = document.getElementById('calendar-body');
    const monthYear = document.getElementById('month-year');
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    const currentDate = today.getDate();

    function getDaysInMonth(month, year) {
        return new Date(year, month + 1, 0).getDate();
    }

    function renderCalendar(month, year) {
        const firstDay = new Date(year, month).getDay();
        const daysInMonth = getDaysInMonth(month, year);

        // Format the month as MM
        const formattedMonth = String(month + 1).padStart(2, '0');
        monthYear.textContent = `${formattedMonth}/${year}`;
        calendarBody.innerHTML = '';

        let date = 1;
        for (let i = 0; i < 6; i++) {
            const row = document.createElement('tr');

            for (let j = 0; j < 7; j++) {
                const cell = document.createElement('td');
                
                if (i === 0 && j < firstDay) {
                    cell.textContent = '';
                } else if (date > daysInMonth) {
                    break;
                } else {
                    cell.textContent = date;

                    if (date === currentDate && month === currentMonth && year === currentYear) {
                        cell.classList.add('today');
                    }

                    if (j === 0) {
                        cell.classList.add('sunday');
                    } else if (j === 6) {
                        cell.classList.add('saturday');
                    }

                    date++;
                }
                row.appendChild(cell);
            }

            calendarBody.appendChild(row);
        }
    }

    renderCalendar(currentMonth, currentYear);
});

