import argparse
from argostranslate import package, translate

parser = argparse.ArgumentParser()
parser.add_argument("from_lang", help = "From Language, e.g. en")
parser.add_argument("to_lang", help = "To Language, e.g. es")
parser.add_argument("input_file", help = "Input Text File, e.g. abc.txt")
args = parser.parse_args()
 
#check if there is Argos Package index in local drive 
try:
    print("Getting the ArgosTranslate package index...")
    available_packages = package.get_available_packages()
except:
    package.update_package_index()
    available_packages = package.get_available_packages()

try: 
    selected_package = list(
    filter(
         lambda x: x.from_code == args.from_lang and x.to_code == args.to_lang, available_packages
    ))[0]
except: 
    print(f"Error for finding language pair for [{args.from_lang}] to [{args.to_lang}]")
    exit()

print(f"Download '{selected_package}' model from the ArgosTrans if no model is found in the current system...")
download_path = selected_package.download()
package.install_from_path(download_path)

#prepared the language pair
installed_languages = translate.get_installed_languages()
argo_from_lang = list(filter(lambda x: x.code == args.from_lang,installed_languages))[0]
argo_to_lang = list(filter(lambda x: x.code == args.to_lang,installed_languages))[0]
translation = argo_from_lang.get_translation(argo_to_lang)
translated_lines = []

print(f"Reading '{args.input_file}' and starting to translate...")
#load text from file
with open(args.input_file, encoding='utf8') as f:
    lines =  f.read().splitlines() 
    for l in lines:
        translated_l = translation.translate(l)
        translated_lines.append(translated_l)
translated_output = '\n'.join(translated_lines)

#save our translated result into a file
with open("output_"+args.input_file,'w',encoding='utf8') as o:
    o.write(translated_output)
print(f"Translated output is saved as 'output_{args.input_file}', enjoy!")