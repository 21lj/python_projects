function showPosts() {
    document.getElementById('posts').style.display = 'grid';
    document.getElementById('archived-posts').style.display = 'none';
    document.getElementById('posts-tab').classList.add('active');
    document.getElementById('archived-posts-tab').classList.remove('active');
}

function showArchivedPosts() {
    document.getElementById('posts').style.display = 'none';
    document.getElementById('archived-posts').style.display = 'grid';
    document.getElementById('posts-tab').classList.remove('active');
    document.getElementById('archived-posts-tab').classList.add('active');
}