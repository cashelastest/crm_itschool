document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('packForm');
    const schedulesContainer = document.getElementById('schedulesContainer');
    const addScheduleBtn = document.getElementById('addScheduleBtn');
    const scheduleTemplate = document.getElementById('scheduleTemplate');

    let formData = {
        name: '',
        lessonsNumber: '',
        validityPeriod: '',
        course: '',
        price: '',
        schedules: []
    };

    // Add initial schedule
    addSchedule();

    // Event Listeners
    addScheduleBtn.addEventListener('click', addSchedule);
    form.addEventListener('submit', handleSubmit);

    function addSchedule() {
        const scheduleItem = scheduleTemplate.content.cloneNode(true);
        const deleteBtn = scheduleItem.querySelector('.delete-schedule-btn');
        
        deleteBtn.addEventListener('click', function(e) {
            const scheduleElements = schedulesContainer.querySelectorAll('.schedule-item');
            if (scheduleElements.length > 1) {
                e.target.closest('.schedule-item').remove();
                updateFormData();
            }
        });

        const inputs = scheduleItem.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', updateFormData);
        });

        schedulesContainer.appendChild(scheduleItem);
    }

    function updateFormData() {
        // Get all inputs and selects from pack details
        const packInputs = form.querySelectorAll('.pack-details input, .pack-details select');
        packInputs.forEach(input => {
            formData[input.name] = input.value;
        });

        // Specifically get the course select value
        const courseSelect = form.querySelector('select[name="course"]');
        if (courseSelect) {
            formData.course = courseSelect.value;
        }

        const scheduleElements = schedulesContainer.querySelectorAll('.schedule-item');
        formData.schedules = Array.from(scheduleElements).map(scheduleEl => {
            return {
                dayOfWeek: scheduleEl.querySelector('[name="dayOfWeek"]').value,
                startTime: scheduleEl.querySelector('[name="startTime"]').value,
                endTime: scheduleEl.querySelector('[name="endTime"]').value
            };
        });
    }

    function handleSubmit(e) {
        e.preventDefault();
        updateFormData();
        
        // Get the CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('/pack/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Add CSRF token
            },
            body: JSON.stringify({
                data: formData,
            })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }

    // Add event listeners to all pack detail inputs and selects
    const packInputs = form.querySelectorAll('.pack-details input, .pack-details select');
    packInputs.forEach(input => {
        input.addEventListener('input', updateFormData);
    });
});