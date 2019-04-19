function initCountdown(endDate) {
    countdownTick(endDate);
    setInterval(function() {
        countdownTick(endDate)
    }, 1000);
}

function countdownTick(endDate) {
    var timeDiff = Date.parse(endDate) - Date.now();

    if (timeDiff < 0) {
        timeDiff = Math.abs(timeDiff);
        document.getElementById('cd-start').innerText = 'was';
        document.getElementById('cd-end').innerText = 'ago';
    }

    var days = Math.floor(timeDiff / (24*3600*1000));
    timeDiff -= days * 24 * 3600 * 1000;
    var hours = Math.floor(timeDiff / (3600*1000));
    timeDiff -= hours * 3600 * 1000;
    var minutes = Math.floor(timeDiff / (60*1000));
    timeDiff -= minutes * 60 * 1000;
    var seconds = Math.floor(timeDiff / 1000);

    document.getElementById('cd-days').innerText = days;
    document.getElementById('cd-hours').innerText = hours;
    document.getElementById('cd-minutes').innerText = minutes;
    document.getElementById('cd-seconds').innerText = seconds;
}
