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

document.addEventListener('DOMContentLoaded', function() {
    const sliderContainer = document.querySelector('.slider');
    if (sliderContainer) {
        new Slider(sliderContainer);
    }
});