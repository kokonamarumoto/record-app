


document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const events = JSON.parse(document.getElementById('calendar-events').textContent);

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'ja',
    events: events,
    height: 'auto',
    contentHeight: 'auto',
    expandRows: true,
    fixedWeekCount: false,
    eventDisplay: 'block',
    
    
    eventClick: function(info) {
      if (info.event.url) {
        info.jsEvent.preventDefault();
        window.location.href = info.event.url;
      }
    }
  });

  calendar.render();
});
