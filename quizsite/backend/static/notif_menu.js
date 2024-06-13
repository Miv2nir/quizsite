//reveal the notif creation form on button press
function reveal_button(button) {
    button.style.display = 'None';
    document.getElementById('revealme').style.display = 'flex';
    document.getElementById('revealme-too').style.display = 'block';
}