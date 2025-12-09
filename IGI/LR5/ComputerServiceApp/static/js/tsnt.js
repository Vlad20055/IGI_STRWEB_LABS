
// ВАРИАНТ 1: Прототипное наследование (функциональный стиль)


// ВАРИАНТ 2 // Наследование классов

class Person {
    constructor(surname) {
        this._surname = surname;
    }

    set surname(value) {
        this._surname = value;
    }

    get surname() {
        return this._surname;
    }

    getInfo() {
        return this._surname;
    }
}

class TsntHolder extends Person {
    constructor(surname, tsntNumber, square) {
        super(surname);
        this._tsntNumber = tsntNumber;
        this._square = square;
    }

    set tsntNumber(value) {
        this._tsntNumber = value;
    }

    set square(value) {
        this._square = value;
    }

    get tsntNumber() {
        return this._tsntNumber;
    }

    get square() {
        return this._square;
    }

    getInfo() {
        return `${this.surname} - участок ${this.tsntNumber}, ${this.square} кв.м.`;
    }
}


class TsntApp {
    constructor() {
        this.holders = [];
        this.bindEvents();
    }

    bindEvents() {
        document.querySelector('.form button').addEventListener('click', () => this.addHolder());
        document.querySelector('.controls button:nth-child(1)').addEventListener('click', () => this.showAll());
        document.querySelector('.controls button:nth-child(2)').addEventListener('click', () => this.findMultiple());
        document.querySelector('.controls button:nth-child(3)').addEventListener('click', () => this.clearAll());
    }

    addHolder() {
        const surname = document.getElementById('surname').value;
        const tsntNumber = parseInt(document.getElementById('tsntNumber').value);
        const square = parseFloat(document.getElementById('square').value);

        if (surname && tsntNumber && square) {
            const holder = new TsntHolder(surname, tsntNumber, square);
            this.holders.push(holder);
            
            document.getElementById('surname').value = '';
            document.getElementById('tsntNumber').value = '';
            document.getElementById('square').value = '';
            
            this.showMessage('Владелец добавлен!');
        } else {
            this.showMessage('Заполните все поля!');
        }
    }

    showAll() {
        const output = document.getElementById('output');
        
        if (this.holders.length === 0) {
            output.innerHTML = 'Нет данных';
            return;
        }

        let html = '<h3>Все владельцы:</h3>';
        this.holders.forEach(holder => {
            html += `<p>${holder.getInfo()}</p>`;
        });
        
        output.innerHTML = html;
    }

    findMultiple() {
        const output = document.getElementById('output');
        
        const groups = {};
        this.holders.forEach(holder => {
            if (!groups[holder.surname]) {
                groups[holder.surname] = [];
            }
            groups[holder.surname].push(holder);
        });

        const result = [];
        for (const surname in groups) {
            if (groups[surname].length > 1) {
                const plots = groups[surname].map(h => h.tsntNumber);
                const totalSquare = groups[surname].reduce((sum, h) => sum + h.square, 0);
                result.push({
                    surname: surname,
                    plots: plots,
                    totalSquare: totalSquare
                });
            }
        }

        if (result.length === 0) {
            output.innerHTML = 'Владельцев с несколькими участками не найдено';
            return;
        }

        let html = '<h3>Владельцы с несколькими участками:</h3>';
        result.forEach(owner => {
            html += `
                <div style="margin: 10px 0; padding: 10px; border-left: 3px solid #007bff; background: white;">
                    <strong>${owner.surname}</strong><br>
                    Участки: ${owner.plots.join(', ')}<br>
                    Общая площадь: ${owner.totalSquare} кв.м.
                </div>
            `;
        });
        
        output.innerHTML = html;
    }

    clearAll() {
        this.holders = [];
        document.getElementById('output').innerHTML = 'Данные очищены';
    }

    showMessage(msg) {
        const output = document.getElementById('output');
        output.innerHTML = msg;
        setTimeout(() => {
            if (output.innerHTML === msg) {
                output.innerHTML = '';
            }
        }, 2000);
    }
}

// Инициализация приложения после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    new TsntApp();
});




