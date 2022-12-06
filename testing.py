from app.commons.utils.datastore import *

details = {
			'name': "name",
			'mobile_number': "mobile",
			'email_id': "email_id",
			'student': "is_student",
			'name_of_institute': "name_of_institute",
			'year_of_education': "year_of_education",
			'name_of_company': "company",
			'designation': "designation",
			'looking_for_opportunities': "looking_for_opportunities",
		}


save_info(json.dumps(details))