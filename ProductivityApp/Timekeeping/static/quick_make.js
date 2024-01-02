$(document).ready(function () {
    // Handle form submission via AJAX
    $('#quick-add-form').on('submit', function (e) {
        e.preventDefault();

        // Create an empty formData object
        var formData = new FormData($(this)[0]);

        // Check if the 'show_date' URL parameter exists
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('show_date')) {
            // Get the 'show_date' parameter value
            var showDate = urlParams.get('show_date');

            // Append 'show_date' to the formData
            formData.append('show_date', showDate);
        }

        // Send an AJAX POST request to create the new entry
        $.ajax({
            type: 'POST',
            url: '/quick_create_task', // Replace with your actual URL
            data: formData,
            processData: false, // Prevent jQuery from processing the data
            contentType: false, // Prevent jQuery from setting content type
            success: function (data) {
                if (data.status === 'success') {
                    // Reload the page after a successful action
                    window.location.reload();
                }
            },
            error: function () {
                // Handle errors if necessary
                alert('Error creating the entry.');
            }
        });
    });
});
