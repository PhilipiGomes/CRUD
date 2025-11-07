// Minimal JS to submit forms as JSON for the API endpoints
(function () {
    function formToJson(form) {
        const data = {};
        new FormData(form).forEach((v, k) => data[k] = v);
        return JSON.stringify(data);
    }

    function ajaxPost(form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = form.action;
            fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: formToJson(form),
                credentials: 'same-origin'
            }).then(r => r.json().then(j => ({ status: r.status, body: j }))).then(resp => {
                if (resp.status >= 400) {
                    alert(resp.body.message || 'Erro');
                    return;
                }
                // on success, redirect to users list
                window.location = '/usuarios/list';
            }).catch(err => {
                console.error(err); alert('Erro de rede');
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        const login = document.getElementById('loginForm');
        if (login) ajaxPost(login);
        const cad = document.getElementById('cadastroForm');
        if (cad) ajaxPost(cad);
    });

    // expose a logout helper
    window.logout = function () {
        fetch('/logout', { method: 'POST', credentials: 'same-origin' }).then(() => window.location = '/login');
    }
})();
