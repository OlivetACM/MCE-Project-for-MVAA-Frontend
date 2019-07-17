function decode_html(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

function my_function(data) {
    clean_data = JSON.parse(decode_html(data))["Data"]

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

function pdf_data_organizer(data) {
    clean_data = JSON.parse(decode_html(data))
    for (military_courses = 0; military_courses < clean_data.length; military_courses++) {
        document.write("<tr><td>", clean_data[military_courses][equivalent_courses]["CourseNumber"], "</td></tr>")
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

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name')
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('-');
    return false;
}
function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-row:last', 'form');
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});

// NV-2201-0128 NV-1710-0118