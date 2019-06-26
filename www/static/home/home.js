function decode_html(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    console.log(txt.innerHTML)
    return txt.value;
}

function my_function(data) {
    var clean_data = data.toString().replace(/'/g, '"')
    document.write(clean_data)
}

function empty() {
    var x;
    x = document.getElementById("course_code").value;
    if (x == "") {
        alert("Please enter a valid course code.");
        return false;
    };
}