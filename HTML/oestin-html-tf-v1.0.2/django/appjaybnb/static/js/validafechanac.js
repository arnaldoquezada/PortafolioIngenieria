        function validFechaNac() {
        var today = new Date().toISOString().split('T')[0];

        var maxDate = new Date().toISOString().split('T')[0];
    		document.getElementsByName("fechanac")[0].setAttribute('max', today)

        }
