$(document).ready(function () {
    // Show the modal when the button is clicked
    $('#newTrainDataModalButton').click(function () {
        $('#newTrainDataModal').modal('show');
    });

    // Hide the modal when the form is submitted
    $('#newTrainDataForm').submit(function () {
        $('#newTrainDataModal').modal('hide');
    });

        // Intercept the form submission
    $('#newTrainDataForm').submit(function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Create a FormData object to send the form data including files
        var formData = new FormData(this);

        // Make an AJAX request
        $.ajax({
            type: 'POST',
            url: createTrainDataUrl,
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                // Handle success (if needed)
                console.log(response);
                setTimeout(function () {
                    location.reload();
                }, 2000); 
            },
            error: function (error) {
                // Handle errors (if needed)
                console.log(error);
            }
        });
    });
});
