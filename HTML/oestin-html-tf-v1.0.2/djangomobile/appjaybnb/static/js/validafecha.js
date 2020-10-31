        function validDate() {
        var today = new Date().toISOString().split('T')[0];
    		document.getElementsByName("arrive")[0].setAttribute('min', today);
        var today = new Date().toISOString().split('T')[0];
    		document.getElementsByName("departure")[0].setAttribute('min', today);

        var maxDate = new Date(new Date().getTime() + 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    		document.getElementsByName("arrive")[0].setAttribute('max', maxDate)
        var maxDate = new Date(new Date().getTime() + 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    		document.getElementsByName("departure")[0].setAttribute('max', maxDate)
        }
        