import xml.etree.ElementTree as ET
import json
import os

def parse_hansard_to_json(input_file_name):
    # Load and parse the XML file
    tree = ET.parse(input_file_name)
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
            if bool(current_hansard_document): hansard_records.append(current_hansard_document)
            current_hansard_document = {
                'session_type': child.text.strip(),
                'session_type_id': child.attrib['id'],
                'debates': []
            }

        elif child.tag == 'major-heading':
            if bool(current_debate): 
                if bool(current_hansard_document): current_hansard_document['debates'].append(current_debate)
                else: hansard_records.append(current_debate)
            current_debate = {
                'session_topic': child.text.strip(),
                'session_topic_id': child.attrib['id'],
                'speeches': []
            }

        elif child.tag == 'minor-heading':
            if bool(current_speech):
                if bool(current_debate): current_debate['speeches'].append(current_speech)
                elif bool(current_hansard_document): current_debate['debates'].append(current_speech)
                else: hansard_records.append(current_speech)
                
            current_speech = {
                'debate_topic': child.text.strip(),
                'debate_topic_id': child.attrib['id'],
                'speeches': []
            }

        elif child.tag == 'speech':
            if bool(speech_data):
                if bool(current_speech): current_speech['speeches'].append(speech_data)
                elif bool(current_debate): current_debate['speeches'].append(speech_data)
                elif bool(current_hansard_document): current_hansard_document['debates'].append(speech_data)
                
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

    # Add the final elements to the hansard records bottom up
    if bool(current_speech): current_speech['speeches'].append(speech_data)
    elif bool(current_debate): current_debate['speeches'].append(speech_data)
    elif bool(current_hansard_document): current_hansard_document['debates'].append(speech_data)
    else: hansard_records.append(speech_data)
            
    if bool(current_speech):
        if bool(current_debate): current_debate['speeches'].append(current_speech)
        elif bool(current_hansard_document): current_debate['debates'].append(current_speech)
        else: hansard_records.append(current_speech)
    
    if bool(current_debate): 
        if bool(current_hansard_document): current_hansard_document['debates'].append(current_debate)
        else: hansard_records.append(current_debate)
        
    if bool(current_hansard_document): hansard_records.append(current_hansard_document)

    json_output = json.dumps(hansard_records, indent=4)

    # Derive the output filename from the input filename
    base_name = os.path.splitext(os.path.basename(input_file_name))[0]
    output_file_name = f'{base_name}.json'

    # Save the JSON to a file
    with open('./data/data_in_json/' + output_file_name, 'w') as json_file:
        json_file.write(json_output)

    print(f'JSON output saved to {output_file_name}')

