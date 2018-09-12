select row_number() over (order by te, nye asc) as id , * ,
0 as status
into chunk.n_za
from udc_country, udc_employee, udc_industry,udc_total_experience te, udc_no_of_year_in_current_comp nye
where countrycode = 'za';
delete 
	FROM chunk.n_za
	where emp_code = 'A' or industry_code in (96,84)
	
