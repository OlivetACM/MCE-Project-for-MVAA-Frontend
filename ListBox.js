function showChoices() {
    var selLanguage = document.getElementById("selLanguage");
    var result = "<h2>Your Languages</h2>";
    result += "<ul>";
    for (var i = 0; i < selLanguage.length; i++) {
        var currentOption = selLanguage[i];
        if (currentOption.selected == true) {
            result += "<li>" + currentOption.value + "</li>";
        }
    }
    result += "</ul>";
    var output = document.getElementById("output");
    output.innerHTML = result;
}