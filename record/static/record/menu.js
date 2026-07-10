document.getElementById('toggleBtn').addEventListener('click', function () {
  document.getElementById('toggleSidebar').classList.toggle('active');
});


document.getElementById('closeBtn').addEventListener('click', function () {
  document.getElementById('toggleSidebar').classList.remove('active');
});

