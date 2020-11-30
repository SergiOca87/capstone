// We need to change to button without reloading now
// Need to add a post for the Phases

document.addEventListener('DOMContentLoaded', function() {

    console.log('script loaded');

    document.querySelectorAll('.completed_toggle').forEach( el => {
        el.addEventListener('click', function(e) {
            e.preventDefault();

            // Get the Phase ID
            const phase_id = el.dataset.id;
            const completed = el.dataset.completed === 'true' ? 'False' : 'True';
            console.log(completed)
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
            .then( () => console.log('success'))
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