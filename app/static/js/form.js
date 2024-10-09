document.getElementById('appointmentForm').addEventListener('submit', async function (ev) {
    ev.preventDefault()
    const name = document.getElementById('name').value.trim();
    const service = document.getElementById('service').value.trim();
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const userId = document.getElementById('user_id').value;
    const stylist = document.getElementById('stylist').value.trim();
    const gender = document.getElementById('gender').value.trim();
    const phone = document.getElementById('phone').value;

    if (name.length < 2 || name.length > 50) {
        alert("Имя должно быть от 2 до 50 символов.");
        return;
    }

    if (gender.length < 2 || gender.length > 50) {
        alert("Пол должен быть от 2 до 50 символов.");
        return;
    }

    if (service.length < 2 || service.length > 50) {
        alert("Услуга должна быть от 2 до 50 символов.");
        return;
    }

    if (stylist.length < 2 || stylist.length > 50) {
        alert("Имя мастера должно быть от 2 до 50 символов.");
        return;
    }

    const appointmentData = {
        name: name,
        gender: gender,
        service: service,
        appointment_date: date,
        appointment_time: time,
        stylist: stylist,
        user_id: userId,
        phone: phone
    };

    const jsonData = JSON.stringify(appointmentData);

    let popupMessage;

    try {
        const response = await fetch('/api/appointment', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        });

        const result = await response.json();
        if (result.message == "success!") {
            popupMessage = `${name}, вы записаны на ${service.split('_')[1].toLowerCase()} ${date} в ${time}.`;
        } else {
            console.error('error sending POST request:', result)
            popupMessage = `${name}, к сожалению при попытке записать вас произошла ошибка.`+
                                    `Попробуйте еще раз или позвоните нам по номеру <номер>.`;
        }

    } catch (error) {
        console.error('error sending POST request:', error)
        popupMessage = `${name}, к сожалению при попытке записать вас произошла ошибка.`+
                                    `Попробуйте еще раз или позвоните нам по номеру <номер>.`;
    }
    document.getElementById('popupMessage').textContent = popupMessage;
    document.getElementById('popup').style.display = 'flex';


})


document.getElementById('closePopup').addEventListener('click', async function () {

        setTimeout(() => {
            document.getElementById('popup').style.display = 'none';
            window.Telegram.WebApp.close()
        }, 100)

})


function animateElements() {
    const elements = document.querySelectorAll('h1, .form-group, .btn');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 100 * index);
    });
}

var styleSheet = document.styleSheets[0];
styleSheet.insertRule(`
    h1, .form-group, .btn {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.5s ease, transform 0.5s ease;
    }
`, styleSheet.cssRules.length);

window.addEventListener('load', function () {
    document.body.style.opacity = '1';
    animateElements();
});


styleSheet.insertRule(`
    body {
        opacity: 0;
        transition: opacity 0.5s ease;
    }
`, styleSheet.cssRules.length);

document.addEventListener('DOMContentLoaded', (event) => {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').setAttribute('min', today)
})


let phoneInput = document.getElementById('phone');

IMask(phoneInput, {
    mask: "+{7}(000)000-00-00",
});
