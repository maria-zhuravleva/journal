document.addEventListener('DOMContentLoaded', function() {
  document.addEventListener('click', function(event) {
    const anchor = event.target.closest('a')
    if (anchor && (anchor.id === 'tapHere' || anchor.id === 'tapArrow')) {
      event.preventDefault()
      document.querySelector('.landingPage').classList.add('slide-out')
      setTimeout(function() {
        window.location.href = anchor.getAttribute('href')
      }, 100)
    }
  })
})

document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('.slide-in')

  images.forEach(image => {
    image.style.transform = 'translateX(0)'
    image.style.opacity = '1'
  })
})








