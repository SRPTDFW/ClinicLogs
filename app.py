<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SRPT Daily Clinic Log — Sign in</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
<div class="login-card">
  <h1>SRPT Daily Clinic Log</h1>
  <p id="subtitle">Select your clinic and enter its passcode to log today's checks.</p>
  {% if error %}<div class="error">{{ error }}</div>{% endif %}

  <form method="POST" id="clinicForm">
    <input type="hidden" name="mode" value="clinic">
    <select name="clinic" required>
      {% for c in clinics %}
        <option value="{{ c.name }}">{{ c.name }}</option>
      {% endfor %}
    </select>
    <input type="password" name="passcode" placeholder="Clinic passcode" required>
    <button class="btn" type="submit">Sign in</button>
  </form>

  <form method="POST" id="adminForm" class="hidden" style="display:none;">
    <input type="hidden" name="mode" value="admin">
    <input type="password" name="passcode" placeholder="Admin passcode" required>
    <button class="btn clay" type="submit">Sign in as admin</button>
  </form>

  <div class="login-toggle">
    <button type="button" id="toggleBtn">Signing in as an admin instead?</button>
  </div>
</div>

<script>
  const clinicForm = document.getElementById('clinicForm');
  const adminForm = document.getElementById('adminForm');
  const toggleBtn = document.getElementById('toggleBtn');
  const subtitle = document.getElementById('subtitle');
  let adminMode = false;
  toggleBtn.addEventListener('click', ()=>{
    adminMode = !adminMode;
    clinicForm.style.display = adminMode ? 'none' : 'flex';
    adminForm.style.display = adminMode ? 'flex' : 'none';
    toggleBtn.textContent = adminMode ? 'Signing in at a clinic instead?' : 'Signing in as an admin instead?';
    subtitle.textContent = adminMode ? 'Enter the admin passcode to manage clinics and view all records.' : "Select your clinic and enter its passcode to log today's checks.";
  });
</script>
</body>
</html>
