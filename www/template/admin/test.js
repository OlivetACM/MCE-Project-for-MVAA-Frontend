        function clearList(list){
            var i;
            for( i = 0; i < list.options.length; i++){
                list.options.remove(i);
                }
            }

        function displaysameschool(){
            console.log("starting function")
            var school_inst = document.getElementById('select_institution').value;
            var list = document.getElementById('select_course');
            console.log(list);
            clearList(list);
            console.log(list);
            if (school_inst == '0'){
                console.log("school inst is 0")
                "{% for course,id in data %}"
                list.options.add("{{course}}", "{{ forloop.counter|add:"1" }}")
                "{% endfor %}"
            }
            else if (school_inst == '1'){
                console.log("school inst is 1")
                "{% for course,id in data %}"
                "{% if id == '1' %}"
                list.options.add("{{course}}", "{{ forloop.counter|add:"1" }}")
                "{% endif %}"
                "{% endfor %}"
            }
            else if (school_inst == '2'){
                console.log("school inst is 2")
                "{% for course,id in data %}"
                "{% if id == '2' %}"
                list.options.add("{{course}}", "{{ forloop.counter|add:"1" }}")
                "{% endif %}"
                "{% endfor %}"
            }

         }
         function displaysamemilitary() {
            var military_inst = $('#military').val()
            var list = document.getElementById('military_course')
            clearList(list);
            if (military_inst == '0'){
                {% for course,id in data %}
                list.options.add({{course}}, {{ forloop.counter|add:"1" }})
                {% endfor %}
            }
            if (military_inst == '3'){
                {% for course,id in data %}
                {% if id == '3' %}
                list.options.add({{course}}, {{ forloop.counter|add:"1" }})
                {% endif %}
                {% endfor %}
            }
            if (military_inst == '4'){
                {% for course,id in data %}
                {% if id == '4' %}
                list.options.add({{course}}, {{ forloop.counter|add:"1" }})
                {% endif %}
                {% endfor %}
            }
            if (military_inst == '5'){
                {% for course,id in data %}
                            {% if id == '5' %}
                list.options.add({{course}}, {{ forloop.counter|add:"1" }})
                {% endif %}
                {% endfor %}
            }
            if (military_inst == '6'){
                {% for course,id in data %}
                {% if id == '6' %}
                list.options.add({{course}}, {{ forloop.counter|add:"1" }})
                {% endif %}
                {% endfor %}
            }
            if (military_inst == '7'){
                {% for course,id in data %}
                {% if id == '7' %}
                list.options.add({{course}}, {{ forloop.counter|add:"1" }})
                {% endif %}
                {% endfor %}
            }
        }


function val() {
    console.log("in the beginning of display")
    d = document.getElementById("select_id").value;
    alert(d);
}

function displaysameschool(){
    console.log("in the beginning of display")
    var courses = {{data}}
    console.log(courses)
    console.log("testing")
 }

 function displaysameschool(){
            console.log("starting function")
            var school_inst = document.getElementById('select_institution').value;
            var list = document.getElementById('select_course');
            console.log(list);
            clearList(list);
            console.log(list);

            var course_codes = {{ data | js }};
            console.log(course_codes);
            var i;
            for(i = 0; i < course_codes.length; i++){
                if(course_codes[i][1] == school_inst){
                    list.options.add(course_codes[i][0], i);
                }
            }
         }

function checkselected(){
            var school_course = document.getElementById('select_course').value
            var military_course = document.getElementById('military_course').value

            if(school_course == 0 or military_course == 0){
                alert("you must select class!")
            }
        }


function checkselected(message){
            console.log("runing checkselected");
            var form = document.getElementById('generatebutton')
            var school_course = document.getElementById('select_course');
            var military_course = document.getElementById('military_course');
            console.log("runing checkselected");

            if(school_course.value == 0 ){
                console.log("alerting user");
                alert(message);
            }
            else if(military_course.value == 0){
                console.log("alerting user");
                alert(message);
            }
            else {
                form.appendChild(school_course);
                form.appendChild(military_course);
                form.submit();
                console.log("runing checkselected");
                alert("checking what this does");
            }
        }



























