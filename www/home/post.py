import cgi

form = cgi.FieldStorage()
course_code = form.getvalue('course_code')
text_course_code = form.getvalue('course_code_text')

#print("this is course_code in post: ", course_code)