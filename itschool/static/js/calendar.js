document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      slotMinTime: '08:00:00',
      slotMaxTime: '20:00:00',
      events: '/api/events/',  // URL для получения событий от Django
      eventClick: function(info) {
        // Обработка клика по событию
        alert('Урок: ' + info.event.title);
      }
    });
    calendar.render();
  });