function decode_html(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    console.log(txt.innerHTML)
    return txt.value;
}

function my_function(data) {
    var clean_data = data.toString().replace(/'/g, '"')
    var decoded_data = decode_html(clean_data)
    var new_data = JSON.parse(decoded_data)
    console.log(decoded_data)
    document.write("Course Number: ", new_data[0]["CourseNumber"]);
    document.write("<br>")
    document.write("Course Name: ", new_data[0]["CourseName"]);
    document.write("<br>")
    document.write("Course Description: ", new_data[0]["CourseDescription"]);

    document.write("<br>")
    document.write("<br>")
    document.write("<br>")


    for(i = 0; i < 3; i++) {
        document.write("Course Equivalence: ", new_data[i]["CourseEquivalenceNonOC"])
        document.write("<br>")
        document.write("Course Name: ", new_data[i]["OCCourseName"])
        document.write("<br>")
        document.write("Course Description: ", new_data[i]["OCCourseDescription"])
        document.write("<br>")
        document.write("Course Credits: ", new_data[i]["CourseCredit"])
        document.write("<br>")
        document.write("<br>")
    }
}

function empty() {
    var x;
    x = document.getElementById("course_code").value;
    if (x == "") {
        alert("Please enter a valid course code.");
        return false;
    };
}