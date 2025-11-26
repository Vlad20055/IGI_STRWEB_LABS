class ContactsTable {
    constructor() {
        this.employees = [];
        this.filteredEmployees = [];
        this.currentPage = 1;
        this.pageSize = 3;
        this.sortField = null;
        this.sortDirection = 'asc';
        this.selectedEmployees = new Set();
        
        this.initializeElements();
        this.bindEvents();
        this.loadEmployees();
    }

    initializeElements() {
        // Основные элементы
        this.tableBody = document.getElementById('employees-tbody');
        this.searchInput = document.getElementById('search-input');
        this.searchBtn = document.getElementById('search-btn');
        this.addEmployeeBtn = document.getElementById('add-employee-btn');
        this.premiumBtn = document.getElementById('premium-btn');
        this.selectAllCheckbox = document.getElementById('select-all');
        
        // Пагинация
        this.prevPageBtn = document.getElementById('prev-page');
        this.nextPageBtn = document.getElementById('next-page');
        this.pageInfo = document.getElementById('page-info');
        this.currentRange = document.getElementById('current-range');
        this.totalEmployees = document.getElementById('total-employees');
        
        // Форма
        this.addForm = document.getElementById('add-employee-form');
        this.employeeForm = document.getElementById('employee-form');
        this.cancelAddBtn = document.getElementById('cancel-add-btn');
        this.submitEmployeeBtn = document.getElementById('submit-employee-btn');
        
        // Детали и премирование
        this.employeeDetails = document.getElementById('employee-details');
        this.premiumText = document.getElementById('premium-text');
        this.copyPremiumBtn = document.getElementById('copy-premium-btn');
        
        // Прелоадер
        this.preloader = document.getElementById('preloader');

        // Генератор числовых полей
        this.numberGenerator = new NumberInputsGenerator();
    }

    bindEvents() {
        // Поиск
        this.searchBtn.addEventListener('click', () => this.filterTable());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.filterTable();
        });

        // Пагинация
        this.prevPageBtn.addEventListener('click', () => this.previousPage());
        this.nextPageBtn.addEventListener('click', () => this.nextPage());

        // Форма
        this.addEmployeeBtn.addEventListener('click', () => this.showAddForm());
        this.cancelAddBtn.addEventListener('click', () => this.hideAddForm());
        this.employeeForm.addEventListener('input', () => this.validateForm());
        this.employeeForm.addEventListener('submit', (e) => this.addEmployee(e));

        // Выбор сотрудников
        this.selectAllCheckbox.addEventListener('change', (e) => this.toggleSelectAll(e));
        this.premiumBtn.addEventListener('click', () => this.generatePremiumText());

        // Копирование текста премирования
        this.copyPremiumBtn.addEventListener('click', () => this.copyPremiumText());

        // Сортировка по заголовкам
        document.querySelectorAll('[data-sort]').forEach(th => {
            th.addEventListener('click', () => this.sortTable(th.dataset.sort));
        });
    }

    loadEmployees() {
        this.showPreloader();
        
        // Собираем данные из таблицы (уже загруженной Django)
        const rows = this.tableBody.querySelectorAll('tr');
        this.employees = Array.from(rows).map(row => {
            const cells = row.querySelectorAll('td');
            const specializations = cells[3].textContent.split(', ').filter(s => s.trim());
            
            return {
                id: row.dataset.employeeId,
                full_name: cells[1].textContent,
                photo: cells[2].querySelector('img')?.src || '',
                specializations: specializations,
                phone: cells[4].textContent,
                email: cells[5].textContent,
                university_site: cells[6].querySelector('a')?.href || ''
            };
        });

        this.filteredEmployees = [...this.employees];
        this.hidePreloader();
        this.renderTable();
    }

    renderTable() {
        this.showPreloader();
        
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        const pageData = this.filteredEmployees.slice(startIndex, endIndex);

        this.tableBody.innerHTML = '';

        pageData.forEach(employee => {
            const row = document.createElement('tr');
            row.dataset.employeeId = employee.id;
            
            row.innerHTML = `
                <td>
                    <input type="checkbox" class="employee-checkbox" value="${employee.id}" 
                           ${this.selectedEmployees.has(employee.id) ? 'checked' : ''}>
                </td>
                <td>${this.escapeHtml(employee.full_name)}</td>
                <td>${employee.photo ? `<img src="${employee.photo}" alt="${employee.full_name}" class="employee-photo">` : '<div class="no-photo">🖼️</div>'}</td>
                <td>${employee.specializations.join(', ')}</td>
                <td>${this.escapeHtml(employee.phone)}</td>
                <td>${this.escapeHtml(employee.email)}</td>
                <td>${employee.university_site ? `<a href="${employee.university_site}" target="_blank" class="university-link">${this.truncateUrl(employee.university_site)}</a>` : '<span class="no-site">Не указан</span>'}</td>
            `;

            // Клик по строке для деталей
            row.addEventListener('click', (e) => {
                if (!e.target.matches('input[type="checkbox"]')) {
                    this.showEmployeeDetails(employee);
                }
            });

            // Чекбокс выбора
            const checkbox = row.querySelector('.employee-checkbox');
            checkbox.addEventListener('change', (e) => {
                e.stopPropagation();
                this.toggleEmployeeSelection(employee.id, checkbox.checked);
            });

            this.tableBody.appendChild(row);
        });

        this.updatePagination();
        this.hidePreloader();
    }

    // ПАГИНАЦИЯ
    updatePagination() {
        const totalPages = Math.ceil(this.filteredEmployees.length / this.pageSize);
        const startItem = ((this.currentPage - 1) * this.pageSize) + 1;
        const endItem = Math.min(this.currentPage * this.pageSize, this.filteredEmployees.length);

        this.currentRange.textContent = `${startItem}-${endItem}`;
        this.totalEmployees.textContent = this.filteredEmployees.length;
        this.pageInfo.textContent = `Страница ${this.currentPage} из ${totalPages}`;

        this.prevPageBtn.disabled = this.currentPage === 1;
        this.nextPageBtn.disabled = this.currentPage === totalPages || totalPages === 0;
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.renderTable();
        }
    }

    nextPage() {
        const totalPages = Math.ceil(this.filteredEmployees.length / this.pageSize);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            this.renderTable();
        }
    }

    // СОРТИРОВКА
    sortTable(field) {
        if (this.sortField === field) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortField = field;
            this.sortDirection = 'asc';
        }

        this.filteredEmployees.sort((a, b) => {
            let aValue = a[field];
            let bValue = b[field];

            if (Array.isArray(aValue)) {
                aValue = aValue.join(', ');
                bValue = bValue.join(', ');
            }

            if (aValue < bValue) return this.sortDirection === 'asc' ? -1 : 1;
            if (aValue > bValue) return this.sortDirection === 'asc' ? 1 : -1;
            return 0;
        });

        this.updateSortIndicators();
        this.currentPage = 1;
        this.renderTable();
    }

    updateSortIndicators() {
        document.querySelectorAll('[data-sort]').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
            if (th.dataset.sort === this.sortField) {
                th.classList.add(this.sortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
            }
        });
    }

    // ФИЛЬТРАЦИЯ
    filterTable() {
        const searchText = this.searchInput.value.toLowerCase().trim();
        
        if (!searchText) {
            this.filteredEmployees = [...this.employees];
        } else {
            this.filteredEmployees = this.employees.filter(employee => 
                employee.full_name.toLowerCase().includes(searchText) ||
                employee.specializations.some(spec => spec.toLowerCase().includes(searchText)) ||
                employee.phone.toLowerCase().includes(searchText) ||
                employee.email.toLowerCase().includes(searchText) ||
                employee.university_site.toLowerCase().includes(searchText)
            );
        }

        this.currentPage = 1;
        this.renderTable();
    }

    // ВЫБОР СОТРУДНИКОВ
    toggleSelectAll(event) {
        const isChecked = event.target.checked;
        const currentPageData = this.getCurrentPageData();
        
        currentPageData.forEach(employee => {
            if (isChecked) {
                this.selectedEmployees.add(employee.id);
            } else {
                this.selectedEmployees.delete(employee.id);
            }
        });

        this.renderTable();
        this.updatePremiumButton();
    }

    toggleEmployeeSelection(employeeId, isSelected) {
        if (isSelected) {
            this.selectedEmployees.add(employeeId);
        } else {
            this.selectedEmployees.delete(employeeId);
            this.selectAllCheckbox.checked = false;
        }
        
        this.updatePremiumButton();
    }

    updatePremiumButton() {
        this.premiumBtn.disabled = this.selectedEmployees.size === 0;
    }

    // ДЕТАЛИ СОТРУДНИКА
    showEmployeeDetails(employee) {
        document.getElementById('detail-full-name').textContent = employee.full_name;
        document.getElementById('detail-specialization').textContent = employee.specializations.join(', ');
        document.getElementById('detail-phone').textContent = employee.phone;
        document.getElementById('detail-email').textContent = employee.email;
        document.getElementById('detail-university-site').textContent = employee.university_site || 'Не указан';
        
        this.employeeDetails.style.display = 'block';
    }

    // ПРЕМИРОВАНИЕ
    generatePremiumText() {
        const selectedNames = Array.from(this.selectedEmployees)
            .map(id => {
                const employee = this.employees.find(emp => emp.id === id);
                return employee ? employee.full_name.split(' ')[0] : ''; // Берем только фамилию
            })
            .filter(name => name);

        if (selectedNames.length === 0) return;

        const premiumContent = document.getElementById('premium-content');
        premiumContent.innerHTML = `
            <p><strong>ПРИКАЗ О ПРЕМИРОВАНИИ</strong></p>
            <p>На основании результатов работы премировать следующих сотрудников:</p>
            <ul>
                ${selectedNames.map(name => `<li>${name}</li>`).join('')}
            </ul>
            <p>Размер премии: 15% от оклада.</p>
            <p>Дата: ${new Date().toLocaleDateString('ru-RU')}</p>
        `;

        this.premiumText.style.display = 'block';
    }

    copyPremiumText() {
        const text = document.getElementById('premium-content').innerText;
        navigator.clipboard.writeText(text).then(() => {
            alert('Текст скопирован в буфер обмена!');
        });
    }

    // ФОРМА ДОБАВЛЕНИЯ
    showAddForm() {
        this.addForm.style.display = 'block';
    }

    hideAddForm() {
        this.addForm.style.display = 'none';
        this.employeeForm.reset();
        this.clearValidation();
    }

    validateForm() {
        const formData = new FormData(this.employeeForm);
        const phone = formData.get('phone') || '';
        const url = formData.get('university_site') || '';
        
        const isPhoneValid = this.validatePhone(phone);
        const isUrlValid = !url || this.validateUrl(url);
        const allFieldsFilled = Array.from(formData.entries()).every(([key, value]) => {
            if (key === 'university_site') return true; // Необязательное поле
            return value.trim() !== '';
        });

        this.updateValidation('phone', isPhoneValid, 'Формат: +375 (XX) XXX-XX-XX или 8 (XX) XXX-XX-XX');
        this.updateValidation('url', isUrlValid, 'Формат: https://example.com/page.html или .php');

        this.submitEmployeeBtn.disabled = !(allFieldsFilled && isPhoneValid && isUrlValid);
    }

    validatePhone(phone) {
        const phoneRegex = /^(?:\+375|8)\s?\(?\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
        return phoneRegex.test(phone.trim());
    }

    validateUrl(url) {
        if (!url) return true;
        const urlRegex = /^https?:\/\/.+(\.php|\.html)$/;
        return urlRegex.test(url.trim());
    }

    updateValidation(field, isValid, message) {
        const element = field === 'phone' ? document.getElementById('phone') : document.getElementById('university-site');
        const validationElement = field === 'phone' ? document.getElementById('phone-validation') : document.getElementById('url-validation');
        
        element.classList.toggle('invalid', !isValid);
        element.classList.toggle('valid', isValid && element.value.trim() !== '');
        
        validationElement.textContent = !isValid && element.value.trim() !== '' ? message : '';
        validationElement.style.color = '#dc3545';
    }

    clearValidation() {
        document.querySelectorAll('.validation-message').forEach(el => el.textContent = '');
        document.querySelectorAll('input').forEach(input => {
            input.classList.remove('invalid', 'valid');
        });
    }

    addEmployee(event) {
        event.preventDefault();
        
        const formData = new FormData(this.employeeForm);
        const newEmployee = {
            id: 'new-' + Date.now(),
            full_name: formData.get('full_name'),
            photo: formData.get('photo') || '',
            specializations: Array.from(formData.getAll('specialization')),
            phone: formData.get('phone'),
            email: formData.get('email'),
            university_site: formData.get('university_site') || ''
        };

        this.employees.unshift(newEmployee);
        this.filteredEmployees.unshift(newEmployee);
        
        this.hideAddForm();
        this.currentPage = 1;
        this.renderTable();
    }

    // ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    getCurrentPageData() {
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        return this.filteredEmployees.slice(startIndex, endIndex);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    truncateUrl(url, maxLength = 30) {
        return url.length > maxLength ? url.substring(0, maxLength) + '...' : url;
    }

    showPreloader() {
        this.preloader.style.display = 'flex';
    }

    hidePreloader() {
        setTimeout(() => {
            this.preloader.style.display = 'none';
        }, 300);
    }
}

