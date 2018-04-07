function submit_form(){
    var game_choice = document.getElementById("game_dropdown").value;
    var opp_choice = document.getElementById("opp_dropdown").value;
    var data = {
        "game_choice": game_choice,
        "opp_choice": opp_choice
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/set_parameters", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
}

function update_opp_choices(game_choice) {
    var opp_choices = document.getElementById("opp_dropdown");
    
    // Clear the list
    opp_choices.options.length = 0;
    
    // Repopulate
    options = []
    if (game_choice == "rps") {
        var option1 = document.createElement("option");
        option1.text = "Random";
        option1.value = "random_rps"
        var option2 = document.createElement("option");
        option2.text = "Counter";
        option2.value = "counter_rps"

        options.push(option1)
        options.push(option2)
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

    options.forEach(function(option){
        opp_choices.add(option)
    });
    update_opp_team(game_choice)
}

function update_opp_team(game_choice){
    var team_dropdown = document.getElementById("opp_team");

    // Clear the list
    team_dropdown.options.length = 0;

    // REpopulate
    var options = []
    if (game_choice === "rps"){
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

    options.forEach(function(option){
        team_dropdown.add(option);
    });
}