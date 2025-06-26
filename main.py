"""
Given a tsv file containing a column 'type' and column 'label', and optional columns 'group' and 'key',
generate a Palmyra config file.

Usage:
    main (-i <input> | --input=<input>)
        (-d <default> | --default=<default>)
    main (-h | --help)

Options:
    -i <input> --input=<input>
        A tsv file containing POS and relation labels (see data/sample.tsv)
    -d <default> --default=<default>
        The default POS tag used when creating a new node in Palmyra
    -h --help
        Show this screen.

"""
import json
import pandas as pd
from docopt import docopt

arguments = docopt(__doc__)

def set_up_df(df):
    """Checks if optional group and key columns exist, fills with default values if not.
    Also removes duplicates based on the label column

    Args:
        df (pd.DataFrame): pandas DataFrame
    """
    df.drop_duplicates(subset=['label'], keep='first', inplace=True)

    if 'group' not in df.columns:
        df['group'] = '1'
    if 'key' not in df.columns:
        shortcuts = pd.read_csv('data/shortcut_list.tsv', sep='\t')
        shortcuts_dict = dict(zip(shortcuts['arabic_char'], shortcuts['default_keys']))
        df['key'] = df.label.str[0].replace(shortcuts_dict).str.lower()
    
    return df



def generate_boilerplate(default_pos):
    return {
        "display_text": "text",
        "orientation": "r-to-l",
        "lemma": "false",
        "features": [],
        "defaultFeatures": [],
        "newNodeDefaults": {
            "pos": f"{default_pos}",
            "relation": "---",
            "name": "*"
        }
    }

def get_pos_details(pos_df):
    # return a list of pos entries [{"label": "NOM", "key": "n", "group": "1" }]
    return {'values': pos_df[['label', 'group', 'key']].to_dict('records')}

def get_relation_details(relation_df):
    # return a list of pos entries [{ "label": "SBJ", "key": "s", "group": "1" }]
    return {'values': relation_df[['label', 'group', 'key']].to_dict('records')}

def main():
    # df = pd.read_csv('data/sample.tsv', sep='\t')
    df = pd.read_csv(arguments['--input'], sep='\t')

    df = set_up_df(df)

    config_dict = generate_boilerplate(arguments['--default'])
    
    config_dict['pos'] = get_pos_details(df[df.type == 'pos'])
    config_dict['relation'] = get_pos_details(df[df.type == 'relation'])
    
    # with open("data/sample_output.config", "w") as f:
    print(json.dumps(config_dict, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
