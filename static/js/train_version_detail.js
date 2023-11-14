function showUpdateForm() {
    $("#updateForm").show();
    $("#predictionForm").hide();
}

function showPredictionForm() {
    $("#updateForm").hide();
    $("#predictionForm").show();
}

// Intercept the form submission
$('#trainForm').submit(function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Create a FormData object to send the form data including files
    var formData = new FormData(this);

    // Make an AJAX request
    $.ajax({
        type: 'POST',
        url: trainURL,
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Handle success (if needed)
            console.log(response);
        },
        error: function (error) {
            // Handle errors (if needed)
            console.log(error);
        }
    });
});




// Intercept the form submission
$('#predictionForm').submit(function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Create a FormData object to send the form data
    var formData = new FormData(this);
    formData.forEach(function(value, key) {
        console.log(key + ': ' + value);
    });
    // Make an AJAX request
    $.ajax({
        type: 'POST',
        url: predictionURL,
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response)
            // Handle success and update the result element
            if ('prediction_scaled' in response && 'prediction_original' in response) {
                var resultText = `Predicted value (scaled): ${response.prediction_scaled}<br>`;
                resultText += `Predicted value (original): ${response.prediction_original}`;
                $('#predictionResult').html(resultText).removeClass('hidden');
            } else {
                // Handle error
                console.log(response.error);
            }
        },
        error: function (error) {
            // Handle errors (if needed)
            console.log(error);
        }
    });
});
