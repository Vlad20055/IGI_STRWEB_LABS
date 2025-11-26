class Slider {
    constructor(container) {
        this.container = container;
        this.slides = container.querySelectorAll('.slide');
        this.prevBtn = container.querySelector('.slider-nav.prev');
        this.nextBtn = container.querySelector('.slider-nav.next');
        this.paginationDots = container.querySelectorAll('.pagination-dot');
        this.counterCurrent = container.querySelector('.slide-counter .current');
        this.counterTotal = container.querySelector('.slide-counter .total');
        
        this.settings = {
            delay: parseInt(container.dataset.delay) * 1000 || 5000,
            loop: container.dataset.loop === 'true',
            navs: container.dataset.navs === 'true',
            pags: container.dataset.pags === 'true',
            auto: container.dataset.auto === 'true',
            stopHover: container.dataset.stopHover === 'true'
        };
        
        this.currentIndex = 0;
        this.totalSlides = this.slides.length;
        this.autoPlayInterval = null;
        this.isPaused = false;
        
        this.init();
    }
    
    init() {
        this.counterTotal.textContent = this.totalSlides;
        
        this.bindEvents();
        
        if (this.settings.auto) {
            this.startAutoPlay();
        }
        
        this.showSlide(this.currentIndex);
    }
    
    bindEvents() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
        
        if (this.paginationDots.length > 0) {
            this.paginationDots.forEach((dot, index) => {
                dot.addEventListener('click', () => this.goToSlide(index));
            });
        }
        
        if (this.settings.auto && this.settings.stopHover) {
            this.container.addEventListener('mouseenter', () => this.pause());
            this.container.addEventListener('mouseleave', () => this.resume());
        }
    }
    
    showSlide(index) {
        this.slides.forEach(slide => slide.classList.remove('active'));
        if (this.paginationDots.length > 0) {
            this.paginationDots.forEach(dot => dot.classList.remove('active'));
            this.paginationDots[index].classList.add('active');
        }

        this.slides[index].classList.add('active');
        this.counterCurrent.textContent = index + 1;
        this.currentIndex = index;
    }
    
    next() {
        let nextIndex = this.currentIndex + 1;
        
        if (nextIndex >= this.totalSlides) {
            if (this.settings.loop) {
                nextIndex = 0;
            } else {
                nextIndex = this.totalSlides - 1;
            }
        }
        
        this.showSlide(nextIndex);
        
        if (this.settings.auto) {
            this.resetAutoPlay();
        }
    }
    
    prev() {
        let prevIndex = this.currentIndex - 1;
        
        if (prevIndex < 0) {
            if (this.settings.loop) {
                prevIndex = this.totalSlides - 1;
            } else {
                prevIndex = 0;
            }
        }
        
        this.showSlide(prevIndex);
        
        if (this.settings.auto) {
            this.resetAutoPlay();
        }
    }
    
    goToSlide(index) {
        if (index >= 0 && index < this.totalSlides) {
            this.showSlide(index);
            
            if (this.settings.auto) {
                this.resetAutoPlay();
            }
        }
    }
    
    startAutoPlay() {
        if (this.settings.auto && !this.isPaused) {
            this.autoPlayInterval = setInterval(() => {
                this.next();
            }, this.settings.delay);
        }
    }
    
    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
    
    resetAutoPlay() {
        this.stopAutoPlay();
        this.startAutoPlay();
    }
    
    pause() {
        this.isPaused = true;
        this.stopAutoPlay();
    }
    
    resume() {
        this.isPaused = false;
        this.startAutoPlay();
    }
}

class CatalogPagination {
    constructor() {
        this.perPage = 3;
        this.services = {
            items: [],
            currentPage: 1,
            totalPages: 1,
            container: document.getElementById('services-container'),
            prevBtn: document.getElementById('services-prev'),
            nextBtn: document.getElementById('services-next'),
            info: document.getElementById('services-info')
        };
        
        this.spareparts = {
            items: [],
            currentPage: 1,
            totalPages: 1,
            container: document.getElementById('spareparts-container'),
            prevBtn: document.getElementById('spareparts-prev'),
            nextBtn: document.getElementById('spareparts-next'),
            info: document.getElementById('spareparts-info')
        };
        
        this.init();
    }
    
    init() {
        // Собираем все элементы
        this.services.items = Array.from(this.services.container.querySelectorAll('.service-item'));
        this.spareparts.items = Array.from(this.spareparts.container.querySelectorAll('.sparepart-item'));
        
        // Настройка пагинации
        this.setupPagination(this.services);
        this.setupPagination(this.spareparts);
        
        // Обработчики событий
        this.bindEvents();
        
        // Первоначальный рендер
        this.render(this.services);
        this.render(this.spareparts);
    }
    
    setupPagination(section) {
        section.totalPages = Math.ceil(section.items.length / this.perPage);
        this.updatePaginationInfo(section);
    }
    
    bindEvents() {
        // Кнопки пагинации услуг
        this.services.prevBtn.addEventListener('click', () => this.prevPage(this.services));
        this.services.nextBtn.addEventListener('click', () => this.nextPage(this.services));
        
        // Кнопки пагинации запчастей
        this.spareparts.prevBtn.addEventListener('click', () => this.prevPage(this.spareparts));
        this.spareparts.nextBtn.addEventListener('click', () => this.nextPage(this.spareparts));
        
        // Выбор количества элементов
        document.getElementById('per-page-select').addEventListener('change', (e) => {
            this.perPage = parseInt(e.target.value);
            this.services.currentPage = 1;
            this.spareparts.currentPage = 1;
            this.setupPagination(this.services);
            this.setupPagination(this.spareparts);
            this.render(this.services);
            this.render(this.spareparts);
        });
    }
    
    prevPage(section) {
        if (section.currentPage > 1) {
            section.currentPage--;
            this.render(section);
        }
    }
    
    nextPage(section) {
        if (section.currentPage < section.totalPages) {
            section.currentPage++;
            this.render(section);
        }
    }
    
    render(section) {
        // Скрываем все элементы
        section.items.forEach(item => item.style.display = 'none');
        
        // Показываем элементы текущей страницы
        const startIndex = (section.currentPage - 1) * this.perPage;
        const endIndex = startIndex + this.perPage;
        
        section.items.slice(startIndex, endIndex).forEach(item => {
            item.style.display = 'block';
        });
        
        // Обновляем информацию и кнопки
        this.updatePaginationInfo(section);
        this.updatePaginationButtons(section);
    }
    
    updatePaginationInfo(section) {
        section.totalPages = Math.ceil(section.items.length / this.perPage);
        section.info.textContent = `Страница ${section.currentPage} из ${section.totalPages}`;
    }
    
    updatePaginationButtons(section) {
        section.prevBtn.disabled = section.currentPage === 1;
        section.nextBtn.disabled = section.currentPage === section.totalPages || section.totalPages === 0;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    new CatalogPagination();
});

document.addEventListener('DOMContentLoaded', function() {
    const sliderContainer = document.querySelector('.slider');
    if (sliderContainer) {
        new Slider(sliderContainer);
    }
});