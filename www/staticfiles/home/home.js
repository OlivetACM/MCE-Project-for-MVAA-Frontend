function decode_html(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

function my_function(data) {
    clean_data = JSON.parse(decode_html(data))

    for (military_courses = 0; military_courses < clean_data.length; military_courses++) {
        document.write('<hr style="border: 2px solid#5b9aa0;" /><br>')
        for (equivalent_courses = 0; equivalent_courses < clean_data[military_courses].length; equivalent_courses++) {
            if (equivalent_courses == 0) {
                document.write("JST/AU Course Number: ", clean_data[military_courses][equivalent_courses]["CourseNumber"], "<br>")
                document.write("Course Name:", clean_data[military_courses][equivalent_courses]["CourseName"], "<br>")
                document.write("Course Decription: ", clean_data[military_courses][equivalent_courses]["CourseDescription"], "<br><br>")
            }

            document.write("OC Course Number: ", clean_data[military_courses][equivalent_courses]["CourseEquivalenceNonOC"], "<br>")
            document.write("Course Name: ", clean_data[military_courses][equivalent_courses]["OCCourseName"], "<br>")
            document.write("Course Description: ", clean_data[military_courses][equivalent_courses]["OCCourseDescription"], "<br>")
            document.write("Approved Credits: ", clean_data[military_courses][equivalent_courses]["CourseCredit"], "<br><br>")

        }
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

// NV-2201-0128 NV-1710-0118