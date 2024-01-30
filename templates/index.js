$(document).ready(function() {
        $('#model').change(function() {
            var selectedModel = $(this).val();
            // Fetch the colors and storage options for the selected model
            $.getJSON('/get_options', {model: selectedModel}, function(data) {
                var colorOptions = '<option value="" selected>Choose...</option>';
                var storageOptions = '<option value="" selected>Choose...</option>';
                $.each(data.colors, function(key, value) {
                    colorOptions += '<option value="' + value + '">' + value + '</option>';
                });
                $.each(data.storage, function(key, value) {
                    storageOptions += '<option value="' + value + '">' + value + '</option>';
                });
                $('#color').html(colorOptions);
                $('#storage').html(storageOptions);
            });
        });
    });