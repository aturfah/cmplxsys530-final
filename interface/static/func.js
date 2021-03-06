function uc_first_char(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function submit_form() {
    var game_choice = document.getElementById("game_dropdown").value;
    var opp_choice = document.getElementById("opp_dropdown").value;
    var player_team_choice = document.getElementById("player_team_dropdown").value;
    var opp_team_choice = document.getElementById("opp_team_dropdown").value;
    var req_data = {
        "game_choice": game_choice,
        "opp_choice": opp_choice,
        "player_team_choice": player_team_choice,
        "opp_team_choice": opp_team_choice
    };

    if (game_choice === "rps") {
        alert("Rock/Paper/Scissors is not supported as of yet. This will not work.")
        return
    }

    $.post("/set_parameters", req_data, function (data) {
        document.getElementById("game_log").innerHTML = ""
        set_opts(data);
        update_gamestate(data);
    });
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

    // Repopulate
    var options = []
    if (game_choice === "rps") {
        var option1 = document.createElement("option");
        option1.text = "N/A";
        opp_team_dropdown.add(option1.cloneNode(true));
        player_team_dropdown.add(option1.cloneNode(true));
    } else {
            // Send request to /team_options endpoint
            $.get("/team_options", success=function(data) {
            data["teams"].forEach(function(datum) {
                var option_i = document.createElement("option")
                option_i.text = datum
                option_i.value = datum
                opp_team_dropdown.add(option_i.cloneNode(true));
                player_team_dropdown.add(option_i.cloneNode(true));
            })
        });
    }
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

function create_poke_DOM(data, opponent) {
    // Create the pokemon display from the data given.
    var url = "https://play.pokemonshowdown.com/sprites/afd/REPLACE.png".replace("REPLACE", data["name"]);
    var hp_pct = " <span id='opp_pct_hp'>REPLACE%</span>".replace("REPLACE", data["current_hp"] * 100 / data["max_hp"]);
    var hp_raw = " (<span id='poke_raw_hp'>REPLACE1</span>/REPLACE2)".replace("REPLACE1", data["current_hp"])
        .replace("REPLACE2", data["max_hp"]);

    var poke_div = document.createElement("div")
    poke_div.style.width = "40%"
    poke_div.style.display = "inline-block"
    // Set player/Opponent box
    var title = document.createElement("h5")
    title.classList.add("pkmn_title")
    if (opponent) {
        title.innerHTML = "".concat("Opponent's ", uc_first_char(data["name"]))
        poke_div.id = "opponent_poke"
    } else {
        title.innerHTML = "".concat("Player's ", uc_first_char(data["name"]))
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

    var poke_info = document.createElement("p")
    poke_info.innerHTML = poke_hp_text

    var boost_txt = "<br/><b>Boosts</b><br/>";
    var stats = ["atk", "def", "spa", "spd", "spe"];
    stats.forEach(function (stat_name) {
        if (data["boosts"][stat_name] !== 0) {
            new_str = stat_name.concat(": ")
            if (data["boosts"][stat_name] > 0) {
                new_str = new_str.concat("+", data["boosts"][stat_name])
            } else {
                new_str = new_str.concat(data["boosts"][stat_name])
            }
            boost_txt = boost_txt.concat(new_str, "<br/>")
        }
    });
    poke_info.innerHTML += boost_txt

    poke_div.appendChild(title)
    poke_div.appendChild(poke_img)
    poke_div.appendChild(poke_info)

    return poke_div
}

function create_move_DOM(moves) {
    var move_div = document.createElement("div")
    move_div.id = "moves"
    var atk_div = document.createElement("div")
    var switch_div = document.createElement("div")
    var atk_btns = []
    var switch_btns = []
    moves.forEach(function (move) {
        var move_btn = document.createElement("input");
        move_btn.type = "button"
        move_btn.value = "".concat(move[0], " ", move[2])
        move_btn.style.margin = "10px 10px 0px 0px";
        move_btn.onclick = function () {
            submit_move([move[0], move[1]])
        }
        if (move[0] === "ATTACK") {
            atk_btns.push(move_btn)
        } else {
            switch_btns.push(move_btn)
        }
    });

    atk_btns.forEach(function (btn) {
        atk_div.appendChild(btn)
    });
    switch_btns.forEach(function (btn) {
        switch_div.appendChild(btn)
    });

    move_div.appendChild(atk_div);
    move_div.appendChild(switch_div);
    return move_div
}

function submit_move(move_choice) {
    // Set properties of request
    var req_data = {
        "move_class": move_choice[0],
        "move_choice": move_choice[1]
    }

    $.post("/make_move", req_data, function(data) {
        set_opts(data);
        update_log(data);
        update_gamestate(data);
    });
}

function update_log(data) {
    var game_log = document.getElementById("game_log")
    var new_entry = document.createElement("p")
    var outcome = data["outcome"]
    var turn_info = data["turn_info"]

    var new_str = "";

    // Log the info
    turn_info.forEach(function (datum) {
        if (datum["type"] === "SWITCH"){
            // Switching
            if(datum["player"] === "player1") {
                new_str = new_str.concat("Player switched to ");
            } else {
                new_str = new_str.concat("Opponent switched to ");
            }
            new_str = new_str.concat(datum["new_active"], ".<br/>");
        } else {
            // Attacking
            var player_attacking = datum["attacker"] === "player1"
            if (player_attacking) {
                new_str = new_str.concat("Player's ")
            } else {
                new_str = new_str.concat("Opponent's ")
            }
    
            new_str = new_str.concat(datum["atk_poke"], " attacked ", datum["def_poke"], " with ", datum["move"]["name"])
            new_str = new_str.concat(". It did ", datum["pct_damage"], "%")
    
            if (!player_attacking) {
                new_str = new_str.concat(" (", datum["damage"], ")")
            }
            new_str = new_str.concat(" damage.<br/>")
        }
    });
    new_entry.innerHTML += "".concat(new_str, "<br/>")

    if (outcome["finished"] === true) {
        if (outcome["winner"] === 1) {
            new_entry.innerHTML += "You win! :D"
        } else {
            new_entry.innerHTML += "Opponent wins... :("
        }
    }
    game_log.appendChild(new_entry)

}

function create_team_list(gamestate, owner){
    var icon_placeholder = "https://www.serebii.net/pokedex-sm/icon/{DEX_NUM}.png";
    var team_icons = document.createElement("ul");
    team_icons.classList.add("pokemon_list");

    var temp_li = document.createElement("li");
    temp_li.id = owner.concat("_icon_", gamestate["active"]["dex_num"]);
    var active_icon = document.createElement("img");
    active_icon.src = icon_placeholder.replace("{DEX_NUM}", gamestate["active"]["dex_num"].toString().padStart(3, "0"));
    temp_li.onmouseover = function () {
        make_pkmn_data_visible(gamestate["active"]["dex_num"], owner.concat("_info"), owner.concat("_info_"))
    }
    temp_li.appendChild(active_icon);
    team_icons.appendChild(temp_li);
    gamestate["team"].forEach(function (pkmn) {
        let temp_li = document.createElement("li");
        temp_li.id = owner.concat("_icon_", pkmn["dex_num"]);
        var team_icon = document.createElement("img");
        team_icon.src = icon_placeholder.replace("{DEX_NUM}", pkmn["dex_num"].toString().padStart(3, "0"));
        temp_li.onmouseover = function () {
            make_pkmn_data_visible(pkmn["dex_num"], owner.concat("_info"), owner.concat("_info_"))
        }
        temp_li.appendChild(team_icon);
        team_icons.appendChild(temp_li);
    });
    return(team_icons)
}

function create_player_pkmn_panel(pkmn_data, active) {
    var id_prefix = "player_info_";
    var data_div = document.createElement("div");
    data_div.id = id_prefix.concat(pkmn_data["dex_num"]);

    data_list = document.createElement("ul");

    // Add Pokemon's name
    var name_element = document.createElement("li");
    name_element.innerHTML = "<b>Name:</b> ".concat(uc_first_char(pkmn_data["name"]));
    data_list.appendChild(name_element);

    // Add Pokemon's HP
    var hp_element = document.createElement("li");
    hp_element.innerHTML = "<b>Hit Points:</b> ".concat(pkmn_data["current_hp"], "/", pkmn_data["max_hp"]);
    data_list.appendChild(hp_element);

    // Add Pokemon's status, if present
    if (pkmn_data["status"] !== null) {
        let status_element = document.createElement("li");
        status_element.innerHTML = "<b>Status:</b> ".concat(pkmn_data["status"]);
        data_list.appendChild(status_element);
    }

    // Display Pokemon's moves, if not active
    var moves_label = document.createElement("li");
    moves_label.innerHTML = "<b>Moves:</b>";
    var move_sublist = document.createElement("ul");
    pkmn_data["moves"].forEach(function (move_info){
        let move_li = document.createElement("li");
        move_li.innerHTML = move_info["name"];
        move_sublist.appendChild(move_li);
    });
    data_list.appendChild(moves_label);
    data_list.appendChild(move_sublist);

    // Display pokemon's stats, and boosts (if active)
    var stats = [["attack", "atk"], ["defense", "def"], ["sp_attack","spa"], ["sp_defense", "spd"], ["speed", "spe"]];
    var stat_label = document.createElement("li");
    stat_label.innerHTML = "<b>Stats:</b>";
    var stat_ul = document.createElement("ul");
    stats.forEach(function (stat_pair) {
        let stat_name = stat_pair[0];
        let stat_key = stat_pair[1];
        stat_li = document.createElement("li");
        var boost_text = ""
        if (pkmn_data["boosts"][stat_key] !== 0) {
            boost_text = " @ ";
            if (pkmn_data["boosts"][stat_key] > 0) {
                boost_text = boost_text.concat("+", pkmn_data["boosts"][stat_key]);
            } else {
                boost_text = boost_text.concat(pkmn_data["boosts"][stat_key]);
            }
        }
        stat_li.innerHTML = uc_first_char(stat_name).concat(": ", pkmn_data[stat_name], boost_text);
        stat_ul.appendChild(stat_li);
    });
    data_list.appendChild(stat_label);
    data_list.appendChild(stat_ul);

    data_div.appendChild(data_list);
    return(data_div);
}

function create_opponent_pkmn_panel(pkmn_data, active, move_data, investment_data) {
    // Set up the and preliminary list
    var id_prefix = "opponent_info_";
    var data_div = document.createElement("div");
    data_div.id = id_prefix.concat(pkmn_data["dex_num"]);

    data_list = document.createElement("ul");

    // Add pokemon's name
    var name_element = document.createElement("li");
    name_element.innerHTML = "<b>Name:</b> ".concat(uc_first_char(pkmn_data["name"]));
    data_list.appendChild(name_element);

    // Add Pokemon % HP
    var hp_element = document.createElement("li");
    var pct_hp = 100 * pkmn_data["pct_hp"];
    hp_element.innerHTML = "<b>HP remaining:</b> ".concat(pct_hp, "%");
    data_list.appendChild(hp_element);

    // Add Pokemon's status, if present
    if (pkmn_data["status"] !== null) {
        let status_element = document.createElement("li");
        status_element.innerHTML = "<b>Status:</b> ".concat(pkmn_data["status"]);
        data_list.appendChild(status_element);
    }

    // Display known moves
    if (move_data) {
        var move_label = document.createElement("li");
        move_label.innerHTML = "<b>Moves</b>";
        data_list.appendChild(move_label);
        var move_ul = document.createElement("ul");
        move_data.forEach(function (move_info) {
            let move_li = document.createElement("li");
            move_li.innerHTML = move_info["name"];
            move_ul.appendChild(move_li);
        });
        data_list.appendChild(move_label);
        data_list.appendChild(move_ul);
    }

    // Display Attack, Defense, Sp.Attack, Sp.Defense investment inferences
    var stats = [["hitpoints", "hp"], ["attack", "atk"], ["defense", "def"], ["sp_attack","spa"], ["sp_defense", "spd"]];
    var stat_label = document.createElement("li");
    stat_label.innerHTML = "<b>Stats:</b>"
    var stat_ul = document.createElement("ul");
    stats.forEach(function(stat_pair){
        let stat_name = stat_pair[0];
        let stat_key = stat_pair[1];
        let stat_li = document.createElement("li");
        stat_li.innerHTML = uc_first_char(stat_name).concat(" Investments"); 
        stat_ul.appendChild(stat_li);

        // List for the investment info
        investment_ul = document.createElement("ul");
        investment_data[stat_key].forEach(function (investment_pair) {
            let temp_li = document.createElement("li");
            temp_li.innerHTML = ""
            if (investment_pair["positive_nature"] !== undefined) {
                temp_li.innerHTML = temp_li.innerHTML.concat("Positive Nature: ", investment_pair["positive_nature"], " || ")
            }
            temp_li.innerHTML = temp_li.innerHTML.concat("Investment: ", investment_pair["max_evs"]);
            investment_ul.appendChild(temp_li);
        });
        stat_ul.appendChild(investment_ul);
    });
    data_list.appendChild(stat_label);
    data_list.appendChild(stat_ul);

    // Display speed range
    var speed_element = document.createElement("li");
    speed_element.innerHTML = "<b>Speed Range:</b> ".concat(investment_data["spe"][0], " to ", investment_data["spe"][1]);
    data_list.appendChild(speed_element);

    data_div.appendChild(data_list)

    return data_div
}

function update_gamestate(data) {
    // Check if game is over (don't update gamestate)
    var outcome = data["outcome"]
    if (outcome["finished"] === true) {
        return;
    }

    // Set up variables for player and opponent
    var player_div = document.getElementById("player_info");
    var player_gs = data["gamestate"]["player"];

    var opponent_div = document.getElementById("opponent_info");
    var opponent_gs = data["gamestate"]["opponent"];

    // Make team icons for player
    player_div.innerHTML = ""
    player_div.appendChild(create_team_list(player_gs, "player"));

    // Make team icons for opponent
    opponent_div.innerHTML = "";
    opponent_div.appendChild(create_team_list(opponent_gs["data"], "opponent"));

    //Make divs for the player's info
    player_div.appendChild(create_player_pkmn_panel(player_gs["active"], true));
    player_gs["team"].forEach(function (pkmn_datum) {
        player_div.appendChild(create_player_pkmn_panel(pkmn_datum, false));
    });

    //Make divs for opponent's info
    opponent_div.appendChild(create_opponent_pkmn_panel(opponent_gs["data"]["active"], true,
                                                        opponent_gs["moves"][opponent_gs["data"]["active"]["name"]],
                                                        opponent_gs["investment"][opponent_gs["data"]["active"]["name"]]));
    opponent_gs["data"]["team"].forEach(function (pkmn_datum) {
        let poke_name = pkmn_datum["name"]
        opponent_div.appendChild(create_opponent_pkmn_panel(pkmn_datum, false, opponent_gs["moves"][poke_name], opponent_gs["investment"][poke_name]))
    })

    make_pkmn_data_visible(player_gs["active"]["dex_num"], "player_info", "player_info_")
    make_pkmn_data_visible(opponent_gs["data"]["active"]["dex_num"], "opponent_info", "opponent_info_")
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

function make_pkmn_data_visible(dex_num, info_div, id_prefix) {
    // Make other divs invisible
    player_info_div = document.getElementById(info_div);
    player_info_div.childNodes.forEach(function (child_node) {
        if (child_node.id.includes(id_prefix)) {
            child_node.classList.add("invisible_panel");
        }
    });

    // Make this div visible
    target_div = document.getElementById(id_prefix.concat(dex_num));
    target_div.classList.remove("invisible_panel")
}