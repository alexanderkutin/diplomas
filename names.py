import pandas as pd
import re
import os
from certs import generate_kpk_cert
from certs import TextElement

# Define endings dictionary for dative case transformations
endings = {
    'm': {
        'us': 'um',
        'is': 'im',
        's': 'am',
        'š': 'am',
        'e': 'em',
        'o': 'o',
        'a': 'am'
    },
    'v': {
        'us': 'um',
        'is': 'im',
        's': 'am',
        'š': 'am',
        'e': 'em',
        'o': 'o',
        'a': 'am'
    },
    'f': {
        'us': 'ui',
        'a': 'ai',
        'e': 'ei',
        'u': 'ai',
        's': 'ij',
        'o': 'o'
    },
    's': {
        'us': 'ui',
        'a': 'ai',
        'e': 'ei',
        'u': 'ai',
        's': 'ij',
        'o': 'o'
    }
}


# Function to convert a name to dative case
def convert_to_dative(full_name, gender):
    if not isinstance(full_name, str):
        return None
    if not isinstance(gender, str) or not gender.lower() in ['m', 'f', 's', 'v']:
        print(f'ERROR: INVALID GENDER FOR {full_name}!')
        return None

    names_and_delims = re.split(r'(\s+|-)', full_name)
    names_dative = ''
    for name in names_and_delims:
        if name.isalpha():
            for last_letter, dative_ending in endings[gender.lower()].items():
                if name.endswith(last_letter):
                    name = name[:-len(last_letter)] + dative_ending
        names_dative = names_dative + name

    return names_dative

def convert_names(filename, template, out_dir, name_params: TextElement, num_params: TextElement):
    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"Directory '{out_dir}' does not exist.")
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File '{template}' does not exist.")

    # Load CSV file without header and assign column names
    input_file = filename  # Replace with the path to your input CSV file
    df = pd.read_csv(input_file, header=None, encoding='utf-8', names=['Name', 'Nr', 'Sex'])

    # # Combine the modified first name and surname for the final output
    # df['Name_Surname_Dative'] = df['First_Name_Dative'] + ' ' + df['Surname_Dative']

    df['Name_Surname_Dative'] = df.apply(lambda row: convert_to_dative(row['Name'], row['Sex']), axis=1)

    full_names_dative = df[['Name_Surname_Dative', 'Nr']].values.tolist()

    for row in full_names_dative:
        if type(row[0]) == str and type(row[1]) == str:
            name_params.line = row[0]
            num_params.line = row[1]
            generate_kpk_cert(template, out_dir, name_params, num_params)


# convert_names('names.csv', 'template.pdf', 'certs')
# print(convert_to_dative('Mārtiņš Misāns-Kutins', 'm'))