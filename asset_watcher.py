import os

DO_RUN = True

# This should not run anywhere in the game
if (DO_RUN):
    catologue_name = "assets.py"

    graphic_files = [".png", ".jpg"]
    audio_files = [".wav", ".ogg"]

    filepaths = []
    folder = ""

    for root, dir, files in os.walk(os.getcwd()):
        for asset in files:
            if ('.' + asset.split('.')[-1]) in graphic_files:
                folder = "Graphics"
            elif ('.' + asset.split('.')[-1] in audio_files):
                folder = "Audio"
            else:
                continue

            cleaned_name = asset.split('.')[0].replace(" ", "_")
            filepaths.append(cleaned_name + " = " + "os.path.join(\"" + folder + "\", \"" + asset + "\")")

    output = "# Auto generated file from asset_watcher.py\n"
    output += "import os\n"
    output += "\n"

    for asset in filepaths:
        output += asset
        output += ("\n")


    asset_catalogue = open(catologue_name, "w")
    asset_catalogue.write (output)