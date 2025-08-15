from openai import OpenAI
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
	from openai.types.chat import ChatCompletion


API_KEY				= 'EMPTY'
API_URL				= ''
MODEL				= ''
SUBSTITUTE_NAME		= '[NAME]'
SUBSTITUTE_ADDRESS 	= '[ADDRESS]'
SUBSTITUTE_PHONE	= '[PHONE]'


client = OpenAI(
	base_url= API_URL,
	api_key	= API_KEY
)

prompt = f"""You are a data anonymization assistant

Replace all personal firstname and lastnames in the following text with 
{SUBSTITUTE_NAME}, all addresses with {SUBSTITUTE_ADDRESS} and all phone 
numbers with {SUBSTITUTE_PHONE}.

Do not replace words that are genetic terms or labels, such as "name" or 
"address", unless they are followed by or include real personal information.

Dont replace company or organization names.

If no personal names, addresses or phone numbers are found, return the 
original text unchanged.

Return only the modified or original text. Do not include any explanations 
or introductions.
"""

def mask_gdpr(query:str, minimal_resp=True) -> Union[str, "ChatCompletion"]:
	response = client.chat.completions.create(
		model 	= MODEL,
		messages= [
			{'role': 'system', 'content': prompt},
			{'role': 'user', 'content': query}
		]
	)
	if minimal_resp:
		content = response.choices[0].message.content
		return content.strip() if content else ''
	return response
