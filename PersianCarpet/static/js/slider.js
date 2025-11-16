// slider.js
class Slider {
  constructor() {
    this.slider = document.querySelector(".slider");
    this.slides = document.querySelectorAll(".slide");
    this.prevBtn = document.querySelector(".prev-btn");
    this.nextBtn = document.querySelector(".next-btn");
    this.dots = document.querySelectorAll(".dot");
    this.currentIndex = 0;
    this.totalSlides = this.slides.length;
    this.autoPlayInterval = null;
    this.autoPlayDelay = 5000;

    this.touchStartX = 0;
    this.touchEndX = 0;
    this.minSwipeDistance = 50;

    this.init();
  }

  init() {
    this.prevBtn.addEventListener("click", () => this.prevSlide());
    this.nextBtn.addEventListener("click", () => this.nextSlide());

    this.dots.forEach((dot) => {
      dot.addEventListener("click", (e) => {
        const index = parseInt(e.currentTarget.getAttribute("data-index"));
        this.goToSlide(index);
      });
    });

    document.addEventListener("keydown", (e) => this.handleKeydown(e));

    this.addSwipeListeners();

    this.startAutoPlay();

    this.slider.addEventListener("mouseenter", () => this.stopAutoPlay());
    this.slider.addEventListener("mouseleave", () => this.startAutoPlay());

    this.addFocusListeners();

    console.log("اسلایدر راه‌اندازی شد. تعداد اسلایدها:", this.totalSlides);
  }

  addSwipeListeners() {
    this.slider.addEventListener(
      "touchstart",
      (e) => this.handleTouchStart(e),
      { passive: true }
    );
    this.slider.addEventListener("touchmove", (e) => this.handleTouchMove(e), {
      passive: true,
    });
    this.slider.addEventListener("touchend", (e) => this.handleTouchEnd(e), {
      passive: true,
    });

    this.slider.addEventListener("mousedown", (e) => this.handleMouseDown(e));
    this.slider.addEventListener("mouseup", (e) => this.handleMouseUp(e));
  }

  handleTouchStart(e) {
    this.touchStartX = e.changedTouches[0].screenX;
    this.stopAutoPlay();
  }

  handleTouchMove(e) {
    if (Math.abs(e.changedTouches[0].screenX - this.touchStartX) > 10) {
      e.preventDefault();
    }
  }

  handleTouchEnd(e) {
    this.touchEndX = e.changedTouches[0].screenX;
    this.handleSwipe();
    this.startAutoPlay();
  }

  handleMouseDown(e) {
    this.touchStartX = e.clientX;
    this.stopAutoPlay();
  }

  handleMouseUp(e) {
    this.touchEndX = e.clientX;
    this.handleSwipe();
    this.startAutoPlay();
  }

  handleSwipe() {
    const swipeDistance = this.touchEndX - this.touchStartX;

    if (Math.abs(swipeDistance) < this.minSwipeDistance) {
      return;
    }

    if (swipeDistance > 0) {
      this.prevSlide();
    } else {
      this.nextSlide();
    }
  }

  showSlide(index) {
    this.slides.forEach((slide) => slide.classList.remove("active"));
    this.dots.forEach((dot) => dot.classList.remove("active"));

    this.slides[index].classList.add("active");
    this.dots[index].classList.add("active");

    this.currentIndex = index;

    this.updateAriaLive();
  }

  nextSlide() {
    let nextIndex = this.currentIndex + 1;
    if (nextIndex >= this.totalSlides) {
      nextIndex = 0;
    }
    this.showSlide(nextIndex);
    this.restartAutoPlay();
  }

  prevSlide() {
    let prevIndex = this.currentIndex - 1;
    if (prevIndex < 0) {
      prevIndex = this.totalSlides - 1;
    }
    this.showSlide(prevIndex);
    this.restartAutoPlay();
  }

  goToSlide(index) {
    if (index >= 0 && index < this.totalSlides) {
      this.showSlide(index);
      this.restartAutoPlay();
    }
  }

  startAutoPlay() {
    if (this.autoPlayInterval) {
      this.stopAutoPlay();
    }

    this.autoPlayInterval = setInterval(() => {
      this.nextSlide();
    }, this.autoPlayDelay);
  }

  stopAutoPlay() {
    if (this.autoPlayInterval) {
      clearInterval(this.autoPlayInterval);
      this.autoPlayInterval = null;
    }
  }

  restartAutoPlay() {
    this.stopAutoPlay();
    this.startAutoPlay();
  }

  handleKeydown(e) {
    if (e.key === "ArrowRight") {
      this.nextSlide();
    } else if (e.key === "ArrowLeft") {
      this.prevSlide();
    } else if (e.key >= "1" && e.key <= "3") {
      const index = parseInt(e.key) - 1;
      if (index < this.totalSlides) {
        this.goToSlide(index);
      }
    }
  }

  addFocusListeners() {
    const focusableElements = [this.prevBtn, this.nextBtn, ...this.dots];

    focusableElements.forEach((element) => {
      element.addEventListener("focus", () => this.stopAutoPlay());
      element.addEventListener("blur", () => this.startAutoPlay());
    });
  }

  updateAriaLive() {
    const activeSlide = this.slides[this.currentIndex];
    const imageAlt = activeSlide.querySelector("img").getAttribute("alt");
    console.log(`اسلاید فعلی: ${this.currentIndex + 1} - ${imageAlt}`);
  }

  addSlide(imageSrc, altText) {
    const newSlide = document.createElement("div");
    newSlide.className = "slide";

    const img = document.createElement("img");
    img.src = imageSrc;
    img.alt = altText;
    img.className = "slide-image";

    newSlide.appendChild(img);
    this.slider.appendChild(newSlide);

    this.updateDots();

    this.slides = document.querySelectorAll(".slide");
    this.totalSlides = this.slides.length;
  }

  updateDots() {
    const dotsContainer = document.querySelector(".slider-dots");
    dotsContainer.innerHTML = "";

    for (let i = 0; i < this.totalSlides; i++) {
      const dot = document.createElement("button");
      dot.className = `dot ${i === this.currentIndex ? "active" : ""}`;
      dot.setAttribute("data-index", i);
      dot.setAttribute("aria-label", `رفتن به اسلاید ${i + 1}`);

      dot.addEventListener("click", (e) => {
        const index = parseInt(e.currentTarget.getAttribute("data-index"));
        this.goToSlide(index);
      });

      dotsContainer.appendChild(dot);
    }

    this.dots = document.querySelectorAll(".dot");
  }

  destroy() {
    this.stopAutoPlay();
    document.removeEventListener("keydown", this.handleKeydown);

    this.slider.removeEventListener("touchstart", this.handleTouchStart);
    this.slider.removeEventListener("touchmove", this.handleTouchMove);
    this.slider.removeEventListener("touchend", this.handleTouchEnd);
    this.slider.removeEventListener("mousedown", this.handleMouseDown);
    this.slider.removeEventListener("mouseup", this.handleMouseUp);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const slider = new Slider();

  window.slider = slider;
});

if (typeof module !== "undefined" && module.exports) {
  module.exports = Slider;
}
