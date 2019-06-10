import cgi

form = cgi.FieldStorage()
course_code = form.getvalue('course_code')

print(course_code)