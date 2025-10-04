CTFd._internal.challenge.data = undefined;

CTFd._internal.challenge.renderer = null;

CTFd._internal.challenge.preRender = function () {};

CTFd._internal.challenge.render = null;

CTFd._internal.challenge.postRender = function () {};

CTFd._internal.challenge.submit = function (preview) {
    var challenge_id = parseInt(CTFd.lib.$("#challenge-id").val());
    var submission = CTFd.lib.$("#challenge-input").val();

    let alert = resetAlert();

    var body = {
        challenge_id: challenge_id,
        submission: submission,
    };
    var params = {};
    if (preview) {
        params["preview"] = true;
    }

    return CTFd.api
        .post_challenge_attempt(params, body)
        .then(function (response) {
            if (response.status === 429) {
                return response; // ratelimit
            }
            if (response.status === 403) {
                return response; // não logado / pausado
            }
            return response;
        });
};

function mergeQueryParams(parameters, queryParameters) {
    if (parameters.$queryParameters) {
        Object.keys(parameters.$queryParameters).forEach(function (parameterName) {
            var parameter = parameters.$queryParameters[parameterName];
            queryParameters[parameterName] = parameter;
        });
    }
    return queryParameters;
}

function resetAlert() {
    let alert = document.getElementById("deployment-info");
    alert.innerHTML = "";
    alert.classList.remove("alert-danger");
    return alert;
}

function toggleChallengeCreate() {
    let btn = document.getElementById("create-chal");
    btn.classList.toggle("d-none");
}

function toggleChallengeUpdate() {
    let btn = document.getElementById("extend-chal");
    btn.classList.toggle("d-none");

    btn = document.getElementById("terminate-chal");
    btn.classList.toggle("d-none");
}

function calculateExpiry(date) {
    let difference = Math.ceil((new Date(date * 1000) - new Date()) / 1000 / 60);
    return difference;
}

function createChallengeLinkElement(data, parent) {
    var expires = document.createElement("span");
    expires.textContent =
        "A instância termina em " +
        calculateExpiry(new Date(data.expires)) +
        " minutos.";
    parent.append(expires);
    parent.append(document.createElement("br"));

    if (data.connect == "tcp") {
        let codeElement = document.createElement("code");
        const host = String(data.hostname || data.fqdn || "");
        const port = String(data.port || "");
        codeElement.textContent = host && port ? `${host}:${port}` : (host || port);
        parent.append(codeElement);
    } else if (data.connect == "ssh") {
        let codeElement = document.createElement("code");
        const host = String(data.hostname || data.fqdn || "");
        const port = String(data.port || "");
        codeElement.textContent = host && port ? `${host}:${port}` : (host || port);
        parent.append(codeElement);
    } else {
        let link = document.createElement("a");
        link.href = "http://" + data.hostname + ":" + data.port;
        link.textContent = "http://" + data.hostname + ":" + data.port;
        link.target = "_blank";
        parent.append(link);
    }
}

function view_container_info(challenge_id) {
    resetAlert();
    var path = "/containers/api/view_info";

    let alert = document.getElementById("deployment-info");
    fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            "CSRF-Token": init.csrfNonce,
        },
        body: JSON.stringify({ chal_id: challenge_id }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status == "Pas d'instance lancé") {
                alert.append("Nenhuma instância foi iniciada.");
                toggleChallengeCreate();
            } else if (data.status == "already_running") {
                createChallengeLinkElement(data, alert);
                toggleChallengeUpdate();
            } else {
                resetAlert();
                alert.append(data.message);
                alert.classList.toggle("alert-danger");
                toggleChallengeUpdate();
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
        });
}

function container_request(challenge_id) {
    var path = "/containers/api/request";
    let alert = resetAlert();

    fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            "CSRF-Token": init.csrfNonce,
        },
        body: JSON.stringify({ chal_id: challenge_id }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error !== undefined) {
                alert.append(data.error);
                alert.classList.toggle("alert-danger");
                toggleChallengeCreate();
            } else if (data.message !== undefined) {
                alert.append(data.message);
                alert.classList.toggle("alert-danger");
                toggleChallengeCreate();
            } else {
                createChallengeLinkElement(data, alert);
                toggleChallengeUpdate();
                toggleChallengeCreate();
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
        });
}

function container_renew(challenge_id) {
    var path = "/containers/api/renew";
    let alert = resetAlert();

    fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            "CSRF-Token": init.csrfNonce,
        },
        body: JSON.stringify({ chal_id: challenge_id }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error !== undefined) {
                alert.append(data.error);
                alert.classList.toggle("alert-danger");
                toggleChallengeCreate();
            } else if (data.message !== undefined) {
                alert.append(data.message);
                alert.classList.toggle("alert-danger");
                toggleChallengeCreate();
            } else {
                createChallengeLinkElement(data, alert);
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
        });
}

function container_stop(challenge_id) {
    const path = "/containers/api/stop";
    const alert = resetAlert();

    fetch(path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            "CSRF-Token": init.csrfNonce,
        },
        body: JSON.stringify({ chal_id: challenge_id }),
    })
        .then((response) => response.json())
        .then((data) => {
            alert.classList.remove("d-none");
            alert.classList.add("alert");
            alert.classList.remove("alert-success", "alert-danger", "alert-warning");

            if (data.error !== undefined) {
                alert.classList.add("alert-danger");
                alert.textContent = "Erro: " + data.error;
            } else if (data.message !== undefined) {
                alert.classList.add("alert-danger");
                alert.textContent = "Erro: " + data.message;
            } else if (data.success !== undefined) {
                alert.classList.add("alert-success");
                alert.textContent = "Sua instância foi finalizada.";
                toggleChallengeUpdate();
            } else {
                alert.classList.add("alert-warning");
                alert.textContent = "Resposta inesperada do servidor.";
            }
            toggleChallengeCreate();
        })
        .catch((error) => {
            console.error("Fetch error:", error);
            alert.classList.remove("d-none");
            alert.classList.add("alert");
            alert.classList.remove("alert-success", "alert-danger", "alert-warning");
            alert.classList.add("alert-success");
            alert.textContent = "Sua instância foi finalizada.";
            toggleChallengeUpdate();
        });
}
