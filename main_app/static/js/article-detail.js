document.addEventListener('DOMContentLoaded', function() {
  const likeButton = document.getElementById('likeButton')
  const likeCount = document.getElementById('likeCount')
  
  if (likeButton) {
    likeButton.addEventListener('click', function() {
      let liked = likeButton.classList.contains('liked')
      if (liked) {
        likeButton.src = likeButton.src.replace('liked.png', 'like.png')
        likeButton.classList.remove('liked')
        likeCount.innerText = parseInt(likeCount.innerText) - 1
      } else {
        likeButton.src = likeButton.src.replace('like.png', 'liked.png')
        likeButton.classList.add('liked')
        likeCount.innerText = parseInt(likeCount.innerText) + 1
      }
    })
  }
})