class NumberInputsGenerator {
    constructor() {
        this.generatedFields = [];
        this.initializeElements();
        this.bindEvents();
        this.loadFromStorage();
    }

    initializeElements() {
        this.enableGenerator = document.getElementById('enable-generator');
        this.generatorForm = document.getElementById('generator-form');
        this.numberInputForm = document.getElementById('number-input-form');
        this.generatedFieldsContainer = document.getElementById('generated-fields-container');
    }

    bindEvents() {
        // Переключение видимости формы
        this.enableGenerator.addEventListener('change', (e) => {
            this.generatorForm.style.display = e.target.checked ? 'block' : 'none';
        });

        // Обработка формы
        this.numberInputForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateField();
        });
    }

    generateField() {
        const formData = new FormData(this.numberInputForm);
        const attributes = {
            name: formData.get('name') || 'numberField',
            min: formData.get('min'),
            max: formData.get('max'),
            step: formData.get('step') || '1',
            value: formData.get('value'),
            placeholder: formData.get('placeholder'),
            readonly: formData.get('readonly') === 'on'
        };

        // Создаем поле
        const fieldId = 'field-' + Date.now();
        const fieldWrapper = document.createElement('div');
        fieldWrapper.className = 'generated-field';
        fieldWrapper.dataset.fieldId = fieldId;

        const input = document.createElement('input');
        input.type = 'number';
        input.id = fieldId;

        // Устанавливаем атрибуты
        Object.entries(attributes).forEach(([key, value]) => {
            if (value !== '' && value !== null && value !== false) {
                if (key === 'readonly' && value) {
                    input.setAttribute('readonly', 'readonly');
                } else if (key !== 'readonly') {
                    input.setAttribute(key, value);
                }
            }
        });

        // Создаем информацию о поле
        const fieldInfo = document.createElement('span');
        fieldInfo.className = 'field-info';
        fieldInfo.textContent = this.getFieldInfo(attributes);

        // Кнопка удаления
        const deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.className = 'delete-field';
        deleteBtn.textContent = 'Удалить';
        deleteBtn.addEventListener('click', () => {
            this.removeField(fieldId);
        });

        fieldWrapper.appendChild(input);
        fieldWrapper.appendChild(fieldInfo);
        fieldWrapper.appendChild(deleteBtn);
        this.generatedFieldsContainer.appendChild(fieldWrapper);

        // Сохраняем в хранилище
        this.saveToStorage(fieldId, attributes);
    }

    getFieldInfo(attributes) {
        const info = [];
        // Добавляем имя в информацию
        if (attributes.name && attributes.name !== 'numberField') {
            info.push(`name: ${attributes.name}`);
        }
        if (attributes.min) info.push(`min: ${attributes.min}`);
        if (attributes.max) info.push(`max: ${attributes.max}`);
        if (attributes.step && attributes.step !== '1') info.push(`step: ${attributes.step}`);
        if (attributes.readonly) info.push('readonly');
        
        return info.length > 0 ? `(${info.join(', ')})` : '';
    }

    removeField(fieldId) {
        const fieldWrapper = document.querySelector(`[data-field-id="${fieldId}"]`);
        if (fieldWrapper) {
            fieldWrapper.remove();
        }
        this.removeFromStorage(fieldId);
    }

    saveToStorage(fieldId, attributes) {
        const savedFields = JSON.parse(localStorage.getItem('generatedNumberFields') || '{}');
        savedFields[fieldId] = attributes;
        localStorage.setItem('generatedNumberFields', JSON.stringify(savedFields));
    }

    removeFromStorage(fieldId) {
        const savedFields = JSON.parse(localStorage.getItem('generatedNumberFields') || '{}');
        delete savedFields[fieldId];
        localStorage.setItem('generatedNumberFields', JSON.stringify(savedFields));
    }

    loadFromStorage() {
        const savedFields = JSON.parse(localStorage.getItem('generatedNumberFields') || '{}');
        
        Object.entries(savedFields).forEach(([fieldId, attributes]) => {
            // Воссоздаем поле из сохраненных данных
            const fieldWrapper = document.createElement('div');
            fieldWrapper.className = 'generated-field';
            fieldWrapper.dataset.fieldId = fieldId;

            const input = document.createElement('input');
            input.type = 'number';
            input.id = fieldId;

            // Устанавливаем атрибуты
            Object.entries(attributes).forEach(([key, value]) => {
                if (value !== '' && value !== null && value !== false) {
                    if (key === 'readonly' && value) {
                        input.setAttribute('readonly', 'readonly');
                    } else if (key !== 'readonly') {
                        input.setAttribute(key, value);
                    }
                }
            });

            const fieldInfo = document.createElement('span');
            fieldInfo.className = 'field-info';
            fieldInfo.textContent = this.getFieldInfo(attributes);

            const deleteBtn = document.createElement('button');
            deleteBtn.type = 'button';
            deleteBtn.className = 'delete-field';
            deleteBtn.textContent = 'Удалить';
            deleteBtn.addEventListener('click', () => {
                this.removeField(fieldId);
            });

            fieldWrapper.appendChild(input);
            fieldWrapper.appendChild(fieldInfo);
            fieldWrapper.appendChild(deleteBtn);
            this.generatedFieldsContainer.appendChild(fieldWrapper);
        });
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    new ContactsTable();
});
