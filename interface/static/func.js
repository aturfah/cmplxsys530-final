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
    // Set player's active Pokemon
    if (options["outcome"]["finished"]) {
        update_battle_finished(options)
        return
    }

    var game_window = document.getElementById("game_window")
    game_window.innerHTML = ""
    game_window.appendChild(create_poke_DOM(options["player_active"], false))
    game_window.appendChild(create_poke_DOM(options["opp_active"], true))
    game_window.appendChild(create_move_DOM(options["player_opts"]))
}

function create_poke_DOM(data, opponent){
    // Create the pokemon display from the data given.
    var url = "https://play.pokemonshowdown.com/sprites/afd/REPLACE.png".replace("REPLACE", data["name"]);
    var hp_pct = " <span id='opp_pct_hp'>REPLACE%</span>".replace("REPLACE", data["current_hp"]*100/data["max_hp"]);
    var hp_raw = " (<span id='poke_raw_hp'>REPLACE1</span>/REPLACE2)".replace("REPLACE1", data["current_hp"])
                                    .replace("REPLACE2", data["max_hp"]);
    
    var poke_div = document.createElement("div")
    poke_div.style.width = "40%"
    poke_div.style.display = "inline-block"
    // Set player/Opponent box
    var title = document.createElement("h5")
    if (opponent) {
        title.innerHTML = "".concat("Opponent's ", data["name"])
        poke_div.id = "opponent_poke"
    } else {
        title.innerHTML = "".concat("Player's ", data["name"])
        poke_div.id = "player_poke"
    }
    // Set image
    var poke_img = document.createElement("img")
    poke_img.src = url
    // Set HP String
    poke_hp_text = "Current HP:"
    poke_hp_text = poke_hp_text.concat(hp_pct)
    if (!opponent) {
        poke_hp_text = poke_hp_text.concat(hp_raw)
        poke_hp_text = poke_hp_text.replace('opp_pct_hp', 'poke_pct_hp')
    }
    console.log(poke_hp_text)

    var poke_hp = document.createElement("p")
    poke_hp.innerHTML = poke_hp_text

    poke_div.appendChild(title)
    poke_div.appendChild(poke_img)
    poke_div.appendChild(poke_hp)

    return poke_div
}

function create_move_DOM(moves) {
    var move_div = document.createElement("div")
    move_div.id = "moves"
    moves.forEach(function(move){
        var move_btn = document.createElement("input");
        move_btn.type = "button"
        move_btn.value = move[2]
        move_btn.style.margin = "10px 10px 0px 0px";
        move_btn.onclick = function() {
            submit_move([move[0], move[1]])
        }
        move_div.appendChild(move_btn)
    });
    return move_div
}

function submit_move(move_choice) {
    // Set properties of request
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/make_move", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = {
        "move_choice": move_choice
    }
    // On request competion
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            set_opts(JSON.parse(this.responseText));
            update_log(JSON.parse(this.responseText))
        } else if (this.status == 500 || this.status == 404) {
            alert("Something went wrong...");
        }
    };
    // Send the request.
    xhr.send(JSON.stringify(data));
}

function update_log(data) {
    console.log(data)
}

function update_battle_finished(data) {
    document.getElementById("moves").innerHTML = ""
    if (data["outcome"]["winner"] === 0) {
        document.getElementById("poke_raw_hp").innerHTML = "0"
        document.getElementById("poke_pct_hp").innerHTML = "0%"
    } else {
        document.getElementById("opp_pct_hp").innerHTML = "0%"
    }
}