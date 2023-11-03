// document.addEventListener('DOMContentLoaded', function() {
//   const likeButton = document.getElementById('likeButton')
//   const likeCount = document.getElementById('likeCount')
  
//   if (likeButton) {
//     likeButton.addEventListener('click', function() {
//       let liked = likeButton.classList.contains('liked')
//       if (liked) {
//         likeButton.src = likeButton.src.replace('liked.png', 'like.png')
//         likeButton.classList.remove('liked')
//         likeCount.innerText = parseInt(likeCount.innerText) - 1
//       } else {
//         likeButton.src = likeButton.src.replace('like.png', 'liked.png')
//         likeButton.classList.add('liked')
//         likeCount.innerText = parseInt(likeCount.innerText) + 1
//       }
//     })
//   }
// })

document.addEventListener('DOMContentLoaded', function() {
  const likeButton = document.getElementById('likeButton')
  const likeCount = document.getElementById('likeCount')
  const csrfToken = document.cookie.match(/csrftoken=([^ ;]+)/)[1]

  if (likeButton) {
    likeButton.addEventListener('click', function() {
      let liked = likeButton.classList.contains('liked')
      const articleId = likeButton.dataset.articleId

      fetch(`/articles/${articleId}/like/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ liked: !liked })  
      })
      .then(response => response.json())
      .then(data => {
        likeCount.innerText = data.likes

        if (liked) {
          likeButton.src = likeButton.src.replace('liked.png', 'like.png')
          likeButton.classList.remove('liked')
        } else {
          likeButton.src = likeButton.src.replace('like.png', 'liked.png')
          likeButton.classList.add('liked')
        }
      })
      .catch(error => console.error('Error:', error))
    })
  }
})





