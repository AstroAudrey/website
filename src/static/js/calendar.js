// comment here lol idk
document.addEventListener('DOMContentLoaded', () => {
    const calendarDates = document.getElementById('calendar-dates');
    const monthYear = document.getElementById('month-year');

    const months = [
        '01', '02', '03', '04', '05', '06',
        '07', '08', '09', '10', '11', '12'
    ];

    let currentDate = new Date();

    function renderCalendar() {
        calendarDates.innerHTML = '';
        monthYear.textContent = `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

        const firstDayIndex = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
        const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();

        // Create blank spaces for days of the week before the first day of the month
        for (let i = 0; i < firstDayIndex; i++) {
            const day = document.createElement('div');
            day.textContent = '';
            calendarDates.appendChild(day);
        }

        // Display the days of the current month
        for (let i = 1; i <= lastDay; i++) {
            const day = document.createElement('div');
            day.textContent = i;
            if (i === currentDate.getDate() && currentDate.getMonth() === new Date().getMonth() && currentDate.getFullYear() === new Date().getFullYear()) {
                day.classList.add('today');
            }
            calendarDates.appendChild(day);
        }
    }

    renderCalendar();
});