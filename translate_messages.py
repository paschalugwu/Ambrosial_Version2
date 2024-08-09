import polib
from googletrans import Translator
import os

# List of target languages with their ISO 639-1 codes
LANGUAGES = {
    'fr': 'French'
}

def translate_messages():
    translator = Translator()
    pot_file = 'messages.pot'
    
    if not os.path.exists(pot_file):
        print(f"The file {pot_file} does not exist.")
        return

    # Load the .pot file
    pot = polib.pofile(pot_file)

    for lang_code, lang_name in LANGUAGES.items():
        print(f"Translating messages to {lang_name} ({lang_code})...")
        # Create a new PO file for the language
        po = polib.POFile()
        po.metadata = pot.metadata.copy()
        po.metadata['Language'] = lang_code

        for entry in pot:
            if entry.msgid.strip() == '':
                # Copy headers or empty entries
                new_entry = polib.POEntry(
                    msgid=entry.msgid,
                    msgstr=entry.msgstr,
                    occurrences=entry.occurrences,
                    comment=entry.comment
                )
            else:
                # Translate the msgid
                try:
                    translation = translator.translate(entry.msgid, dest=lang_code).text
                except Exception as e:
                    print(f"Error translating '{entry.msgid}': {e}")
                    translation = entry.msgid  # Fallback to original text if translation fails

                new_entry = polib.POEntry(
                    msgid=entry.msgid,
                    msgstr=translation,
                    occurrences=entry.occurrences,
                    comment=entry.comment
                )
            po.append(new_entry)

        # Define the path for the translated .po file
        lang_dir = os.path.join('translations', lang_code, 'LC_MESSAGES')
        os.makedirs(lang_dir, exist_ok=True)
        po_file_path = os.path.join(lang_dir, 'messages.po')
        po.save(po_file_path)
        print(f"Saved translated file to {po_file_path}")

    print("Translation completed for all languages.")

if __name__ == "__main__":
    translate_messages()
