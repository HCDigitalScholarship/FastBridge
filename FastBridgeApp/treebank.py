import csv
import xml.etree.ElementTree as ET

def xml_to_csv(xml_file_path, csv_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # define the header
    header = ['token_id', 'form', 'citation-part', 'lemma', 'part-of-speech', 'morphology', 'head-id', 'relation', 'information-status', 'presentation-after']

    csv_data = []
    csv_data.append(header)

    # Find all sentence elements and their children
    for sentence in root.iter('sentence'):
        for token in sentence.iter('token'):
            token_id = token.attrib.get('id', '')
            form = token.attrib.get('form', '')
            citation_part = token.attrib.get('citation-part', '')
            lemma = token.attrib.get('lemma', '')
            part_of_speech = token.attrib.get('part-of-speech', '')
            morphology = token.attrib.get('morphology', '')
            head_id = token.attrib.get('head-id', '')
            relation = token.attrib.get('relation', '')
            information_status = token.attrib.get('information-status', '')
            presentation_after = token.attrib.get('presentation-after', '')
            row = [token_id, form, citation_part, lemma, part_of_speech, morphology, head_id, relation, information_status, presentation_after]
            csv_data.append(row)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


#make sure xml_file is the relative path to the xml file
xml_file = 'FastBridgeApp\proiel_proiel-treebank_master_cic-att.xml'
csv_file = "output.csv"

xml_to_csv(xml_file, csv_file)