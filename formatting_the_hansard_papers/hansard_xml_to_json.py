import xml.etree.ElementTree as ET
import json

# Load and parse the XML file
tree = ET.parse('./data/debates2024-02-08a.xml')
root = tree.getroot()

# Initialize a list to hold the debates
hansard_records = []
current_hansard_document = {}
current_debate = {}
current_speech = {}
speech_data = {}

# Iterate through the XML tree
for child in root:
    if child.tag == 'oral-heading':
        # Add the previous hansard document to the list of hansard records (if there is one).
        if bool(current_hansard_document): hansard_records.append(current_hansard_document)
            
        current_hansard_document = {
            'session_type': child.text.strip(),
            'session_type_id': child.attrib['id'],
            'debates': []
        }

    elif child.tag == 'major-heading':
        # Add the previous debate to the list of debates (if there is one).
        if bool(current_debate): current_hansard_document['debates'].append(current_debate)
        
        current_debate = {
            'session_topic': child.text.strip(),
            'session_topic_id': child.attrib['id'],
            'speeches': []
        }
    elif child.tag == 'minor-heading':
            # Add the previous debate to the list of debates (if there is one).
            if bool(current_speech): current_debate['speeches'].append(current_speech)
            
            current_speech = {
                    'debate_topic': child.text.strip(),
                    'debate_topic_id': child.attrib['id'],
                    'speech': []
                }
    elif child.tag == 'speech':
        if bool(speech_data): current_debate['speeches'].append(speech_data)
        speech_data = {
                        'id': child.attrib['id'],
                        'speaker': child.attrib.get('speakername', 'Unknown'),
                        'type': child.attrib.get('type', 'Unknown'),
                        'person_id': child.attrib.get('person_id', 'Unknown'),
                        'comment': [],
                        'column_number': child.attrib.get('colnum', 'Unknown')
                    } 
        for subchild in child:
                         speech_data['comment'].append({
                            'text_id': subchild.get('pid'),
                            'text': subchild.text
                         })
                         
# Add the final speech, minor heading, major heading and oral heading to the hansard records bottom up
if bool(speech_data): current_debate['speeches'].append(speech_data)
if bool(current_speech): current_debate['speeches'].append(current_speech)
if bool(current_debate): current_hansard_document['debates'].append(current_debate)
if bool(current_hansard_document): hansard_records.append(current_hansard_document)


# # Convert the debates list into JSON
json_output = json.dumps(hansard_records, indent=4)

# # Print the JSON output
print(json_output)

# # Optionally, save the JSON to a file
with open('debates2024-02-08a.json', 'w') as json_file:
    json_file.write(json_output)
