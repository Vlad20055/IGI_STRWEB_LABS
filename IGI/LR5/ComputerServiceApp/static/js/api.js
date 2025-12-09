// Геолокация
document.getElementById('locationBtn').addEventListener('click', () => {
    const output = document.getElementById('locationOutput');
    output.textContent = 'Определение местоположения...';
    
    if (!navigator.geolocation) {
        output.textContent = 'Геолокация не поддерживается вашим браузером';
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            output.innerHTML = `
                ✅ Местоположение получено:<br>
                Широта: ${lat.toFixed(6)}<br>
                Долгота: ${lon.toFixed(6)}<br>
                <a href="https://www.openstreetmap.org/#map=15/${lat}/${lon}" target="_blank">
                    Посмотреть на карте
                </a>
            `;
        },
        (error) => {
            let message = 'Ошибка определения местоположения: ';
            switch(error.code) {
                case 1: message += 'Доступ запрещен'; break;
                case 2: message += 'Позиция недоступна'; break;
                case 3: message += 'Таймаут'; break;
                default: message += 'Неизвестная ошибка';
            }
            output.textContent = message;
        }
    );
});

// Синтез речи
document.getElementById('speakBtn').addEventListener('click', () => {
    const textInput = document.getElementById('textInput');
    const text = textInput.value.trim();
    
    if (!text) {
        alert('Введите текст для озвучивания');
        textInput.focus();
        return;
    }
    
    if (!window.speechSynthesis) {
        alert('Синтез речи не поддерживается вашим браузером');
        return;
    }
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ru-RU';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    
    speechSynthesis.speak(utterance);
});