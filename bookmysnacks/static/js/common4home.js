function changeContent(page) {
    // Hide all content
    document.querySelectorAll('.card').forEach(card => {
      card.classList.add('hidden');
    });

    // Show the selected content
    document.getElementById(page + '-content').classList.remove('hidden');

    // Update the breadcrumb and title
    document.getElementById('current-page').innerText = page.charAt(0).toUpperCase() + page.slice(1);
    document.getElementById('page-title').innerText = page.charAt(0).toUpperCase() + page.slice(1);
    
    // Update active link
    document.querySelectorAll('.sidebar ul li a').forEach(link => {
      link.classList.remove('active');
    });
    document.querySelector(`.sidebar ul li a[onclick="changeContent('${page}')"]`).classList.add('active');
  }

