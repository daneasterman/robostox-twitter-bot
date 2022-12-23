import re
from helpers.forms import FORMS

def get_company_name(title):
	start_name = title.index(" - ") +3
	end_name = title.index("(") -1
	company_name = title[start_name:end_name]
	return company_name

def generate_form_explanation(form_type):
	form_explanation = FORMS.get(form_type, "")
	return form_explanation

def circle_brackets_data(title):
	string_list = re.findall(r'\(.*?\)', title)
	cik = string_list[0].strip("()")
	filing_entity = string_list[1].strip("()")
	return cik, filing_entity