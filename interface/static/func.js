function submit_form(){
    var game_choice = document.getElementById("game_dropdown").value;
    var data = {
        "game_choice": game_choice
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/set_parameters", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
}

function update_opp_choices(game_choice) {
    console.log(game_choice)
}