function submit_form() {
    var game_choice = document.getElementById("game_dropdown").value;
    var opp_choice = document.getElementById("opp_dropdown").value;
    var player_team_choice = document.getElementById("player_team_dropdown").value;
    var opp_team_choice = document.getElementById("opp_team_dropdown").value;
    var data = {
        "game_choice": game_choice,
        "opp_choice": opp_choice,
        "player_team_choice": player_team_choice,
        "opp_team_choice": player_team_choice
    };

    var xhr = new XMLHttpRequest();
    // Set properties of request
    xhr.open("POST", "/set_parameters", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    // On request competion
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            set_opts(JSON.parse(this.responseText));
        } else if (this.status == 500) {
            alert("Something went wrong...");
        }
    };
    // Send the request.
    xhr.send(JSON.stringify(data));
}

function update_opp_choices(game_choice) {
    var opp_choices = document.getElementById("opp_dropdown");

    // Clear the list
    opp_choices.options.length = 0;

    // Repopulate
    var options = [];
    if (game_choice == "rps") {
        var option1 = document.createElement("option");
        option1.text = "Random";
        option1.value = "random_rps"
        var option2 = document.createElement("option");
        option2.text = "Counter";
        option2.value = "counter_rps"
        var option3 = document.createElement("option");
        option3.text = "Rock";
        option3.value = "rock_rps";
        var option4 = document.createElement("option");
        option4.text = "Paper";
        option4.value = "paper_rps";
        var option5 = document.createElement("option");
        option5.text = "Scissors";
        option5.value = "scissors_rps";
        var option6 = document.createElement("option");
        option6.text = "Uniform";
        option6.value = "uniform_rps";

        options.push(option1);
        options.push(option2);
        options.push(option3);
        options.push(option4);
        options.push(option5);
        options.push(option6);
    } else {
        var option1 = document.createElement("option");
        option1.text = "Random";
        option1.value = "random_pkmn"
        var option2 = document.createElement("option");
        option2.text = "Basic Planning";
        option2.value = "basic_planning_pkmn"

        options.push(option1)
        options.push(option2)
    }

    options.forEach(function (option) {
        opp_choices.add(option)
    });
    update_team(game_choice)
}

function update_team(game_choice) {
    var opp_team_dropdown = document.getElementById("opp_team_dropdown");
    var player_team_dropdown = document.getElementById("player_team_dropdown");

    // Clear the list
    opp_team_dropdown.options.length = 0;
    player_team_dropdown.options.length = 0;

    // REpopulate
    var options = []
    if (game_choice === "rps") {
        var option1 = document.createElement("option");
        option1.text = "N/A";
        options.push(option1)
    } else {
        var option1 = document.createElement("option");
        option1.text = "Spinda";
        option1.value = "spinda"
        var option2 = document.createElement("option");
        option2.text = "Floatzel";
        option2.value = "floatzel"
        var option3 = document.createElement("option");
        option3.text = "Ivysaur";
        option3.value = "ivysaur"
        options.push(option1)
        options.push(option2)
        options.push(option3)
    }

    options.forEach(function (option) {
        opp_team_dropdown.add(option.cloneNode(true));
        player_team_dropdown.add(option.cloneNode(true));
    });
}

function set_opts(options) {
    console.log(options)
    // Set player's active Pokemon
    var game_window = document.getElementById("game_window")
    typeof(create_poke_DOM(options["player_active"], false))
    game_window.appendChild(create_poke_DOM(options["player_active"], false))
    game_window.appendChild(create_poke_DOM(options["opp_active"], true))
}

function create_poke_DOM(data, opponent){
    // Create the pokemon display from the data given.
    var url = "https://play.pokemonshowdown.com/sprites/afd/REPLACE.png".replace("REPLACE", data["name"]);
    var hp_pct = "REPLACE%".replace("REPLACE", data["current_hp"]*100/data["max_hp"]);
    var hp_raw = "(REPLACE1/REPLACE2)".replace("REPLACE1", data["current_hp"])
                                    .replace("REPLACE2", data["max_hp"]);
    
    var poke_div = document.createElement("div")
    poke_div.style.width = "40%"
    poke_div.style.display = "inline-block"
    // Set player/Opponent box
    var title = document.createElement("h5")
    if (opponent) {
        title.innerHTML = "".concat("Opponent's ", data["name"])
    } else {
        title.innerHTML = "".concat("Player's ", data["name"])
    }
    // Set image
    var poke_img = document.createElement("img")
    poke_img.src = url
    // Set HP String
    poke_hp_text = "Current HP: "
    poke_hp_text = poke_hp_text.concat(hp_pct)
    if (!opponent) {
        poke_hp_text = poke_hp_text.concat(" ", hp_raw)
    }
    
    var poke_hp = document.createElement("p")
    poke_hp.innerHTML = poke_hp_text

    poke_div.appendChild(title)
    poke_div.appendChild(poke_img)
    poke_div.appendChild(poke_hp)

    return poke_div
}

function create_move_DOM(moves) {
    console.log(moves)
}