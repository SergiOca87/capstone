// TODO - Make the pahe toggle dynamic, the forEach only accounts for existing elements

document.addEventListener('DOMContentLoaded', function() {

    addListeners();

    // Get the phase Form
    document.querySelector('.phase_form').addEventListener('submit', function(e) {
        e.preventDefault();

        //  Get the project id
        const project_id = this.dataset.id;

        // Get all of the values from the FormData, as you would regularly in JS
        const name = document.querySelector('#name').value;
        const start = document.querySelector('#start').value;
        const end = document.querySelector('#end').value;
        const completed = document.querySelector('#completed').checked;
        let latest_phase_id = this.dataset.latest;

       fetch(`/project/${project_id}`, {
            method: 'POST',
            credentials : 'include', // For Cors
            credentials : 'same-origin', // For same origin requests 
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                name,
                start,
                end, 
                completed
            })
       })
       .then( () => {

            fetch(`/phase/${latest_phase_id}`)
                .then(response => response.json())
                .then(data => {
                    const phase = `
                    <li class="list-group-item">
                        <p>${data.name}</p>
                        <p>Start: ${data.start_date}</p>
                        <p>End: ${data.end_date}</p>
                        <a class="completed_toggle btn btn-outline-danger" href="#" data-project="${project_id}" data-completed="${data.completed}" data-id="${data.id}">Not Completed</a>
                    </li>
                `

                    document.querySelector('.list-group-flush').insertAdjacentHTML('beforeend', phase);
                    addListeners();
                })
       })
       .then( () => {

            // Add 1 to the data id on the form, so we can add a new phase without an id conflict
           let latest_phase_id_int = parseInt(latest_phase_id);
           latest_phase_id_int++
           document.querySelector('.phase_form').setAttribute('data-latest', latest_phase_id_int.toString())
       })

       .catch( (error) => console.log(error))
    })

});

function addListeners() {
    console.log('addlisteners run')
    document.querySelectorAll('.completed_toggle').forEach( el => {
        el.addEventListener('click', function(e) {
            e.preventDefault();
            completeToggle(el)
        })
    });
}

function completeToggle(el) {

    console.log('complete toogle')
   
    // Get the Phase ID
    const phase_id = el.dataset.id;
    const completed = el.dataset.completed === 'true' ? 'False' : 'True';
    const project_id = el.dataset.project;

    fetch(`/phase/${phase_id}`, {
        method: 'PUT',
        credentials : 'include', // For Cors
        credentials : 'same-origin', // For same origin requests 
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            completed: completed
        })
    })
    .then( () => {
        if( el.classList.contains('btn-outline-danger') ) {
            el.classList.remove('btn-outline-danger');
            el.classList.add('btn-outline-success');
            el.textContent = 'Completed';
            el.dataset.completed = 'true';
        } else {
            el.classList.remove('btn-outline-success');
            el.classList.add('btn-outline-danger');
            el.textContent = 'Not Completed';
            el.dataset.completed = 'false';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });  
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;}


    // TODO:
    // Get rid of completed toggle on phase create?