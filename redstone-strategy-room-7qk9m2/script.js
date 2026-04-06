document.querySelectorAll('.accordion-item').forEach((item) => {
  item.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.accordion-item').forEach((el) => el.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
