// We need to change to button without reloading now
// Need to add a post for the Phases

document.addEventListener('DOMContentLoaded', function() {

    // Get the phase Form
    document.querySelector('.phase_form').addEventListener('submit', function(e) {
        e.preventDefault();

        //  Get the project id
        const project_id = this.dataset.id;

        // Get all of the values from the FormData, as you would regularly in JS
        const name = document.querySelector('#name').value;
        const start = document.querySelector('#start').value;
        const end = document.querySelector('#end').value;
        const completed = document.querySelector('#completed').value;

        // create the post method 
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

        // Create a template literal of the Phase and add instanceof, it works
       })
       .catch( (error) => console.log(error))
       

        
    })


   

    document.querySelectorAll('.completed_toggle').forEach( el => {
        el.addEventListener('click', function(e) {
            e.preventDefault();

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
        });
    });
});

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