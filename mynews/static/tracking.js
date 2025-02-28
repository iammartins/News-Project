// Function to send a tracking request (generic)
function trackEvent(eventType, details) {
    fetch('/analysis/track_event/', { // Replace with your actual URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: `event_type=${eventType}&details=${details}` // Encode data
    });
}

// Track site visit (on page load)
window.addEventListener('load', function() {
    trackEvent('site_visit', window.location.pathname); // Pass the current path as details
});

// Example: Track a button click
const myButton = document.getElementById('myButton'); // Replace with your button's ID
if (myButton) { // Check if the element exists
    myButton.addEventListener('click', function() {
        trackEvent('button_click', 'Clicked the "My Button"'); // Example details
    });
}

// Example: Track form submission (replace 'myForm' with your form's ID)
const myForm = document.getElementById('myForm');
if (myForm) {
    myForm.addEventListener('submit', function() {
        trackEvent('form_submission', 'Form submitted'); // Example details
    });
}

//Example: Track when user start reading a post

// Function to track when user starts reading a post
function trackPostRead(postId) {
    trackEvent('post_read_start', postId);
}

// Example: Call the function when the user scrolls past a certain point in the post
const postContent = document.querySelector('.post-content'); // Replace with your post content selector
if (postContent) {
    let postRead = false; // Flag to prevent multiple tracking calls

    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        const triggerPoint = postContent.offsetTop + postContent.offsetHeight * 0.2; // 20% of the post height

        if (scrollPosition > triggerPoint && !postRead) {
            trackPostRead(postContent.dataset.postId); // Assuming you have a data-post-id attribute
            postRead = true;
        }
    });
}


//Example: Track when user ends reading a post

function trackPostReadEnd(postId) {
    trackEvent('post_read_end', postId);
}

// Example: Call the function when the user scrolls past a certain point in the post
if (postContent) {
    let postReadEnd = false; // Flag to prevent multiple tracking calls

    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        const triggerPoint = postContent.offsetTop + postContent.offsetHeight * 0.9; // 90% of the post height

        if (scrollPosition > triggerPoint && !postReadEnd) {
            trackPostReadEnd(postContent.dataset.postId); // Assuming you have a data-post-id attribute
            postReadEnd = true;
        }
    });
}
