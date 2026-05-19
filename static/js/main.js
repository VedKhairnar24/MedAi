/**
 * MedAI - Modern JavaScript Interactions
 * Enhanced UX with smooth animations and interactions
 */

document.addEventListener('DOMContentLoaded', function() {
  // ========================================
  // 1. Smooth Page Load Animation
  // ========================================
  const fadeElements = document.querySelectorAll('.fade-in');
  fadeElements.forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    setTimeout(() => {
      el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, 100 * (index + 1));
  });

  // ========================================
  // 2. Smooth Scroll for Anchor Links
  // ========================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ========================================
  // 3. Add ripple effect to buttons
  // ========================================
  document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.classList.add('ripple');
      this.appendChild(ripple);

      setTimeout(() => ripple.remove(), 600);
    });
  });

  // ========================================
  // 4. Number Counter Animation
  // ========================================
  const statCards = document.querySelectorAll('.stat-card');
  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const element = entry.target;
        const text = element.querySelector('.fs-1, .fs-2');
        
        if (text && !isNaN(text.textContent)) {
          animateCounter(text);
        }
        observer.unobserve(element);
      }
    });
  }, observerOptions);

  statCards.forEach(card => observer.observe(card));

  function animateCounter(element) {
    const target = parseInt(element.textContent);
    const duration = 1000;
    const step = target / (duration / 16);
    let current = 0;

    const interval = setInterval(() => {
      current += step;
      if (current >= target) {
        element.textContent = target;
        clearInterval(interval);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 16);
  }

  // ========================================
  // 5. Table Row Animations
  // ========================================
  document.querySelectorAll('.table tbody tr').forEach((row, index) => {
    row.style.opacity = '0';
    row.style.transform = 'translateX(-20px)';
    setTimeout(() => {
      row.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
      row.style.opacity = '1';
      row.style.transform = 'translateX(0)';
    }, 50 * (index + 1));
  });

  // ========================================
  // 6. Form Input Focus Effects
  // ========================================
  document.querySelectorAll('.form-control, .form-select').forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });

    input.addEventListener('blur', function() {
      this.parentElement.classList.remove('focused');
    });
  });

  // ========================================
  // 7. Symptom Chip Interactions (if on predict page)
  // ========================================
  const symptomChips = document.querySelectorAll('.symptom-chip');
  const selectedTagsContainer = document.getElementById('selected-tags');
  const symptomInput = document.getElementById('symptom-input');

  if (symptomChips.length > 0 && selectedTagsContainer) {
    symptomChips.forEach(chip => {
      chip.addEventListener('click', function() {
        const symptom = this.textContent.trim();
        const tagId = `tag-${symptom.replace(/\s+/g, '-')}`;
        const existingTag = document.getElementById(tagId);

        if (existingTag) {
          existingTag.remove();
          this.classList.remove('selected');
        } else {
          const tag = document.createElement('span');
          tag.id = tagId;
          tag.className = 'badge bg-teal text-white';
          tag.style.padding = '8px 12px';
          tag.style.cursor = 'pointer';
          tag.style.display = 'inline-flex';
          tag.style.alignItems = 'center';
          tag.style.gap = '8px';
          tag.style.transition = 'all 0.3s ease';
          tag.innerHTML = `${symptom} <i class="fas fa-times" style="cursor:pointer; font-size: 0.8rem;"></i>`;
          
          tag.addEventListener('click', () => {
            tag.style.opacity = '0';
            tag.style.transform = 'scale(0.8)';
            setTimeout(() => tag.remove(), 200);
            this.classList.remove('selected');
          });

          if (selectedTagsContainer.querySelector('.text-muted')) {
            selectedTagsContainer.innerHTML = '';
          }
          selectedTagsContainer.appendChild(tag);
          this.classList.add('selected');
        }

        // Update symptom input
        updateSymptomInput();
      });
    });
  }

  function updateSymptomInput() {
    if (symptomInput && selectedTagsContainer) {
      const tags = Array.from(selectedTagsContainer.querySelectorAll('.badge'))
        .map(tag => tag.textContent.trim().replace(/×/g, '').trim());
      symptomInput.value = tags.join(', ');
    }
  }

  // ========================================
  // 8. Alert Auto-Dismiss
  // ========================================
  document.querySelectorAll('.alert').forEach(alert => {
    if (alert.classList.contains('alert-success')) {
      setTimeout(() => {
        alert.style.transition = 'opacity 0.4s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 400);
      }, 4000);
    }
  });

  // ========================================
  // 9. Add Hover Effects to Cards
  // ========================================
  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-8px)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // ========================================
  // 10. Navbar Active Link Highlight
  // ========================================
  const navLinks = document.querySelectorAll('.sidebar a');
  navLinks.forEach(link => {
    if (link.href === window.location.href) {
      link.classList.add('active');
    }
  });

  // ========================================
  // 11. Loading Animation
  // ========================================
  window.showLoading = function() {
    const loader = document.createElement('div');
    loader.className = 'spinner-border text-teal';
    loader.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 9999;
    `;
    document.body.appendChild(loader);
  };

  window.hideLoading = function() {
    const loader = document.querySelector('.spinner-border');
    if (loader) loader.remove();
  };

  // ========================================
  // 12. Scroll to Top Button
  // ========================================
  const scrollTopBtn = document.createElement('button');
  scrollTopBtn.className = 'btn btn-teal';
  scrollTopBtn.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    padding: 0;
    display: none;
    z-index: 999;
    box-shadow: 0 4px 12px rgba(2, 128, 144, 0.3);
  `;
  scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
  document.body.appendChild(scrollTopBtn);

  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
      scrollTopBtn.style.display = 'flex';
      scrollTopBtn.style.alignItems = 'center';
      scrollTopBtn.style.justifyContent = 'center';
    } else {
      scrollTopBtn.style.display = 'none';
    }
  });

  scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  // ========================================
  // 13. Form Validation Visual Feedback
  // ========================================
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      let isValid = true;
      
      this.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
          field.classList.add('is-invalid');
          isValid = false;
        } else {
          field.classList.remove('is-invalid');
        }
      });

      if (!isValid) {
        e.preventDefault();
        showNotification('Please fill in all required fields', 'warning');
      }
    });
  });

  // ========================================
  // 14. Notification System
  // ========================================
  window.showNotification = function(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.style.cssText = `
      position: fixed;
      top: 100px;
      right: 20px;
      max-width: 400px;
      z-index: 9998;
      animation: slideDown 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    `;
    notification.innerHTML = `
      <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
      ${message}
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.opacity = '0';
      notification.style.transform = 'translateY(-20px)';
      setTimeout(() => notification.remove(), 400);
    }, 4000);
  };

  // ========================================
  // 15. Dark/Light Mode Toggle (if implemented)
  // ========================================
  const themeToggle = localStorage.getItem('theme') || 'light';
  if (themeToggle === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  console.log('✨ MedAI modern interactions loaded successfully!');
});

// Add ripple CSS dynamically
const style = document.createElement('style');
style.textContent = `
  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    transform: scale(0);
    animation: ripple-animation 0.6s ease-out;
    pointer-events: none;
  }

  @keyframes ripple-animation {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }

  .is-invalid {
    border-color: #ef4444 !important;
    background: rgba(239, 68, 68, 0.05) !important;
  }

  .selected {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
    color: #065f46 !important;
  }
`;
document.head.appendChild(style);
