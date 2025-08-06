document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('user-select');
  const statsContainer = document.getElementById('stats');

  fetch('/api/users')
    .then(res => res.json())
    .then(users => {
      users.forEach(user => {
        const option = document.createElement('option');
        option.value = user.user_id;
        option.textContent = user.username;
        select.appendChild(option);
      });
    });

  select.addEventListener('change', () => {
    const userId = select.value;
    fetch(`/api/user/${userId}/games`)
      .then(res => res.json())
      .then(games => {
        statsContainer.innerHTML = '';
        if (games.length === 0) {
          statsContainer.textContent = 'No games found for this user.';
          return;
        }
        games.forEach(game => {
          const div = document.createElement('div');
          div.className = 'game-card';
          div.innerHTML = `
            <strong>${game.name}</strong><br>
            Playtime: ${game.playtime_hours} hours<br>
            Rating: ${game.rating ?? 'N/A'}<hr>
          `;
          statsContainer.appendChild(div);
        });
      });
  });
});