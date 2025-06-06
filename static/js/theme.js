document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length) {
        setTimeout(() => {
            alerts.forEach(el => {
                const bsAlert = new bootstrap.Alert(el);
                bsAlert.close();
            });
        }, 5000);
    }
});
