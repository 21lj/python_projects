
    function add() {
        var qtyInput = document.getElementById('qty');
        var currentValue = parseInt(qtyInput.value);
        if (currentValue < 10) {
            qtyInput.value = currentValue + 1;
        }
    }

    function min() {
        var qtyInput = document.getElementById('qty');
        var currentValue = parseInt(qtyInput.value);
        if (currentValue > 1) {
            qtyInput.value = currentValue - 1;
        }
    }

    
