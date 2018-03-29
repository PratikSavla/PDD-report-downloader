print("Enter the Reg no:")
USERNAME = input("")
print("Enter the password")
PASSWORD = input("")
ELAB = "pdd"
import requests
import os
import img2pdf

def gen_report(username, password, elabx):

	elab = {'url': 'http://care2.srmuniv.ac.in/ktrswepdd/', 'code': 'c/c.code.php', 'key': 'c'}

	login_page = elab['url'] + 'login_check.php'
	home_page = elab['url'] + 'login/student/home.php'
	question_page = elab['url'] + 'login/student/code/' + elab['code'] + '?id=1&value='
	
	payload = {
		'uname': username,
		'pass': password
	}
	
	print('eLab Report Generator : ' + payload['uname'])
	
	with requests.Session() as s:
	
		s.post(login_page, data=payload)
		s.get(home_page)
	
		s.get(elab['url'] + 'login/student/question.php')
		s.post(elab['url'] + 'login/student/home.helper.php', data={'text': elab['key'].upper()})
		s.get(elab['url'] + 'login/student/question.php')
		s.get(elab['url'] + 'login/student/question.list.js')
		s.post(elab['url'] + 'login/student/course.get.php', data={'q': 'SESSION'})
		s.post(elab['url'] + 'login/student/course.get.php', data={'q': 'VALUES'})
		s.get(elab['url'] + 'login/student/code/' + elab['code'] + '?id=1&value=0')
		s.get(elab['url'] + 'Code-mirror/lib/codemirror.js')
		s.get(elab['url'] + 'Code-mirror/mode/clike/clike.js')
		s.get(elab['url'] + 'login/student/code/' + elab['key'] + '/code.elab.js')
		s.post(elab['url'] + 'login/student/code/code.get.php')
		s.post(elab['url'] + 'login/student/code/flag.checker.php')
	
		for i in range(0, 100):
	
			present_question = question_page + str(i)
			s.get(present_question)
			code = s.get(elab['url'] + 'login/student/code/code.get.php')
	
			if(code.text != ''):
	
				if(elab['key'] == 'daa'):
		
						evaluate_payload_c = s.post(elab['url'] + 'login/student/code/' + elab['key'] + '/code.evaluate.elab.php', data={'code': code.text, 'input': '', 'language': 'c'})
						evaluate_payload_cpp = s.post(elab['url'] + 'login/student/code/' + elab['key'] + '/code.evaluate.elab.php', data={'code': code.text, 'input': '', 'language': 'cpp'})
						evaluate_payload_java = s.post(elab['url'] + 'login/student/code/' + elab['key'] + '/code.evaluate.elab.php', data={'code': code.text, 'input': '', 'language': 'java'})
						evaluate_payload_python = s.post(elab['url'] + 'login/student/code/' + elab['key'] + '/code.evaluate.elab.php', data={'code': code.text, 'input': '', 'language': 'python'})
	
						if '100' in [evaluate_payload_c.text[-4:-1], evaluate_payload_cpp.text[-4:-1], evaluate_payload_java.text[-4:-1], evaluate_payload_python.text[-4:-1]]:
							complete_percent = '100'
						else:
							complete_percent = '0'
		
				else:
					evaluate_payload = s.post(elab['url'] + 'login/student/code/' + elab['key'] + '/code.evaluate.elab.php', data={'code': code.text, 'input': ''})
					complete_percent = evaluate_payload.text[-4:-1]
	
			
	
				if(complete_percent == '100'):
		
					print(str(i + 1) + ' : getting report')
					file = s.get(elab['url'] + 'login/student/code/getReport.php')
	
					with open(str(i).zfill(3) + '.png', 'wb') as f:
						f.write(file.content)
		
				else:
		
					print(str(i + 1) + ' : evaluation error : Couldn\'t get report')
	
			else:		
				print(str(i + 1) + ' : No code written')
	
		global filename
		filename = payload['uname'] + '-' + elabx.upper() + '.pdf'
		with open(filename, "ab") as f:
			f.write(img2pdf.convert([i for i in sorted(os.listdir('.')) if i.endswith('.png')]))
	
		print('PDF file named ' + filename + ' generated')
		for i in range(0, 100):
			if(os.path.isfile(str(i) + '.png')):
				os.remove(str(i) + '.png')
	
		print('Image files cleared')
gen_report(USERNAME, PASSWORD, ELAB)
