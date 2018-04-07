function submit_form(){
    var game_choice = document.getElementById("game_dropdown").value;
    var data = {
        "game_choice": game_choice
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/set_engine", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
}