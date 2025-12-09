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


// ВАРИАНТ 1: Прототипное наследование (функциональный стиль)

// Конструктор Person
function Person(surname) {
    this._surname = surname;
}

// Методы для Person
Person.prototype.setSurname = function(value) {
    this._surname = value;
};

Person.prototype.getSurname = function() {
    return this._surname;
};

Person.prototype.getInfo = function() {
    return this._surname;
};

// Конструктор TsntHolder с наследованием от Person
function TsntHolder(surname, tsntNumber, square) {
    Person.call(this, surname); // вызов родительского конструктора
    this._tsntNumber = tsntNumber;
    this._square = square;
}

// Наследование прототипа
TsntHolder.prototype = Object.create(Person.prototype);
TsntHolder.prototype.constructor = TsntHolder;

// Методы для TsntHolder
TsntHolder.prototype.setTsntNumber = function(value) {
    this._tsntNumber = value;
};

TsntHolder.prototype.setSquare = function(value) {
    this._square = value;
};

TsntHolder.prototype.getTsntNumber = function() {
    return this._tsntNumber;
};

TsntHolder.prototype.getSquare = function() {
    return this._square;
};

TsntHolder.prototype.getInfo = function() {
    return this.getSurname() + " - участок " + this._tsntNumber + ", " + this._square + " кв.м.";
};

// Геттеры/сеттеры для совместимости с классовой версией
Object.defineProperty(TsntHolder.prototype, 'surname', {
    get: function() { return this.getSurname(); },
    set: function(value) { this.setSurname(value); }
});

Object.defineProperty(TsntHolder.prototype, 'tsntNumber', {
    get: function() { return this.getTsntNumber(); },
    set: function(value) { this.setTsntNumber(value); }
});

Object.defineProperty(TsntHolder.prototype, 'square', {
    get: function() { return this.getSquare(); },
    set: function(value) { this.setSquare(value); }
});


// ВАРИАНТ 2 //
/*
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
*/